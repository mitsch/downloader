#!/usr/bin/python

import sys
import posixpath
import urlparse
import getopt
import urllib
import os
import string
import re

# The basename will be deduced from the url. If no basename exists in the url, index.html
# will be returned with a the hostname prepended (if so exists in the url)
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

# An altenation of the file path will be returned, if it already exists. If file path does not
# exist, it will be returned without any alternation. The alternation inserts an additional pattern
# right before the suffix (or at the end, if no suffix exists). A file path with this additio won't
# exist so far.
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
			count = count + 1
			alternatedFilePath = counterSplitting[0] + "(" + str(count) + ")" + suffix
		return alternatedFilePath
	else:
		return filePath

# Some resource (given with an url source) will be downloaded and stored in path target.
def download_to_disk(source, target):
	try:
		urllib.urlretrieve(source, target)
		print(source + " -> " + target)
	except EnvironmentError as err:
		print("error: " + source + " -> " + target + ": " + err.strerror)


# A file at fileName will be read, expecting one url per line. Each url will be downloaded
# to some name in targetDirectory. The name will be deduced with get_file_name_from_url and
# depending on alternate (None->yes, True->no), it will be changed to an non-existing file
# name. No checks will be performed on the existence and readability of fileName or the
# existence and writability of targetDirectory.
def download_from_file_to_disk(fileName, targetDirectory, alternate=None):
	with open(fileName) as f:
		for line in f:
			sourceURL = line.rstrip()
			targetName = get_file_name_from_url(sourceURL)
			targetPath = os.path.join(targetDirectory, targetName)
			if alternate:
				targetPath = alternate_existing_file_path(targetPath)
			download_to_disk(sourceURL, targetPath)


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
				if os.access(val, os.W_OK):
					targetDirectory = val
				else:
					print("Cannot download in directory \"" + val + "\"!")
					sys.exit(2)
		elif opt in ("-r", "--rewrite"):
			doRewriteFiles = True
		elif opt in ("-h", "--help"):
			usage()
			sys.exit(0)

	# default setting for targetDirectory (empty string instead of None)
	if not targetDirectory:
		if os.access("./", os.W_OK):
			targetDirectory = ""
		else:
			print("Cannot download in current directory!")
			sys.exit(2)

	# So far we only accept one file of urls
	if len(args) == 1:
		if os.access(args[0], os.R_OK):
			fileName = args[0]
		else:
			print("Cannot read file \"" + args[0] + "\"!")
			sys.exit(2)
	else:
		print("Please give exactly one file of URLs!")
		usage()
		sys.exit(2)

	# let the downloading begin
	download_from_file_to_disk(fileName, targetDirectory, not doRewriteFiles)


if __name__ == "__main__":
	main()
