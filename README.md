# ATDClient

##### ATDClient.py
Command-line testing tool which submits specified file to ATD and saves a report based on analysis results.
The report is saved to <original_file_name>.atd.<reportType>.
Example:
ATDClient.py -a 10.10.10.10 -u atduser -p atdpass -t pdf -f calc.exe
This will submit calc.exe for analysis and save the respective pdf report to calc.exe.atd.pdf.

Proxy along with optional username/password can be specified through HTTP_PROXY/HTTPS_PROXY environment variable.

The tool uses [atdlib module](https://github.com/passimens/atdlib).
[Executable version](dist/ATDClient.exe) is available in [dist](dist) folder.
[Sample batch file](dist/atdsubmit.cmd) is available in [dist](dist) folder.

##### Command line help

	usage: ATDClient.exe [-h] -a ATDHOST -u USERNAME -p PASSWORD -f FILENAME
											 [-r | -R] [-t {pdf,html,txt,xml,zip,json,ioc,stix}]
											 [-c CMDCHSET]

	ATD Client v.2.1. (c) Valeriy V. Filin (Valerii.Filin@gmail.com), 2016.
	Submits a sample file to ATD and gets the report back.

	optional arguments:
		-h, --help            show this help message and exit
		-a ATDHOST, --atdhost ATDHOST
													ATD hostname or IP to use for file submission.
		-u USERNAME, --username USERNAME
													ATD username to authenticate with.
		-p PASSWORD, --password PASSWORD
													ATD user password to authenticate with.
		-f FILENAME, --filename FILENAME
													Path of a target file to be submitted.
		-r, --reanalyze       Flag: force reanalyze file even if previously scanned
		-R, --no-reanalyze    Flag: no force reanalyze
		-t {pdf,html,txt,xml,zip,json,ioc,stix}, --reptype {pdf,html,txt,xml,zip,json,ioc,stix}
													Report type to be generated. Defaults to pdf.
		-c CMDCHSET, --cmdchset CMDCHSET
													Charset to use when decoding cmd line arguments. Defaults to utf-8. Other options: latin1, cpXXX, cpYYYY, isoXXXX_YY, etc.

	To get detailed analysis report avoid submitting archive files. Proxy along with optional username/password can be specified through HTTPS_PROXY environment variable: e.g. "HTTPS_PROXY=http://bob:P@ssw0rd@10.10.10.10:3128/" or "HTTPS_PROXY=http://10.20.20.20:8080".
