#!/usr/bin/env python

import sys, os, signal as os_signal
import sqlite3, json
from lib.callable import Callable
from lib.args import argv
from lib.config import config
import zeronet_lib.site as Site
import zeronet_lib.user as User
import zeronet_lib.instance as Instance
import zeronet_lib.addresses as Addresses
from zeronet_lib.zerowebsocket import ZeroWebSocket

class ZeroNet(Callable.WithHelp):
	"""
		Commands:
		help                        Print this help
		config                      Get or set config values
		wrapperkey                  Return wrapper key of a site or find a site by wrapper key
		socket                      Send request to ZeroWebSocket
		account                     Configure accounts
		certs                       Configure certificates
		instance                    Get info about ZeroNet instance
		sql                         Run sql query on a database

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

	def actionConfig(self, *args, **kwargs):
		"""
			Get or set config values

			Subcommands:
			config list                 Print list of all saved values as newline-separated values
			config set                  Set config value
			config get                  Get config value
			config remove               Remove config value

			Config variables:
			Name                        Default                 Comment
			server.address              127.0.0.1               The address which will be used for communication with ZeroNet
			server.port                 43110                   ZeroNet port
			server.secure               False                   Sets whether ws/http or wss/https protocol should be used
			account.current             (the first account)     The account chosen by 'account choose' command
			homepage                    (ZeroHello address)     ZeroNet homepage
			root_directory                                      Path to ZeroNet root directory (the one having 'src')
			data_directory              (root_directory)/data   Path to data directory
			zeroname.registry           (ZeroName address)      Domain name registry site
		"""

		raise Callable.SubCommand

	def actionConfigList(self, prefix=""):
		"""
			Print list of all saved values as newline-separated values

			Usage:
			config list                 Print all values
			config list <prefix>        Print all values beginning with <prefix>
		"""

		print "\n".join(filter(lambda name: name.startswith(prefix), config.list()))

	def actionConfigSet(self, name, value):
		"""
			Set config value

			Usage:
			config set <name> <value>   Set config variable <name> to <value>. <name> can be dot-separated.
		"""

		config.set(name, value)

	def actionConfigGet(self, name):
		"""
			Get config value

			Usage:
			config get <name>           Print config variable <name>. <name> can be dot-separated.
		"""

		print config.get(name)

	def actionConfigRemove(self, name):
		"""
			Remove config variable

			Usage:
			config remove <name>        Remove config variable <name>. All the following 'config get' will be rejected.
			                            <name> can be dot-separated.
		"""

		config.remove(name)


	def actionWrapperkey(self, search, reverse=False):
		"""
			Return wrapper key of a site or find a site by wrapper key

			Usage:
			wrapperkey <address>        Print wrapper key of a site by address
			wrapperkey <key> --reverse  Print site address by wrapper key
		"""

		try:
			if reverse == False:
				print Site.getWrapperkey(self.getDataDirectory(), search)
			else:
				print Site.findByWrapperkey(self.getDataDirectory(), search)
		except KeyError as e:
			sys.stderr.write("%s\n" % e[0])
			return 1

	def actionSocket(self, site, cmd, *args, **kwargs):
		"""
			Send request to ZeroWebSocket

			Usage:
			socket <site> <cmd>         Send command without arguments to site <site>
			socket <site> <cmd> 1 2 3   Send command <cmd> with arguments 1, 2 and 3
			socket <site> <cmd> --1 2   Send command <cmd> with arguments 1=2 and 3=True
			                    --3
		"""

		if len(args) > 0 and len(kwargs) > 0:
			sys.stderr.write("ZeroWebSocket doesn't accept requests with both positional arguments and named arguments used.\n")
			return 2

		try:
			with self.connect(site) as ws:
				print unicode(ws.send(cmd, *args, **kwargs)).encode("utf-8")
				return 0
		except ZeroWebSocket.Error as e:
			sys.stderr.write("%s\n" % "\n".join(e))
			return 1


	def actionAccount(self, *args, **kwargs):
		"""
			Configure accounts

			Subcommands:
			account list                Get list of addresses
			account master              Get master_seed of account
			account choose              Choose account for actions
		"""

		raise Callable.SubCommand

	def actionAccountList(self):
		"""
			Get list of addresses

			Usage:
			account list                Print newline-separated list of addresses
		"""

		print "\n".join(User.getUsers(self.getDataDirectory()))

	def actionAccountMaster(self):
		"""
			Get master_seed of account

			Usage:
			account master              Print master_seed of current account
		"""

		address = self.getCurrentAccount()

		try:
			print User.getUser(self.getDataDirectory(), address)["master_seed"]
		except KeyError:
			sys.stderr.write("No account %s\n" % address)
			return 1

	def getCurrentAccount(self):
		address = config.get("account.current", None)

		if address is None:
			address = User.getUsers(self.getDataDirectory())[0]
			config.set("account.current", address)

		return address
	def getCurrentUser(self):
		return User.getUser(self.getDataDirectory(), self.getCurrentAccount())

	def actionAccountChoose(self, address):
		"""
			Choose account for actions

			Usage:
			account choose <address>    Use <address> account for all actions
		"""

		try:
			User.getUser(self.getDataDirectory(), address)
		except KeyError:
			sys.stderr.write("No account %s\n" % address)
			return 1

		config.set("account.current", address)

	def actionCerts(self, *args, **kwargs):
		"""
			Configure certificates

			Subcommands:
			certs list                  Get list of certs
			certs address               Get auth_address of a cert
			certs privatekey            Get auth_privatekey of a cert
			certs username              Get user name of a cert
		"""

		raise Callable.SubCommand

	def actionCertsList(self):
		"""
			Get list of certs

			Usage:
			certs list                  Print newline-separated names of auth certs
		"""

		print "\n".join(self.getCurrentUser()["certs"].keys())

	def actionCertsAddress(self, cert):
		"""
			Get auth_address of a cert

			Usage:
			certs address <cert>        Print auth_address of a certificate
		"""

		certs = self.getCurrentUser()["certs"]

		if cert in certs:
			print certs[cert]["auth_address"]
		else:
			sys.stderr.write("No cert %s\n" % cert)
			return 1

	def actionCertsPrivatekey(self, cert):
		"""
			Get auth_privatekey of a cert

			Usage:
			certs privatekey <cert>     Print auth_privatekey of a certificate
		"""

		certs = self.getCurrentUser()["certs"]

		if cert in certs:
			print certs[cert]["auth_privatekey"]
		else:
			sys.stderr.write("No cert %s\n" % cert)
			return 1

	def actionCertsUsername(self, cert):
		"""
			Get user name of a cert

			Usage:
			certs username <cert>       Print auth_user_name of a certificate
		"""

		certs = self.getCurrentUser()["certs"]

		if cert in certs:
			print certs[cert]["auth_user_name"]
		else:
			sys.stderr.write("No cert %s\n" % cert)
			return 1


	def actionInstance(self, *args, **kwargs):
		"""
			Get info about ZeroNet instance

			Subcommands:
			instance running            Check whether ZeroNet instance is running
			instance pid                Get PID of ZeroNet instance
			instance shutdown           Shutdown ZeroNet instance
			instance start              Start ZeroNet instance
		"""

		raise Callable.SubCommand

	def actionInstanceRunning(self):
		"""
			Check whether ZeroNet instance is running

			Usage:
			instance running            Return 0 if running, 1 otherwise
		"""

		return 1 if Instance.isRunning(self.getDataDirectory()) else 0

	def actionInstancePid(self):
		"""
			Get PID of ZeroNet instance

			Usage:
			instance pid                Return 0 and print the PID if running, return 1 otherwise
		"""

		pid = Instance.getPid(self.getDataDirectory())
		if pid is None:
			return 1
		else:
			print pid
			return 0

	def actionInstanceShutdown(self, force=False, signal=None):
		"""
			Shutdown ZeroNet instance

			Usage:
			instance shutdown           Call ZeroWebSocket for shutdown
			instance shutdown --force   Kill ZeroNet process
			instance shutdown <signal>  Send signal to ZeroNet process
		"""

		if not force and signal is None:
			try:
				with self.connect(config.get("homepage", Addresses.ZeroHello)) as ws:
					try:
						ws.send("serverShutdown")
					except ZeroWebSocket.Error as e:
						pass
			except KeyError as e:
				sys.stderr.write("Could not get wrapper key of ZeroHello. Try 'instance shutdown --force'.\n")
				return 1
		else:
			if signal is None:
				signal = os_signal.SIGINT

			pid = Instance.getPid(self.getDataDirectory())
			if pid is None:
				sys.stderr.write("Could not find ZeroNet process.\n")
				return 1

			os.kill(pid, signal)

	def actionInstanceStart(self):
		Instance.start(config["root_directory"])

	def getDataDirectory(self):
		return config.get("data_directory", "%s/data" % config["root_directory"])

	def actionSql(self, query, site=None):
		"""
			Run sql query on a database

			Usage:
			sql <query>                 Run <query> on content.db
			sql <query> --site <site>   Run <query> on <site>'s database
		"""

		if site is None:
			path = "%s/content.db" % self.getDataDirectory()
		else:
			try:
				with open("%s/%s/content.json" % (self.getDataDirectory(), site), "r") as f:
					pass
			except IOError as e:
				sys.stderr.write("No site %s\n" % site)
				return 1

			try:
				with open("%s/%s/dbschema.json" % (self.getDataDirectory(), site), "r") as f:
					dbschema = json.loads(f.read())
					path = "%s/%s/%s" % (self.getDataDirectory(), site, dbschema["db_file"])
			except IOError as e:
				sys.stderr.write("No database in site %s\n" % site)
				return 1
			except (ValueError, KeyError) as e:
				sys.stderr.write("Malformed dbschema.json\n")
				return 1

		try:
			rows = Site.sqlQuery(path, query)
		except sqlite3.OperationalError as e:
			sys.stderr.write("%s\n" % e)
			return 1

		for row in rows:
			print "\t".join(map(str, row))


	def connect(self, site):
		wrapper_key = Site.getWrapperkey(self.getDataDirectory(), site)

		address = config.get("server.address", "127.0.0.1")
		port = config.get("server.port", "43110")
		secure = config.get("server.secure", False)

		return ZeroWebSocket(wrapper_key, "%s:%s" % (address, port), secure)

try:
	sys.exit(ZeroNet(argv))
except config.AttributeError as e:
	sys.stderr.write("%s\n" % e)
	sys.exit(1)
except Callable.Error as e:
	sys.stderr.write("%s\n" % e)
	sys.exit(2)