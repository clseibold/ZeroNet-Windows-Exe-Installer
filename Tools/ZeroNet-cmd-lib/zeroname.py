#!/usr/bin/env python

import sys, os, signal as os_signal
import sqlite3, json
from lib.callable import Callable
from lib.args import argv
from lib.config import config
import zeronet_lib.site as Site
import zeronet_lib.addresses as Addresses

class ZeroName(Callable.WithHelp):
	"""
		Commands:
		help                        Print this help
		list                        Print all domains
		resolve                     Get address of a site by its domain
		lookup                      Get site domain(s) by address
		alias                       Find aliases of a domain

		Use 'help <command>' or 'help <command> <subcommand>' for more info
	"""

	def action(self, *args, **kwargs):
		if len(args) == 0:
			if len(kwargs) == 0:
				raise Callable.Redirect("help")
			elif len(kwargs) == 1 and "help" in kwargs:
				raise Callable.SubCommand("help")
			else:
				sys.stderr.write("Why are you passing named arguments to this command? Try 'help' instead.\n")
				return 2
		else:
			raise Callable.SubCommand

	def actionList(self):
		"""
			Print all domains

			Usage:
			list                        Print newline-separated list of domains
		"""

		try:
			print "\n".join(Site.getDomains("%s/%s/data/names.json" % (self.getDataDirectory(), self.getAddress())))
		except KeyError as e:
			sys.stderr.write("%s\n" % e[0])
			return 1

	def actionResolve(self, domain):
		"""
			Get address of a site by its domain

			Usage:
			resolve <domain>            Print address of the site
		"""

		try:
			print Site.findByDomain("%s/%s/data/names.json" % (self.getDataDirectory(), self.getAddress()), domain)
		except KeyError as e:
			sys.stderr.write("%s\n" % e[0])
			return 1

	def actionLookup(self, address):
		"""
			Get site domain(s) by address

			Usage:
			lookup <address>            Print domain(s) of the site
		"""

		try:
			print "\n".join(Site.getDomains("%s/%s/data/names.json" % (self.getDataDirectory(), self.getAddress()), address))
		except KeyError as e:
			sys.stderr.write("%s\n" % e[0])
			return 1

	def actionAlias(self, domain):
		"""
			Find aliases of a domain

			Usage:
			alias <domain>              Print all domains linking to the same domain as <domain>
		"""

		try:
			address = Site.findByDomain("%s/%s/data/names.json" % (self.getDataDirectory(), self.getAddress()), domain)
		except KeyError as e:
			sys.stderr.write("%s\n" % e[0])
			return 1

		try:
			print "\n".join(Site.getDomains("%s/%s/data/names.json" % (self.getDataDirectory(), self.getAddress()), address))
		except KeyError as e:
			sys.stderr.write("%s\n" % e[0])
			return 1

	def getDataDirectory(self):
		return config.get("data_directory", "%s/data" % config["root_directory"])
	def getAddress(self):
		return config.get("zeroname.registry", Addresses.ZeroName)

try:
	sys.exit(ZeroName(argv))
except config.AttributeError as e:
	sys.stderr.write("%s\n" % e)
	sys.exit(1)
except Callable.Error as e:
	sys.stderr.write("%s\n" % e)
	sys.exit(2)