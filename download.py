#!/usr/bin/python

import sys
import posixpath
import urlparse
import getopt
import urllib
import os
import string
import re

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

def alternate_existing_file_path(filePath):
	if os.access(filePath, os.F_OK):
		suffixSplitting = string.rsplit(filePath, '.', 1)
		suffix = ("." + suffixSplitting[1]) if len(suffixSplitting) == 2 else ""
		counterSplitting = string.rsplit(suffixSplitting[0], '(', 1)
		count = 1
		if len(counterSplitting) == 2:
			counterMatch = re.match('^(\d+)\)$', counterSplitting[1])
			if counterMatch:
				count = int(counterMatch.group(1)) + 1
		alternatedFilePath = counterSplitting[0] + "(" + str(count) + ")" + suffix
		while os.access(alternatedFilePath, os.F_OK):
			alternatedFilePath = counterSplitting[0] + "(" + str(count) + ")" + suffix
			++count
		return alternatedFilePath
	else:
		return filePath

def download_to_disk(source, target):
	try:
		urllib.urlretrieve(source, target)
		print(source + " -> " + target)
	except EnvironmentError as err:
		print("error: " + source + " -> " + target + ": " + err.strerror)


def download_from_file_to_disk(fileName, targetDirectory, alternate=None):
	with open(fileName) as f:
		for line in f:
			sourceURL = line.rstrip()
			targetName = get_file_name_from_url(sourceURL)
			targetPath = os.path.join(targetDirectory, targetName)
			if alternate:
				targetPath = alternate_existing_file_path(targetPath)
			download_to_disk(sourceURL, targetPath)
	# TODO catch exception for not existing fileName or not existing targetDirectory


def usage():
	print("usage: downloader.py [OPTIONS]... FILE")
	print("Downloads all files with URL in FILE and stores them to the disk")
	print("\nOPTIONS:")
	print("\t-d, --directory=DIRECTORY directory where files will be stored")
	print("\t                          (default is current directory)")
	print("\t-r, --rewrite             already existing files will be replaced")
	print("\t                          (default is creating alternative filename)")
	print("\t-h, --help                prints this information text")

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'd:rh', ["directory=", "rewrite", "help"])
	except getopt.GetoptError as err:
		print str(err)
		usage()
		sys.exit(2)

	# all values to store information from command line
	fileName = None
	targetDirectory = None
	doRewriteFiles = None

	for opt, val in opts:
		if opt in ("-d", "--directory"):
			if targetDirectory:
				print("Too many target directories!")
				usage()
				sys.exit(2)
			else:
				targetDirectory = val
		elif opt in ("-r", "--rewrite"):
			doRewriteFiles = True
		elif opt in ("-h", "--help"):
			usage()
			sys.exit(0)

	# default setting for targetDirectory (empty string instead of None)
	if not targetDirectory:
		targetDirectory = ""

	# So far we only accept one file of urls
	if len(args) == 1:
		fileName = args[0]
	else:
		print("Please give exactly one file of URLs!")
		usage()
		sys.exit(2)

	# let the downloading begin
	download_from_file_to_disk(fileName, targetDirectory, not doRewriteFiles)


if __name__ == "__main__":
	main()
