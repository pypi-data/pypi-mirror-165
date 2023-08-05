import requests as re
from pathlib import Path
import json
import time


def cache_factory(cache_dir: str, file_prefix: str, ttl_sec: int):
	def cache(func):
		def wrapper(*args, **kwargs):

			args_params = [str(argv) for argv in args[1:]]
			kwargs_params = [str(argv) for argv in list(kwargs.values())]

			file_sufix = "_".join(args_params + kwargs_params)

			Path(cache_dir).mkdir(parents=True, exist_ok=True)

			cache_file_path = Path(f"{cache_dir}/{file_prefix}_{file_sufix}.json")
			if cache_file_path.is_file():
				
				now = int(time.time())
				created_at = int(cache_file_path.stat().st_mtime)

				if now < created_at + ttl_sec:
					print("Get data from cache")
					with open(cache_file_path, "r") as file:
						return json.loads(file.read())

			print("Get data from source")
			result = func(*args, **kwargs)

			with open(cache_file_path, "w") as file:
				file.write(json.dumps(result, indent=4, ensure_ascii=False))

			return result
		return wrapper
	return cache


class Extractor:

	def __init__(self, **params)-> None:
		self.params = params

	def _get_from_url(self, url: str)-> dict:
		res = re.get(url)
		if res.status_code != 200:
			raise Exception("Status is not 200")

		return res.json()

	def extract(self)-> dict:
		raise Exception("extract method not implemented")