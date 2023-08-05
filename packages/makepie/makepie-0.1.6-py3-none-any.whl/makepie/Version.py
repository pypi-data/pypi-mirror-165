from .Exceptions import MakepieException

class Version:
	def parse(self, version):
		return list(map(int, version.split(self.separator)))

	def __init__(self, ver: str, separator = '.') -> None:
		self.separator = separator
		try:
			self.list = self.parse(ver)
		except Exception as e:
			raise MakepieException(f"Could not parse version") from e

	@property
	def major(self) -> int:
		return self.list[0]

	@property
	def minor(self) -> int:
		return self.list[1]

	@property
	def patch(self) -> int:
		return self.list[2]
	
	def incr(self, index = 0):
		index = -index - 1
		self.list[index] += 1

		for i in range(index + 1, 0):
			self.list[i] = 0
		
		return self

	def __eq__(self, other) -> bool:
		return self.list == other.list

	def __lt__(self, other) -> bool:
		return self.list < other.list

	def __gt__(self, other) -> bool:
		return not self.__lt__(other) and not self.__eq__(other)

	def __ge__(self, other) -> bool:
		return self.__eq__(other) or self.__gt__(other)

	def __le__(self, other) -> bool:
		return self.__eq__(other) or self.__lt__(other)

	def __str__(self) -> str:
		return self.separator.join(map(str, self.list))
