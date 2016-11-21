import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from optparse import OptionParser
import subprocess
import requests


CONFIGURATION = "Release"

# configuration for pgyer
PGYER_UPLOAD_URL = "http://www.pgyer.com/apiv1/app/upload"
DOWNLOAD_BASE_URL = "http://www.pgyer.com"
USER_KEY = "5994aef875878ee001ab35900803da74"
API_KEY = "390700ad2e15a298225e0210161438a3"

def cleanBuildDir(buildDir):
	cleanCmd = "rm -r %s" %(buildDir)
	process = subprocess.Popen(cleanCmd, shell = True)
	process.wait()
	print "cleaned buildDir: %s" %(buildDir)


def parserUploadResult(jsonResult):
	resultCode = jsonResult['code']
	if resultCode == 0:
		downUrl = DOWNLOAD_BASE_URL +"/"+jsonResult['data']['appShortcutUrl']
		print "Upload Success"
		print "DownUrl is:" + downUrl
	else:
		print "Upload Fail!"
		print "Reason:"+jsonResult['message']

def uploadIpaToPgyer(ipaPath):
    print "ipaPath:"+ipaPath
    files = {'file': open(ipaPath, 'rb')}
    headers = {'enctype':'multipart/form-data'}
    payload = {'uKey':USER_KEY,'_api_key':API_KEY,'publishRange':'2','isPublishToPublic':'2'}
    print "uploading...."
    r = requests.post(PGYER_UPLOAD_URL, data = payload ,files=files,headers=headers)
    if r.status_code == requests.codes.ok:
         result = r.json()
         parserUploadResult(result)
    else:
        print 'HTTPError,Code:'+r.status_code

def buildProject(project, scheme, output):
	process = subprocess.Popen("pwd", stdout=subprocess.PIPE)
	(stdoutdata, stderrdata) = process.communicate()

	archiveDir = stdoutdata.strip() + '/Archive/%s.xcarchive' %(scheme)
	print "archiveDir: " + archiveDir
	archiveCmd = 'xcodebuild archive -project %s -scheme %s -configuration %s -archivePath %s' %(project, scheme, CONFIGURATION, archiveDir)
	process = subprocess.Popen(archiveCmd, shell = True)
	process.wait()

	exportArchiveCmd = 'xcodebuild -exportArchive -archivePath %s -exportPath %s -exportFormat IPA' %(archiveDir, output)
	process = subprocess.Popen(exportArchiveCmd, shell=True)
	(stdoutdata, stderrdata) = process.communicate()

	uploadIpaToPgyer(output)
	#cleanBuildDir("./build")

def buildWorkspace(workspace, scheme, output):
	process = subprocess.Popen("pwd", stdout=subprocess.PIPE)
	(stdoutdata, stderrdata) = process.communicate()

	archiveDir = stdoutdata.strip() + '/Archive/%s.xcarchive' %(scheme)
	print "archiveDir: " + archiveDir
	archiveCmd = 'xcodebuild archive -workspace %s -scheme %s -configuration %s -archivePath %s' %(workspace, scheme, CONFIGURATION, archiveDir)
	process = subprocess.Popen(archiveCmd, shell = True)
	process.wait()

	exportArchiveCmd = 'xcodebuild -exportArchive -archivePath %s -exportPath %s -exportFormat IPA' %(archiveDir, output)
	process = subprocess.Popen(exportArchiveCmd, shell=True)
	(stdoutdata, stderrdata) = process.communicate()

	uploadIpaToPgyer(output)
	# cleanBuildDir(buildDir)

def xcbuild(options):
	project = options.project
	workspace = options.workspace
	scheme = options.scheme
	output = options.output

	if project is None and workspace is None:
		pass
	elif project is not None:
		buildProject(project, scheme, output)
	elif workspace is not None:
		buildWorkspace(workspace, scheme, output)

def main():
	
	parser = OptionParser()
	parser.add_option("-w", "--workspace", help="Build the workspace name.xcworkspace.", metavar="name.xcworkspace")
	parser.add_option("-p", "--project", help="Build the project name.xcodeproj.", metavar="name.xcodeproj")
	parser.add_option("-s", "--scheme", help="Build the scheme specified by schemename. Required if building a workspace.", metavar="schemename")
	parser.add_option("-o", "--output", help="specify output filePath+filename", metavar="output_filePath+filename")

	(options, args) = parser.parse_args()

	print "options: %s, args: %s" % (options, args)

	xcbuild(options)

if __name__ == '__main__':
	main()
