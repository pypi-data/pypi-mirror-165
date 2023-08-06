import sys, os
from time import gmtime, strftime
import numpy as np
import logging

file_handler = logging.FileHandler(filename='nustar_utils_%s.log' % (strftime("%Y-%m-%dT%H:%M:%S", gmtime())))
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [stdout_handler, file_handler]

logging.basicConfig(level=logging.INFO, format=' %(levelname)s - %(message)s', handlers=handlers)
#[%(asctime)s] {%(filename)s:%(lineno)d}
logger = logging.getLogger()

from subprocess import Popen, PIPE, STDOUT

def log_subprocess_output(pipe):
    for line in iter(pipe.readline, b''): # b'\n'-separated lines
        logging.info(line.decode()[0:-1])

#shell_cmd = os.environ['HOME'] + '/Soft/timingsuite/dist/Debug/GNU-MacOSX/timingsuite <timing_cmd.txt'
shell_cmd = 'timingsuite <timing_cmd.txt'


def run(cmd=shell_cmd):
    logger.info("------------------------------------------------------------------------------------------------\n")
    logger.info("**** running %s ****\n" % cmd)
    #out=subprocess.call(cmd, stdout=logger, stderr=logger, shell=True)
    process = Popen('export DYLD_LIBRARY_PATH=$HEADAS/lib;'+cmd, stdout=PIPE, stderr=STDOUT, shell=True)
    with process.stdout:
        log_subprocess_output(process.stdout)
    out = process.wait()  # 0 means success

    logger.info("------------------------------------------------------------------------------------------------\n")

    logger.info("Command '%s' finished with exit value %d" % (cmd, out))

    return out

def get_obsids(src):
    from astroquery.heasarc import Heasarc
    from astropy.io import ascii
    heasarc = Heasarc()
    payload = heasarc._args_to_payload(mission='numaster', entry=src, radius='10 arcmin')
    table = heasarc.query_async(payload)

    table_body = table.content.decode().split('END')[-1].strip().split('\n')
    table_body_clean = [cc for cc in table_body if 'SCIENCE' in cc and 'archived' in cc]
    logger.info("************************************")
    logger.info(src)
    logger.info("************************************")
    logger.info(table_body_clean)
    logger.info("************************************")

    try:
        data = ascii.read(table_body_clean, format='fixed_width_no_header', delimiter=' ')
        logger.info(data['col5'])
        output = [str(x) for x in data['col5'].data]
    except:
        logger.warning('No OBSIDS')
        output =[]

    return output


def plot_periodogram():
    with open('ef_pipe_periodogram_f.qdp') as ff:
        qdp_lines = ff.readlines()
    with open('tmp.qdp', 'w') as ff:
        ff.write(qdp_lines[0])
        ff.write('cpd tmp.gif/GIF\n')
        ff.write('scr white\n')
        ff.write('ma 17 on\n')
        ff.write('time off\n')
        ff.write('lab f\n')
        for ll in qdp_lines[2:]:

            ff.write(ll)
        ff.write('\n')


    run("qdp tmp.qdp")
    from IPython.display import Image
    from IPython.display import display
    _ = display(Image(filename='tmp.gif', format="gif"))


efold_cmd='''14
1
list_evt.txt
%f
%f
ef_pipe
n
%d

%f
%f
1
0
'''

efold_orbit_cmd='''14
1
list_evt.txt
%f
%f
ef_pipe
y
%s
%d

%f
%f
1
0
'''

def get_efold_frequency(nu_min, nu_max, min_en=3., max_en=20., n_bins=32, unit='A',orbitfile=None):
    with open('list_evt.txt', 'w') as ff:
        ff.write('source%s.evt' % unit)

    with open('timing_cmd.txt', 'w') as ff:
        if orbitfile is None:
            ff.write(efold_cmd % (min_en, max_en, n_bins, nu_min, nu_max))
        else:
            ff.write(efold_orbit_cmd % (min_en, max_en,orbitfile, n_bins, nu_min, nu_max))

    run()

    plot_periodogram()

    x = np.loadtxt('ef_pipe_res.dat')

    return x[2]

enphase_cmd='''17
list_evt.txt
none
%s
n
%d

%f
0
0
n
%f
%f
%f
0
0
0
1000000000
'''

def make_enphase(freq,  min_en=3., max_en=70., en_step=0.5, n_bins=32):
    for tt in ['source', 'background']:
        for unit in ['A', 'B']:
            with open('list_evt.txt', 'w') as ff:
                ff.write('%s%s.evt' % (tt, unit))

            with open('timing_cmd.txt', 'w') as ff:
                ff.write(enphase_cmd % ('%s%s_ENPHASE.fits' % (tt, unit),
                                 n_bins, freq, en_step, min_en, max_en) )

            run()

tphase_cmd='''12
list_evt.txt
none
%s
n
%d

%f
0
0
n
%f
0
0
%f
%f
'''

def make_tphase(freq,  min_en=3., max_en=70., t_step=1000, n_bins=32):
    for tt in ['source', 'background']:
        for unit in ['A', 'B']:
            with open('list_evt.txt', 'w') as ff:
                ff.write('%s%s.evt' % (tt, unit))

            with open('timing_cmd.txt', 'w') as ff:
                ff.write(tphase_cmd % ('%s%s_TPHASE.fits' % (tt, unit),
                                 n_bins, freq, t_step, min_en, max_en) )

            run()

def rebin_matrix(e_min, e_max, pp, dpp, min_s_n = 50):

    new_pulses = []
    dnew_pulses = []
    new_e_mins = []
    new_e_maxs = []
    i1 = 0
    while i1 < len(e_min) - 1:
        p1 = pp[i1, :]
        dp1 = dpp[i1, :]
        i1_store = i1
        logger.debug(i1)
        for i2 in range(i1 + 1, len(e_min)):

            s_n = np.sum(p1) / np.sqrt(np.sum(dp1 ** 2))
            logger.debug(s_n)
            if s_n >= min_s_n or i2 == len(e_min) - 1:
                new_pulses.append(p1/float(i2-i1_store))
                dnew_pulses.append(dp1/float(i2-i1_store))
                new_e_mins.append(e_min[i1_store])
                new_e_maxs.append(e_max[i2 - 1])
                logger.debug("Boom", s_n, i1_store, i2)
                i1 = i2
                break
            else:
                logger.debug("i2", i2)
                p1 += pp[i2, :]
                dp1 = np.sqrt(dp1 ** 2 + dpp[i2, :] ** 2)
                i1 = i2 - 1

    logger.info('We rebinned from %d to %d bins at a minimum S/N of %.1f' % (len(e_min), len(new_e_mins), min_s_n))

    return np.array(new_e_mins), np.array(new_e_maxs), np.array(new_pulses), np.array(dnew_pulses)


import random


def fake_profile(conteggi, errore):
    random_pulse = []

    for i in range(len(conteggi)):
        # print(conteggi[i],errore[i])
        pulse = random.gauss(conteggi[i], errore[i])
        random_pulse.append(pulse)

    return np.array(random_pulse)


def pulse_fraction_from_data_rms(counts, counts_err, n_harm=3):
    a0 = np.mean(counts)
    K = n_harm
    N = np.size(counts)

    A = np.zeros(K)
    B = np.zeros(K)

    a = np.zeros(K)
    b = np.zeros(K)
    sigma_a = np.zeros(K)
    sigma_b = np.zeros(K)

    k = 0
    while k < K:
        L = np.zeros(N)
        M = np.zeros(N)
        P = np.zeros(N)
        O = np.zeros(N)
        # print('K=',k+1)
        for i in range(0, N):
            # print('aaaah: ',k,i)
            argsinus = (2 * np.pi * (k + 1) * (i + 1)) / N
            # print('argsin di '+str(k+1),' '+str(i+1)+' :',argsinus)
            L[i] = counts[i] * np.cos(argsinus)
            # print(L)
            # print('L: ',L[i])
            M[i] = counts[i] * np.sin(argsinus)
            # print('M: ',M[i])
            P[i] = counts_err[i] ** 2 * np.cos(argsinus) ** 2
            O[i] = counts_err[i] ** 2 * np.sin(argsinus) ** 2
            #
        A[k] = np.sum(L)
        # print('A:',A[k])
        B[k] = np.sum(M)
        # print('B: ',B)
        SIGMA_A = np.sum(P)
        SIGMA_B = np.sum(O)
        #
        a[k] = (1. / N) * A[k]
        # print(a[k])
        b[k] = (1. / N) * B[k]
        sigma_a[k] = (1. / (N ** 2)) * SIGMA_A
        sigma_b[k] = (1. / (N ** 2)) * SIGMA_B
        k = k + 1

    somma = a ** 2 + b ** 2
    # print(somma)
    differenza = sigma_a ** 2 + sigma_b ** 2
    bla = somma - differenza
    # print('diff: ',differenza)
    PF_rms = np.sqrt(2 * sum(bla)) / a0
    return (PF_rms)


def get_error_from_simul_rms(counts, counts_err, n_simul=100, n_harm=3):
    simul_rms = []
    for i in range(n_simul):
        fp = fake_profile(counts, counts_err)
        simul_rms.append(pulse_fraction_from_data_rms(fp, counts_err, n_harm))

    return np.std(simul_rms)

def pulse_fraction_from_data_min_max(x,dx):

    i_min = np.argmin(x)
    i_max = np.argmax(x)
    tmp1 = (x[i_min]+x[i_max])
    pulsed_frac = (x[i_max] - x[i_min]) / tmp1
    dpulsed_frac = 2*np.sqrt((x[i_max]/tmp1**2)**2 * dx[i_max]**2 + (x[i_min]/tmp1**2)**2 * dx[i_min]**2)

    return pulsed_frac, dpulsed_frac

def plot_matrix_as_image(ee, pp, kind='E', normalize=True,outfile=None):
    pp1 = pp.copy()
    if normalize:
        for i in range(pp.shape[0]):
            x = pp[i, :]
            m = np.mean(x)
            s = np.std(x)
            pp1[i, :] = (x - m) / s

    phi = np.linspace(0, 1, pp.shape[1])
    import matplotlib.pyplot as plt
    plt.figure()
    plt.contourf(phi, ee, pp1)

    plt.xlabel('Phase')
    if kind=='E':
        plt.yscale('log')
        plt.ylabel('Energy [keV]')
    elif kind=='T':
        plt.ylabel('Time [s]')
    if outfile is not None:
        plt.savefig(outfile)

def plot_matrix_as_lines(t, pp, dpp, kind='T', normalize=False):

    pt = pp.copy()
    dpt = dpp.copy()
    if normalize:
        for i in range(pp.shape[0]):
            x = pp[i, :]
            dx = pp[i, :]
            m = np.mean(x)
            s = np.std(x)
            pt[i, :] = (x - m) / s
            dpt[i, :] = dx / s

    import matplotlib.pyplot as plt
    plt.figure()
    phi = np.linspace(0, 1, pt.shape[1])

    for i in range(pt.shape[0]):

        y = pt[i, :]
        dy = dpt[i, :]
        if np.sum(dy) > 0:
            if np.sum(y) / np.sqrt(np.sum(dy ** 2)) > 10:
                label = "%.0f s" % ( t[i] - t[0])
                if kind == 'E':
                    label = "%.0f keV" % t[i]
                plt.errorbar(phi, y, xerr=0.5 / pt.shape[1], yerr=dy, linestyle='', marker='o', label=label)

    plt.ylabel('Rate per bin')
    plt.xlabel('Phase')
    plt.legend()

def get_fourier_coeff(pulse):
    phi = np.linspace(0, 2 * np.pi, len(pulse))
    i_c = np.sum(np.cos(phi) * pulse) / np.pi
    i_s = np.sum(np.sin(phi) * pulse) / np.pi
    i_c2 = np.sum(np.cos(2 * phi) * pulse) / np.pi
    i_s2 = np.sum(np.sin(2 * phi) * pulse) / np.pi

    phi0 = np.arctan2(i_s, i_c) / 2 / np.pi
    phi0_2 = np.arctan2(i_s2, i_c2) / 2 / np.pi
    A = np.sqrt(i_c * i_c + i_s * i_s) / len(pulse) / np.mean(pulse)

    A2 = np.sqrt(i_c2 * i_c2 + i_s2 * i_s2) / len(pulse) / np.mean(pulse)
    return phi0, phi0_2, A, A2

def get_fourier_coeff_error( counts, counts_err, n_simul=100):

    sim_phi0 = []
    sim_phi0_2 = []
    sim_A = []
    sim_A2 = []

    for i in range(n_simul):
        fp = fake_profile(counts, counts_err)
        phi0, phi0_2, A, A2 = get_fourier_coeff(fp)
        sim_phi0.append(phi0)
        sim_phi0_2.append(phi0_2)
        sim_A.append(A)
        sim_A2.append(A)

    return np.std(sim_phi0), np.std(sim_phi0_2,), np.std(sim_A), np.std(sim_A2)

def get_target_coords_extern(input_name):
    from astroquery.simbad import Simbad
    from astropy import units as u
    from astropy.coordinates import SkyCoord

    name = input_name
    simbad = Simbad.query_object(name)
    c = SkyCoord(simbad['RA'], simbad['DEC'], unit=[u.hour, u.deg])
    c.fk5
    logger.info("Coordinates for %s are RA=%.4f, Dec=%.4f" % (name, c.ra.deg[0], c.dec.deg[0]))

    return c.ra.deg[0], c.dec.deg[0]
