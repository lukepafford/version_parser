#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
import argparse
import re
import sys
from textwrap import dedent

try:
	import requests
except ImportError:
	print("This script requires the Python requests module")
	raise SystemExit(1)

try:
	from HTMLParser import HTMLParser
except ImportError:
	from html.parser import HTMLParser	

def main():
	argparser = argparse.ArgumentParser(description='Returns a url of the latest software version from a url',
			formatter_class=argparse.RawDescriptionHelpFormatter,	
			epilog=dedent('''
			This program will return the url of the newest version of software available from a url.
			The program will work against software that follows the pattern from the 
			Semantic Version 2.0.0 specification (http://semver.org)

			Ex.
			If you are downloading software from the url https://mysoftware.com/stable
			and the downloadable files have the consistent naming scheme of mysoftware-x.x.x.tar.gz
			then you will provide the following arguments to the script:
			url = 'https://mysoftware.com/stable'
			prefix = 'mysoftware-'
			suffix = '.tar.gz'

			If there were only three versions available (1.0.0, 1.0.1, 1.1.0)
			Then the program would return the following url:
			'https://mysoftware.com/stable/1.1.0'

			The program is designed to provide a dynamic download for tools like curl, or Ansible.
			Note that the output will likely need to be trimmed of newlines 
			by the program that uses these results
			'''))
	argparser.add_argument('url', type=str,
				help='url that contains directory of software downlods')
	argparser.add_argument('prefix', type=str,
				help='part of string before the version number starts')
	argparser.add_argument('suffix', type=str,
				help='part of string after the version number ends')

	args = argparser.parse_args()
	try:
		r = requests.get(args.url)
	except requests.exceptions.ConnectionError:
		print('Failed to connect to {0}'.format(args.url))
		sys.exit(1)

	parser = Latest_Version_Parser(args.prefix, args.suffix)
	parser.feed(r.text)
	if parser.versions:
		sorted_versions = sort_versions(parser.versions)
	else:
		print("No results were returned")
		print("The url must contain software packages with versions of the format")
		print("'[digit]+.[digit]+.[digit]+'")
		sys.exit(1)
	latest_version = '{0}{1}{2}{3}'.format(args.url, args.prefix, sorted_versions[-1], args.suffix)
	print(latest_version)

class Latest_Version_Parser(HTMLParser):
	""" Returns a list of Samba Tarball names """
	def __init__(self, prefix, suffix):
		HTMLParser.__init__(self)
		self.versions = list()
		self.prefix = prefix
		self.suffix = suffix

	def handle_data(self, data):
		pattern = '{0}(\d+\.\d+\.\d+){1}'.format(self.prefix, self.suffix)
		regex = re.compile(pattern)
		found = re.search(regex, data)
		if found:
			self.versions.append(found.group(1))

def sort_versions(versions):
	""" Returns list of sorted
	versions of format x.x.x
	"""
	return sorted(versions, key=(lambda x: list(map(int, x.split('.')))))

main()