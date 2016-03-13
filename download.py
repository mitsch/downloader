#!/usr/bin/python

import sys
import posixpath
import urlparse
import getopt
import urllib
#import urllib.error
import os

def get_file_name_from_url(fileURL):
	urlSplitting = urlparse.urlsplit(fileURL)
	basename = posixpath.basename(urlSplitting.path)
	hostname = urlSplitting.hostname
	if basename:
		return basename
	elif hostname:
		return hostname + "_index.html"
	else:
		return "index.html"

def download_to_disk(sourceURL, targetDirectory, targetFileName=None):
	targetName = get_file_name_from_url(sourceURL)
	targetPath = os.path.join(targetDirectory, targetName)
	try:
		urllib.urlretrieve(sourceURL, targetPath)
		print(sourceURL + " -> " + targetPath)
	except EnvironmentError as err:
		print("error: " + sourceURL + " -> " + targetPath + ": " + err.strerror)


def download_from_file_to_disk(fileName, targetDirectory):
	with open(fileName) as f:
		for line in f:
			download_to_disk(line.rstrip(), targetDirectory)
	# TODO catch exception for not existing fileName or not existing targetDirectory


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
