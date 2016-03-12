#!/usr/bin/python

import sys
import posixpath
import urlparse
import getopt
import urllib

def get_file_name(fileURL):
	path = urlparse.urlsplit(fileURL).path
	return posixpath.basename(path)

def download_to_disk(sourceURL, targetDirectory, targetFileName=None):
	if targetFileName == None:
		targetFileName = get_file_name(sourceURL)
	try:
		targetFile = urllib.URLopener()
		targetFile.retrieve(sourceURL, targetDirectory + targetFileName)
		print(sourceURL + " -> " + targetFileName + ": ok")
	except IOError as err:
		print(sourceURL + " -> " + targetFileName + ": " + err.strerror)


def download_from_file_to_disk(fileName, targetDirectory):
	with open(fileName) as f:
		for line in f:
			download_to_disk(line, targetDirectory)



def usage():
	print("usage: downloader.py [OPTIONS]... FILE")
	print("Downloads all files with URL in FILE and stores them to the disk")
	print("\nOPTIONS:")
	print("\t-d, --directory=DIRECTORY directory where files will be stored")
	print("\t                          (default is current directory)")

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'd:', ["directory="])
	except getopt.GetoptError as err:
		print str(err)
		usage()
		sys.exit(2)
	#TODO check on opts and args

	fileName = args[0]
	targetDirectory = opts[0].value if len(opts) > 0 else ""
	download_from_file_to_disk(fileName, targetDirectory)



if __name__ == "__main__":
	main()
