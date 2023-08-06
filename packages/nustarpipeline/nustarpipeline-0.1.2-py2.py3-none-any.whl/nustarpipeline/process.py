#!/usr/bin/env python
#

import sys
import os
from time import gmtime, strftime
import glob

import argparse

import logging
from subprocess import Popen, PIPE, STDOUT

file_handler = logging.FileHandler(filename='nustar_utils_%s.log' % (strftime("%Y-%m-%dT%H:%M:%S", gmtime())))
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [stdout_handler, file_handler]

logging.basicConfig(level=logging.INFO, format=' %(levelname)s - %(message)s', handlers=handlers)
#[%(asctime)s] {%(filename)s:%(lineno)d}
logger = logging.getLogger()

def log_subprocess_output(pipe):
	for line in iter(pipe.readline, b''): # b'\n'-separated lines
		logging.info(line.decode()[0:-1])

def get_latest_file(path, *paths):
	'''
	Returns the name of the latest (most recent) file
	of the joined path(s)
	'''
	fullpath = os.path.join(path, *paths)
	files = glob.glob(fullpath)  # You may use iglob in Python3
	if not files:                # I prefer using the negation
		return None                      # because it behaves like a shortcut
	latest_file = max(files, key=os.path.getctime)
	_, filename = os.path.split(latest_file)
	return filename

def get_channel(e):
	'''
	gets the PI channel from energy scale
	http://heasarc.gsfc.nasa.gov/docs/nustar/nustar_faq.html#pi_to_energy
	'''

	return int((e-1.6)/0.04)

def prepare_outdir(outdir):

	'''
	:param outdir:
	:return:
	Creates outdir and pfiles directory
	sets pfiles in there
	'''

	if (not os.path.isdir(outdir)):
		os.makedirs(outdir)

	if (not os.path.isdir(os.path.join(outdir, "pfiles"))):
		os.makedirs(os.path.join(outdir, "pfiles"))

	old_pfiles=os.environ["PFILES"]
	tmp=old_pfiles.split(";")
	sys_pfiles=tmp[-1]

	os.environ["PFILES"]=os.path.join(os.getcwd(),os.path.join(outdir, "pfiles"))+";"+sys_pfiles
	logger.info("PFILES = "+os.environ["PFILES"])
	return
	# time_stamp=strftime("%Y-%m-%dT%H:%M:%S", gmtime())
	# return outdir+"/logfile_"+time_stamp+".txt"

def run(command):
	#source $CALDB/software/tools/caldbinit.sh;
	true_command = 'export HEADASNOQUERY="";export HEADASPROMPT=/dev/nul;' + \
		command
	logger.info("------------------------------------------------------------------------------------------------\n")
	logger.info("**** running %s ****\n" % command)
	#out=subprocess.call(cmd, stdout=logger, stderr=logger, shell=True)
	process = Popen(true_command, stdout=PIPE, stderr=STDOUT, shell=True)
	with process.stdout:
		log_subprocess_output(process.stdout)
	ret_value = process.wait()  # 0 means success
	logger.info("------------------------------------------------------------------------------------------------\n")
	logger.info("Command '%s' finished with exit value %d" % (command, ret_value))
	return ret_value

def get_data(obsid):
	cmd="wget -q -nH --no-check-certificate --cut-dirs=6 -r -l0 -c -N -np -R 'index*' -erobots=off --retr-symlinks https://heasarc.gsfc.nasa.gov/FTP/nustar/data/obs/"+obsid[1:3]+"/"+obsid[0]+"/"+obsid+"/"
	return run(cmd)

def write_region(fname, ra, dec, src_flag, ra_back=-1, dec_back=-1, radius=120):
	ff=open(fname,'w')
	ff.write("global color=green dashlist=8 3 width=1 font=\"helvetica 10 normal roman\" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\nfk5\n")
	if src_flag:
		ff.write("circle(%.4f,%.4f,%.0f\")"%(ra,dec, radius))
	else:
		#The default is just a guess
		if ra_back == -1:
			ra_deg=float(ra)-0.14
		else:
			ra_deg = float(ra_back)
		if dec_back == -1:
			dec_deg=float(dec)-0.08
		else:
			dec_deg=float(dec_back)

		ff.write("circle(%.4f,%.4f,%.4f\")"%(ra_deg,dec_deg, float(radius)))
	ff.close()


def wrap_process(obsid, ra_src, dec_src, outdir_base, pipeline_flag=False, spec_flag=False, lc_flag=False,
				 ds9_flag=False, ra_back=-1, dec_back=-1, radius=120, write_baryevtfile_flag=False,
				 filter_evt_flag=False, user_gti_file='none',
				 repository_location=os.environ['HOME'] + '/NUSTAR/Repository', t_bin=100., e_min=3., e_max=30.):
	if (not os.path.isdir(repository_location + "/" + obsid)):
		logger.error("The obsid you specified (" + obsid + ") does not exist in the repository " + repository_location)
		return 1

	logger.info("Processing OBSID %s for RA=%f Dec=%f with outdir base %s" % (obsid, ra_src, dec_src, outdir_base))
	logger.info("Pipeline flag %r" % (pipeline_flag))
	logger.info("Spectrum flag %r" % (spec_flag))
	logger.info("Lightcurve flag %r" % (lc_flag))

	outdir_pipeline = outdir_base + "_pipeline"
	logger.info("The output of standard pipelines are in " + outdir_pipeline)

	if pipeline_flag:

		# logfile_name =
		prepare_outdir(outdir_pipeline)
		# logfile = open(logfile_name, 'w')
		#print("writing output to log file: %s" % logfile_name)

		cmd = "nupipeline indir=" + repository_location + "/" + obsid + " steminputs=nu" + obsid + " obsmode=Science outdir=" + outdir_pipeline

		run(cmd)
		# logfile.close()

	if lc_flag:

		import shutil
		if not os.path.isdir(outdir_pipeline):
			logger.error("You need to have processed the pipeline before light curve extraction. Folder %s does not exist" % (
				outdir_pipeline))
			return 1
		outdir = outdir_base + "_lc"
		# logfile_name = \
		prepare_outdir(outdir)
		# logfile = open(logfile_name, 'w')
		# logger.info("writing output to log file: %s" % logfile_name)

		##searh clock file
		latest_clock = get_latest_file(repository_location + "/clock/*")

		ch_min = get_channel(e_min)
		ch_max = get_channel(e_max)
		logger.info("Energy scale E = Channel Number * 0.04 keV + 1.6 keV\n")
		logger.info("E_min=%f E_max=%f t_bin=%f ch_min=%d ch_max=%d\n" % (e_min, e_max, t_bin, ch_min, ch_max))

		src_region = outdir + "/sourceA.reg"
		if (not os.path.isfile(src_region)):
			write_region(src_region, ra_src, dec_src, True)

		bkg_region = outdir + "/backgroundA.reg"
		if (not os.path.isfile(bkg_region)):
			spec_bkg = outdir_base + "_spec/backgroundA.reg"
			if (os.path.isfile(spec_bkg)):
				shutil.copy(spec_bkg, bkg_region)
			else:
				write_region(bkg_region, ra_src, dec_src, False, ra_back=ra_back, dec_back=dec_back, radius=radius)

		cmd = "nuproducts indir=" + outdir_pipeline + " instrument=FPMA steminputs=nu" + obsid + " stemout=FPMA_%.1f_%.1f outdir=" % (
		e_min, e_max) + outdir
		cmd += " srcregionfile=" + src_region + " bkgextract=yes runbackscale=no binsize=%f pilow=%d pihigh=%d barycorr=yes" % (
		t_bin, ch_min, ch_max)
		cmd += " orbitfile=" + repository_location + "/" + obsid + "/auxil/nu" + obsid + "_orb.fits.gz cleanup=no srcra_barycorr=%f" % (
			ra_src)
		cmd += " srcdec_barycorr=%f" % (
			dec_src) + " bkglcfile=DEFAULT bkgregionfile=" + bkg_region + " runmkarf=no runmkrmf=no phafile=NONE imagefile=NONE"
		if write_baryevtfile_flag:
			cmd += " write_baryevtfile=yes"

		# print("My latest clock is " + latest_clock)
		if latest_clock != None:
			cmd += " clockfile=\"" + repository_location + "/clock/" + latest_clock + "\""

		if user_gti_file != 'none':
			cmd += " usrgtifile=" + user_gti_file + " usrgtibarycorr=yes"

		run(cmd)

		src_region = outdir + "/sourceB.reg"
		if (not os.path.isfile(src_region)):
			write_region(src_region, ra_src, dec_src, True)

		bkg_region = outdir + "/backgroundB.reg"
		if (not os.path.isfile(bkg_region)):
			spec_bkg = outdir_base + "_spec/backgroundB.reg"
			if (os.path.isfile(spec_bkg)):
				shutil.copy(spec_bkg, bkg_region)
			else:
				write_region(bkg_region, ra_src, dec_src, False, ra_back=ra_back, dec_back=dec_back, radius=radius)

		cmd = "nuproducts indir=" + outdir_pipeline + " instrument=FPMB steminputs=nu" + obsid + " stemout=FPMB_%.1f_%.1f outdir=" % (
		e_min, e_max) + outdir
		cmd += " srcregionfile=" + src_region + " bkgextract=yes runbackscale=no binsize=%f pilow=%d pihigh=%d barycorr=yes" % (
		t_bin, ch_min, ch_max)
		cmd += " orbitfile=" + repository_location + "/" + obsid + "/auxil/nu" + obsid + "_orb.fits.gz cleanup=no srcra_barycorr=%f" % (
			ra_src)
		cmd += " srcdec_barycorr=%f" % (
			dec_src) + " bkglcfile=DEFAULT bkgregionfile=" + bkg_region + " runmkarf=no runmkrmf=no phafile=NONE imagefile=NONE"
		if write_baryevtfile_flag:
			cmd += " write_baryevtfile=yes"

		if latest_clock != None:
			cmd += " clockfile=\"" + repository_location + "/clock/" + latest_clock + "\""

		if user_gti_file != 'none':
			cmd += " usrgtifile=" + user_gti_file + " usrgtibarycorr=yes"

		run(cmd)

		if filter_evt_flag:
			xsel_cmd = '''dummy
	read eve
	./ 
	FPM%s_%.1f_%.1f_cl_barycorr.evt 
	yes 
	filter reg %s%s.reg 
	extra eve
	save eve %s%s.evt




	quit





	'''
			os.chdir(outdir_base + '_lc')
			for unit in ['A', 'B']:
				for reg in ['source', 'background']:
					with open('xsel_%s_%s.txt' % (reg, unit), 'w') as ff:
						ff.write(xsel_cmd % ('A', e_min, e_max, reg, unit, reg, unit))
					cmd = 'xselect < ' + 'xsel_%s_%s.txt' % (reg, unit)
					run(cmd)
			os.chdir('..')
		# logfile.close()

	if spec_flag:
		if not os.path.isdir(outdir_pipeline):
			logger.error("You need to have processed the pipeline before spectral extraction. Folder %s does not exist" % (
				outdir_pipeline))
			return 1
		outdir = outdir_base + "_spec"
		#logfile_name = \
		prepare_outdir(outdir)

		src_regionA = outdir + "/sourceA.reg"
		if (not os.path.isfile(src_regionA)):
			write_region(src_regionA, ra_src, dec_src, True)
		src_regionB = outdir + "/sourceB.reg"
		if (not os.path.isfile(src_regionB)):
			write_region(src_regionB, ra_src, dec_src, True)
		bkg_regionA = outdir + "/backgroundA.reg"
		if (not os.path.isfile(bkg_regionA)):
			write_region(bkg_regionA, ra_src, dec_src, False, ra_back=ra_back, dec_back=dec_back, radius=radius)
		bkg_regionB = outdir + "/backgroundB.reg"
		if (not os.path.isfile(bkg_regionB)):
			write_region(bkg_regionB, ra_src, dec_src, False, ra_back=ra_back, dec_back=dec_back, radius=radius)


		if not ds9_flag:
			logger.info("Please check the regions for FPMA")
			cmd = "ds9 -scale log " + outdir_pipeline + "/nu" + obsid + "A01_cl.evt -regions " + src_regionA + " -regions " + bkg_regionA
			run(cmd)
			logger.info("Please check the regions for FPMB")
			cmd = "ds9 -scale log " + outdir_pipeline + "/nu" + obsid + "B01_cl.evt -regions " + src_regionB + " -regions " + bkg_regionB
			run(cmd)

			#logger.info("Have you checked properly the region files?(y/Y will continue the processing any other key stop it)")
			logger.warning("We ask to rerun the analysis disabling the ds9 iteractive command with which you have checked the region files")
			# ans = input("Please enter the key: ...")
			# if (not (ans == 'y')) and (not (ans == 'Y')):
			# 	print("Exit processing")
			return 0

		cmd = "cd " + outdir + ";nuproducts indir=../" + outdir_pipeline + " instrument=FPMA steminputs=nu" + obsid + " stemout=FPMA outdir=."  # +outdir
		cmd += " srcregionfile=../" + src_regionA + " bkgregionfile=../" + bkg_regionA + " bkgextract=yes runbackscale=yes cleanup=yes "
		cmd += " lcfile=NONE bkglcfile=NONE runmkarf=yes runmkrmf=yes imagefile=NONE clobber=yes"

		if user_gti_file != 'none':
			cmd += " usrgtifile=../" + user_gti_file + " usrgtibarycorr=no"

		cmd += ";cd .."
		run(cmd)

		cmd = "cd " + outdir + ";nuproducts indir=../" + outdir_pipeline + " instrument=FPMB steminputs=nu" + obsid + " stemout=FPMB outdir=."  # +outdir
		cmd += " srcregionfile=../" + src_regionB + " bkgregionfile=../" + bkg_regionB + " bkgextract=yes runbackscale=yes cleanup=yes "
		cmd += " lcfile=NONE bkglcfile=NONE runmkarf=yes runmkrmf=yes imagefile=NONE clobber=yes"

		if user_gti_file != 'none':
			cmd += " usrgtifile=../" + user_gti_file + " usrgtibarycorr=no"

		cmd += ";cd .."

		run(cmd)

		cmd = "optimal_binning.py " + outdir + "/FPMA_sr.pha -b " + outdir + "/FPMA_bk.pha -r " + outdir + "/FPMA_sr.rmf -a " + outdir + "/FPMA_sr.arf -e 3 -E 78"
		run(cmd)

		cmd = "optimal_binning.py " + outdir + "/FPMB_sr.pha -b " + outdir + "/FPMB_bk.pha -r " + outdir + "/FPMB_sr.rmf -a " + outdir + "/FPMB_sr.arf -e 3 -E 78"
		run(cmd)

		#logfile.close()
	return 0


def process():
	help = sys.argv[0] + '\n'
	help += '\n'
	help += 'Process Nustar repository and extracts only LC and image or also spectrum with background\n'

	parser = argparse.ArgumentParser(description='Process Nustar Data',
									 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('OBSID', metavar='obsid', type=str, nargs=1, help='OBSID in the Repository folder')
	parser.add_argument("RA", metavar='ra', nargs=1, help="RA of the source", type=float)
	parser.add_argument("Dec", metavar='dec', nargs=1, help="Dec of the source", type=float)
	parser.add_argument('outdir', metavar='outdir', type=str, nargs=1,
						help='output folder base name (to be appended with _pipeline, _lc, or _spec')

	parser.add_argument("--pipeline", help="Run pipeline", action='store_true')
	parser.add_argument("--spec", help="Run spectral extraction", action='store_true')
	parser.add_argument("--lightcurve", help="Run light curve extraction", action='store_true')
	parser.add_argument("--filter_evt", help="Extract events for region files", action='store_true')

	parser.add_argument("--no-ds9", help="Avoid ds9 display", action='store_true')

	parser.add_argument("--usergti", help="User defined GTIs", type=str, default='none')

	parser.add_argument("--timebin", help="timebin for LC (s)", type=float, default=100)

	parser.add_argument("--eMin", help="minimum energy (keV) for LC", type=float, default=3)
	parser.add_argument("--eMax", help="maximum energy (keV) for LC", type=float, default=30)

	parser.add_argument("--ra_back", help="RA center of background region", type=float, default=-1)
	parser.add_argument("--dec_back", help="Dec center of background region", type=float, default=-1)
	parser.add_argument("--radius", help="radius of regions", type=float, default=120)

	parser.add_argument("--write_baryevtfile", help="write barycentric corrected event files (in lightcurve)",
						action='store_true')

	# parser.add_argument("--pipeline_outdir",
	# 					help='Location of pipeline products (_pipeline will be added) default is equal to outdir',
	# 					type=str, default='outdir')
	parser.add_argument("--repository", help='Location of the repository', type=str,
						default='/gpfs0/ferrigno/NuSTAR/Repository')

	if len(sys.argv) == 1:
		parser.print_help()
		print(help)
		sys.exit(1)

	args = parser.parse_args()

	#repository_location='/gpfs0/ferrigno/NuSTAR/Repository'
	repository_location = args.repository
	if (not os.path.isdir(repository_location)):
		logger.error("The repository location you specified does not exist "+repository_location)
		sys.exit(1)

	PID = os.getpid()
	logger.info("------------------------------------------------------------------------------------------------")
	logger.info(" PID of the process ", PID)
	logger.info(" kill -9 -%d  to kill current proc and children"%PID)
	logger.info("------------------------------------------------------------------------------------------------")

	obsid = args.OBSID[0]
	outdir_base = args.outdir[0]
	ra_src = args.RA[0]
	dec_src = args.Dec[0]
	pipeline_flag = args.pipeline
	lc_flag = args.lightcurve
	spec_flag = args.spec
	ds9_flag = args.no_ds9
	ra_back = args.ra_back
	dec_back = args.dec_back
	radius = args.radius
	write_baryevtfile_flag = args.write_baryevtfile
	filter_evt_flag = args.filter_evt
	t_bin = args.timebin
	e_min = args.eMin
	e_max = args.eMax
	user_gti_file = args.usergti

	out = wrap_process(obsid, ra_src, dec_src, outdir_base, pipeline_flag, spec_flag, lc_flag,
				 ds9_flag, ra_back, dec_back, radius, write_baryevtfile_flag, filter_evt_flag,
				 user_gti_file, repository_location, t_bin, e_min, e_max)

	if out != 0:
		sys.exit(out)

def script_data():
	help = "get_data.py OBSID\n"

	if len(sys.argv) < 2:
		print(help)
		sys.exit(1)

	obsid = sys.argv[1]

	from nustarpipeline import process

	process.get_data(obsid)

if __name__ == "__main__":
	process()

