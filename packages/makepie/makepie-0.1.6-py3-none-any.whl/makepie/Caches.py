import logging, os
from typing import List
from .Exceptions import MakepieException
from .Utils import glob

log = logging.getLogger(__name__)

class FileCache:
	# Accept both path and glob pattern
	def __init__(self, cache_files_globs, dependencies_globs, on_cache):
		self.cache_files_globs = cache_files_globs
		self.dependencies_globs = dependencies_globs
		self.on_cache = on_cache

	@property
	def cache_files(self):
		f = []
		for g in self.cache_files_globs:
			tmp = glob(g)
			log.debug(f"Glob '{g}' found files: {tmp}")
			f.extend(tmp)
		return f

	@property
	def dependencies(self):
		if self.dependencies_globs is None:
			return []
		d = []
		for g in self.dependencies_globs:
			tmp = glob(g)
			log.debug(f"Glob '{g}' found files: {tmp}")
			d.extend(tmp)
		return d

	def get_expiration_time(self, dependencies):
		if len(dependencies) == 0:
			# No expiration
			return 0

		# Get the youngest dependency
		return max(map(os.path.getmtime, dependencies))

	def cached(self):
		log.debug(f"Checking file cache (cache files: {self.cache_files_globs}, dependencies: {self.dependencies_globs})")

		# Check dependencies exist
		dependencies = self.dependencies
		log.debug(f"Found dependencies: {dependencies}")
		if len(dependencies) == 0:
			raise MakepieException(f"Cache dependencies not found")

		# Check file exists
		cache_files = self.cache_files
		log.debug(f"Found cache files: {cache_files}")
		if len(cache_files) == 0:
			log.debug(f"No cache files found, not cached")
			return False
		
		# Check expiration time
		expiration_time = self.get_expiration_time(dependencies)
		# log.debug(f"Datetime: {datetime.datetime.fromtimestamp(expiration_time)}")

		for f in cache_files:
			if os.path.getmtime(f) < expiration_time:
				log.debug(f"Cache file '{f}' is older than dependencies, not cached")
				return False

		return True

	def get_cached_result(self, *args, **kwargs):
		if self.on_cache is None:
			return None
		
		return self.on_cache(*args, **kwargs)
