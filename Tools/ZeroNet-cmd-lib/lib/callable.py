import sys, inspect

def classAsFunction(cls):
	if not isinstance(cls, type):
		return cls

	class Class(cls):
		def __new__(cls, args):
			instance = super(Callable, cls).__new__(cls)
			return instance.__init__(args)

	return Class

@classAsFunction
class Callable(object):
	class SubCommand(Exception):
		pass
	class Redirect(Exception):
		pass
	class Error(Exception):
		pass

	def __init__(self, args):
		return self.call("", args)

	def call(self, cmd, args):
		cmd = cmd.strip()

		try:
			handler = getattr(self, "action" + "".join(map(lambda part: part[0].upper() + part[1:] if part != "" else "", cmd.split(" "))))
		except AttributeError:
			all_commands = [name[6].lower() + name[7:] for name in dir(self) if name.startswith("action") and len(name) > 6]
			raise Callable.Error("Unknown command '%s'. Allowed commands are: %s" % (cmd, ", ".join(all_commands)))

		self.checkCall(cmd, handler, args)

		try:
			return self.callArgs(handler, args)
		except Callable.SubCommand as e:
			if len(args) == 0:
				raise Callable.Error("'%s' command is not a command but has subcommands." % cmd)

			if len(tuple(e)) == 0:
				# Remove first argument and call it
				return self.call("%s %s" % (cmd, args[0]), args[1:])
			else:
				# Remove first argument and call given command
				return self.call(tuple(e)[0], args[1:])
		except Callable.Redirect as e:
			if len(tuple(e)) == 0:
				# Remove first argument and call it (as SubCommand)
				if len(args) == 0:
					raise Callable.Error("'%s' command is not a command but has subcommands." % cmd)
				return self.call("%s %s" % (cmd, args[0]), args[1:])
			elif len(tuple(e)) == 1:
				# Call given value
				return self.call(tuple(e)[0], args)
			else:
				# Call given value and arguments
				return self.call(tuple(e)[0], tuple(e)[1])

	def checkCall(self, cmd, func, argv):
		import inspect

		expected_args = inspect.getargspec(func).args[1:] # Split "self"
		defaults = inspect.getargspec(func).defaults or tuple()

		if self.checkArgs(cmd, func, argv):
			return True

		if len(defaults) > 0:
			default_args = reversed(zip(reversed(expected_args), reversed(defaults)))
			default_args = map(lambda arg: "%s=%s" % arg, default_args)
			expected_args = expected_args[:-len(default_args)] + default_args

		raise Callable.Error("Allowed arguments: %s" % ", ".join(expected_args))

	def checkArgs(self, cmd, func, argv):
		args, kwargs = self.parseArgs(argv)

		import inspect

		expected_args = inspect.getargspec(func).args[1:] # Split "self"
		varargs = inspect.getargspec(func).varargs
		keywords = inspect.getargspec(func).keywords
		defaults = inspect.getargspec(func).defaults or tuple()

		resulting_args = dict()
		if varargs is not None:
			resulting_args[varargs] = []
		if keywords is not None:
			resulting_args[keywords] = {}

		# Positional arguments
		for cnt, value in enumerate(args):
			if cnt < len(expected_args):
				# Passed just as argument
				resulting_args[expected_args[cnt]] = value
			else:
				# Passed to *args
				if varargs is None:
					raise Callable.Error("Too many positional arguments passed to '%s': expected at most %s, got %s." % (cmd, len(expected_args), len(args)))
				else:
					resulting_args[varargs].append(value)

		# Named arguments
		handled_kwargs = []
		for name, value in kwargs.iteritems():
			if name in handled_kwargs:
				raise Callable.Error("'%s' was passed to '%s' as named argument several times." % (name, cmd))

			handled_kwargs.append(name)

			if name in expected_args:
				# Passed just as argument
				if name in resulting_args:
					raise Callable.Error("'%s' was passed to '%s' as both positional argument and named." % (name, cmd))

				resulting_args[name] = value
			else:
				# Passed to **kwargs
				if keywords is None:
					raise Callable.Error("Unknown named argument '%s' passed to '%s'." % (name, cmd))
				else:
					resulting_args[keywords][name] = value

		# Defaults
		if len(defaults) > 0:
			for cnt, name in enumerate(expected_args[-len(defaults):]):
				if name not in resulting_args:
					resulting_args[name] = defaults[cnt]

		# Check that all the arguments were passed
		for name in expected_args:
			if name not in resulting_args:
				raise Callable.Error("Argument '%s' was not passed to '%s'." % (name, cmd))

		return True

	def parseArgs(self, argv):
		args = []
		kwargs = {}

		kwname = None

		for arg in argv:
			if arg.startswith("--"):
				if kwname is not None:
					kwargs[kwname] = True

				kwname = arg[2:]
			else:
				if kwname is None:
					args.append(arg)
				else:
					kwargs[kwname] = arg
					kwname = None

		if kwname is not None:
			kwargs[kwname] = True

		return args, kwargs

	def callArgs(self, handler, argv):
		args, kwargs = self.parseArgs(argv)
		return handler(*args, **kwargs)

	def action(self, *args, **kwargs):
		raise Callable.SubCommand

class WithHelp(Callable):
	def actionHelp(self, *cmd):
		if cmd in [[], [""], tuple(), ("",)]:
			# Print info about the class
			print inspect.cleandoc(self.__doc__)
			return

		try:
			handler = getattr(self, "action" + "".join(map(lambda part: part[0].upper() + part[1:], cmd)))
			if handler.__doc__ is not None:
				print inspect.cleandoc(handler.__doc__)
				return
		except AttributeError:
			pass

		if cmd == ["help"] or cmd == ("help",):
			# Unable to find info on topic 'help' - no __doc__ in 'help' method or no 'help' method, use default help
			print inspect.cleandoc(self.__doc__)
			return

		print "Unknown topic '%s'" % " ".join(cmd)

Callable.WithHelp = WithHelp