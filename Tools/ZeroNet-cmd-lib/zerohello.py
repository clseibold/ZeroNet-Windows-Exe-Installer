#!/usr/bin/env python

import sys, datetime
from lib.callable import Callable
from lib.args import argv
from lib.config import config
import zeronet_lib.site as Site
import zeronet_lib.addresses as Addresses
from zeronet_lib.zerowebsocket import ZeroWebSocket

class ZeroHello(Callable.WithHelp):
	"""
		Commands:
		help                        Print this help
		site                        Edit or get some info about site
		feed                        Show feed

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

	def actionSite(self, *args, **kwargs):
		"""
			Edit or get some info about site

			Subcommands:
			site pause                  Pause site
			site resume                 Resume site
			site favorites              Manage favorite sites
		"""

		raise Callable.SubCommand

	def actionSitePause(self, address):
		"""
			Pause site

			Usage:
			site pause <address>        Stop seeding <address>
		"""

		try:
			with self.connect(self.getAddress()) as ws:
				ws.send("sitePause", address=address)
		except ZeroWebSocket.Error as e:
			sys.stderr.write("%s\n" % "\n".join(e))
			return 1

	def actionSiteResume(self, address):
		"""
			Resume site

			Usage:
			site resume <address>       Resume seeding <address>
		"""

		try:
			with self.connect(self.getAddress()) as ws:
				ws.send("siteResume", address=address)
		except ZeroWebSocket.Error as e:
			sys.stderr.write("%s\n" % "\n".join(e))
			return 1

	def actionSiteFavorites(self, *args, **kwargs):
		"""
			Manage favorite sites

			Subcommands:
			site favorites list         Get all favorite sites
			site favorites add          Add site to favorites
			site favorites remove       Remove site from favorites
		"""

		raise Callable.SubCommand

	def actionSiteFavoritesList(self):
		"""
			Get all favorite sites

			Usage:
			site favorites list         Print newline-separated favorites
		"""

		try:
			with self.connect(self.getAddress()) as ws:
				settings = ws.send("userGetSettings")
				favorites = settings.get("favorite_sites", {}).keys()
				print "\n".join(favorites)
		except ZeroWebSocket.Error as e:
			sys.stderr.write("%s\n" % "\n".join(e))
			return 1

	def actionSiteFavoritesAdd(self, address):
		"""
			Add site to favorites

			Usage:
			site favorites add          Add <address> to favorite sites
			<address>
		"""

		try:
			with self.connect(self.getAddress()) as ws:
				settings = ws.send("userGetSettings")

				if "favorite_sites" not in settings:
					settings["favorite_sites"] = {}
				settings["favorite_sites"][address] = True

				ws.send("userSetSettings", settings)
		except ZeroWebSocket.Error as e:
			sys.stderr.write("%s\n" % "\n".join(e))
			return 1

	def actionSiteFavoritesRemove(self, address):
		"""
			Remove site from favorites

			Usage:
			site favorites remove       Remove <address> from favorite sites
			<address>
		"""

		try:
			with self.connect(self.getAddress()) as ws:
				settings = ws.send("userGetSettings")

				if "favorite_sites" not in settings:
					settings["favorite_sites"] = {}

				try:
					del settings["favorite_sites"][address]
				except KeyError:
					sys.stderr.write("%s is not in favorites.\n" % address)
					return 1

				ws.send("userSetSettings", settings)
		except ZeroWebSocket.Error as e:
			sys.stderr.write("%s\n" % "\n".join(e))
			return 1

	def actionFeed(self, reverse=False, raw=None):
		"""
			Show feed

			Usage:
			feed                        Display newsfeed
			feed --reverse              Show new posts first
			feed --raw <separator=--->  Use machine-readable format and separate items by <separator>
		"""

		try:
			with self.connect(self.getAddress()) as ws:
				feed = ws.send("feedQuery", 30, 3)

				if "rows" in feed:
					rows = feed["rows"]
				else:
					rows = feed

				if reverse:
					rows.sort(key=lambda row: -row["date_added"])
				else:
					rows.sort(key=lambda row: row["date_added"])

				for row in rows:
					title, body = row["title"], row["body"]
					url, site = row["url"], row["site"]
					feed_type, feed_name = row["type"], row["feed_name"]
					date_added = row["date_added"]

					if raw is None:
						date_added = datetime.datetime.fromtimestamp(date_added)

						print "%s on %s" % (feed_name.encode("utf-8"), date_added.strftime("%Y-%m-%d %H:%M:%S"))
						print "<%s>" % title.encode("utf-8")

						if body:
							print body.encode("utf-8")

						print ""
					else:
						print "%s\t%s\t%s\t%s\t%s\t%s" % tuple(map(lambda s: s.encode("utf-8"), [title, url, site, feed_type, feed_name]) + [date_added])
						print body.encode("utf-8")
						print "---" if raw is True else raw
		except ZeroWebSocket.Error as e:
			sys.stderr.write("%s\n" % "\n".join(e))
			return 1

	def getDataDirectory(self):
		return config.get("data_directory", "%s/data" % config["root_directory"])
	def getAddress(self):
		return config.get("homepage", Addresses.ZeroHello)

	def connect(self, site):
		wrapper_key = Site.getWrapperkey(self.getDataDirectory(), site)

		address = config.get("server.address", "127.0.0.1")
		port = config.get("server.port", "43110")
		secure = config.get("server.secure", False)

		return ZeroWebSocket(wrapper_key, "%s:%s" % (address, port), secure)

try:
	sys.exit(ZeroHello(argv))
except config.AttributeError as e:
	sys.stderr.write("%s\n" % e)
	sys.exit(1)
except Callable.Error as e:
	sys.stderr.write("%s\n" % e)
	sys.exit(2)