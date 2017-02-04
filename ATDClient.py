import os
import sys
import hashlib
import time
import socket
import argparse
import atdlib
from atdlib import *

def md5(fname):
    hash = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()

# =================== Main Script Body =====================

parser = argparse.ArgumentParser(
	description='ATD Client v.2.1. (c) Valeriy V. Filin (Valerii.Filin@gmail.com), 2016.\n'
				'Submits a sample file to ATD and gets the report back.',
	epilog='To get detailed analysis report avoid submitting archive files. Proxy along with optional username/password can be specified through HTTPS_PROXY environment variable: e.g. "HTTPS_PROXY=http://bob:P@ssw0rd@10.10.10.10:3128/" or "HTTPS_PROXY=http://10.20.20.20:8080".',
	formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-a', '--atdhost', required=True, help='ATD hostname or IP to use for file submission.')
parser.add_argument('-u', '--username', required=True, help='ATD username to authenticate with.')
parser.add_argument('-p', '--password', required=True, help='ATD user password to authenticate with.')
parser.add_argument('-f', '--filename', required=True, help='Path of a target file to be submitted.')
xgroup = parser.add_mutually_exclusive_group()
xgroup.add_argument('-r', '--reanalyze', dest='reanalyze', action='store_true', help='Flag: force reanalyze file even if previously scanned')
xgroup.add_argument('-R', '--no-reanalyze', dest='reanalyze', action='store_false', help='Flag: no force reanalyze')
parser.add_argument('-t', '--reptype', choices = ['pdf', 'html', 'txt', 'xml', 'zip', 'json', 'ioc', 'stix'], default='pdf', help='Report type to be generated. Defaults to pdf.')
parser.add_argument('-c', '--cmdchset', default='utf-8', help='Charset to use when decoding cmd line arguments. Defaults to utf-8. Other options: latin1, cpXXX, cpYYYY, isoXXXX_YY, etc.')

args = parser.parse_args()

hostname = args.atdhost
username = args.username
password = args.password
filename = args.filename
charset = args.cmdchset
reptype = args.reptype
reanalyze = args.reanalyze if args.reanalyze != None else False

try:
	ufname = unicode(filename, charset)
except:
	print("Invalid charset selected: %s" % charset)
	sys.exit(1)

if not os.path.isfile(ufname):
	print("File %s not found or is not a regular file" % ufname)
	sys.exit(1)

# ------ Get ATD report: ------

atd = atdlib.atdsession()

# --- Authenticate to ATD box: ---

try:
	atd.open(hostname, username, password)
except ATDError as e:
	print(e)
	sys.exit(1)

if not reanalyze :
	# --- Check if file was previously analyzed. Submit if not: ---
	md5s = md5(ufname)

	try:
		res = atd.md5status(md5s)
	except ATDError as e:
		print(e)
		sys.exit(1)

	if res['status'] in (0, 6, 7, 8):
		# No previous submissions, or cancelled (6), or invalid(7), or discarded(8)
		try:
			myip = socket.gethostbyname(socket.gethostname())
		except:
			print("Error getting local IP address. Using blank")
			myip = ''

		try:
			jobId = atd.fileup(ufname, myip)
		except ATDError as e:
			print(e)
			sys.exit(1)
		
		status = 0

	elif 0 < res['status'] <= 5 :
		jobId = res['jobid']
		status = res['status']

	else:
		print("atdstatus returned unexpected result")
		sys.exit(1)

else :
	# --- User chose reanalyze = yes. Submit the file ignoring previous results: ---
	
	try:
		myip = socket.gethostbyname(socket.gethostname())
	except:
		print("Error getting local IP address. Using blank")
		myip = ''

	try:
		jobId = atd.fileup(ufname, myip, True)
	except ATDError as e:
		print(e)
		sys.exit(1)

	status = 0

# --- Wait for file analysis to complete: ---

while status in (0, 2, 3) :

	time.sleep(5)
	try:
		res = atd.jobstatus(jobid=jobId)
	except ATDError as e:
		print(e)
		sys.exit(1)
	
	status = res['status']

# --- Analysis compeleted. Getting tasks list for jobId ---
try:
	tasks = atd.jobtasks(jobId)
except ATDError as e:
	print(e)
	sys.exit(1)

# --- Saving report content for the first file in job ---
try:
	with open(ufname + ".atd." + reptype, "wb") as report:
		report.write(atd.taskreport(taskid=tasks[0], type=reptype))
except ATDError as e:
	print(e)
	sys.exit(1)

atd.close()
