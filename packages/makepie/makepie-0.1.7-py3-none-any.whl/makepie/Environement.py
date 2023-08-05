DEV = 10
LOC = 11
STA = 20
TES = 21
PRE = 30
PRO = 40

env_aliases = {
	DEV: ["development", "dev"],
	LOC: ["local", "loc"],
	STA: ["staging", "sta", "stag"],
	TES: ["test", "tes", "testing"],
	PRE: ["preproduction", "pre", "preprod"],
	PRO: ["production", "pro", "prod"]
}

class Environment:
	def parse(self, env:str) -> int:
		for code, names in env_aliases.items():
			if env.upper() in names or env.lower() in names:
				return code
		raise ValueError(f"Unknown environment '{env}'")

	def __init__(self, env:str):
		self.code = self.parse(env)				

	@property
	def long(self):
		return env_aliases[self.code][0]

	@property
	def short(self):
		return self.long[:3]

	@property
	def level(self):
		return self.code // 10
		
	def __str__(self):
		return self.long

	def __eq__(self, code: int) -> bool:
		return self.code == code
