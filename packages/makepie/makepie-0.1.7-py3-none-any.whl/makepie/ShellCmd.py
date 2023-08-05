from io import TextIOWrapper
import logging, os, time, sys
from subprocess import PIPE, Popen
from .MakepieLogging import applog
from .Exceptions import MakepieException
from .Config import config

log = logging.getLogger(__name__)

def logdata(data, logger: logging.Logger, name: str):
	if len(data) == 0:
		return

	if not config("PRINT_STREAM_NAME", True):
		logger.info(data)
		return

	# Remove last character if it is a newline
	if data[-1] == "\n":
		data = data[:-1]

	# Insert prefix at the beginning of each line
	prefix = f"{name}> "
	logdata = prefix + data.replace("\n", "\n" + prefix) + "\n"
	logger.info(logdata)
	return data

def log_streams(out: TextIOWrapper, err: TextIOWrapper, logger: logging.Logger):
	outdata = out.read(config("MAX_READ_SIZE", 4096))
	logdata(outdata, logger, "out")

	errdata = err.read(config("MAX_READ_SIZE", 4096))
	logdata(errdata, logger, "err")

	return (outdata, errdata)

# Wait for the process to finish and log its output
# stdin, process stdout & stderr should be set to non-blocking
# Logger should have no terminator
def subprocess_wait_loop(process: Popen, logger: logging.Logger, stdin: str|TextIOWrapper, timeout=None):
	start = time.time()
	outlog = ""
	errlog = ""

	if isinstance(stdin, str):
		process.stdin.write(stdin)
		process.stdin.close()

	# Wait for command to finish/timeout
	while True:
		if (timeout is not None) and (time.time() - start > timeout):
			process.kill()
			process.wait()
			raise MakepieException(f"Command timed out after {timeout} seconds")

		if isinstance(stdin, TextIOWrapper):
			# Copy data from stdin to process stdin
			data = stdin.read(config("MAX_READ_SIZE", 4096))
			if len(data) > 0:
				process.stdin.write(data)

		(outdata, errdata) = log_streams(process.stdout, process.stderr, logger)
		outlog += outdata
		errlog += errdata

		# Exit condition
		if process.poll() is not None:
			process.wait()
			break

		time.sleep(config("POLL_INTERVAL", 0.01))

	# Empty streams
	while True:
		(outdata, errdata) = log_streams(process.stdout, process.stderr, logger)
		outlog += outdata
		errlog += errdata
		if len(outdata) == 0 and len(errdata) == 0:
			break

	return (time.time() - start, outlog, errlog)

def sh(
	cmd: str,
	stdin: str|TextIOWrapper=sys.stdin,
	env=os.environ,
	timeout: float=None,
	throws: bool=True,
):
	# Not implemented for windows
	if os.name == "nt":
		raise MakepieException("Shell commands are not yet implemented on Windows")

	applog.debug(f"shell> {cmd}")

	# Non blocking execution
	proc = Popen(
		cmd,
		shell=True,
		bufsize=1,
		stdin=PIPE,
		stdout=PIPE,
		stderr=PIPE,
		universal_newlines=True,
		env=env
	)

	# Trick to avoid handling newline mess of streams
	previous_val = applog.handlers[0].terminator
	applog.handlers[0].terminator = ""

	# Save blocking state & set PIPES to non-blocking
	(out_no, err_no) = (proc.stdout.fileno(), proc.stderr.fileno())
	(b_out, b_err) = (os.get_blocking(out_no), os.get_blocking(err_no))
	(os.set_blocking(out_no, False), os.set_blocking(err_no, False))
	try:
		in_no = stdin.fileno()
		b_in = os.get_blocking(in_no)
		os.set_blocking(in_no, False)
	except Exception:
		in_no = None

	try:
		(exec_time, outlog, errlog) = subprocess_wait_loop(proc, applog, stdin, timeout)
	finally:
		# Restore old terminator
		applog.handlers[0].terminator = previous_val

		# Restore blocking state
		(os.set_blocking(out_no, b_out), os.set_blocking(err_no, b_err))
		if in_no is not None:
			os.set_blocking(in_no, b_in)

		# Close streams
		proc.stdin.close()
		proc.stdout.close()
		proc.stderr.close()

	# Post execution
	log.info(f"Returned code: {proc.returncode} after {round(exec_time * 1000)} ms")

	if throws and proc.returncode != 0:
		raise MakepieException(f"Command returned error code {proc.returncode}")

	return (proc, outlog, errlog)
