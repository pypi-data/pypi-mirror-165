import pandas as pd
from pathlib import Path
from datetime import datetime


def artefact_factory(artefact_dir: str, file_prefix: str, clean_after: bool = False):
	def artefact(func):
		def wrapper(*args, **kwargs):

			if clean_after is True:
				[
					file.unlink() 
					for file in Path(artefact_dir).glob("**/*") 
					if file.is_file()
				]

			Path(artefact_dir).mkdir(parents=True, exist_ok=True)

			now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
			artefact_file_path = Path(f"{artefact_dir}/{file_prefix}_{str(now)}.xlsx")
			
			result : pd.DataFrame = func(*args, **kwargs)
			result.to_excel(artefact_file_path)

			return result
		return wrapper
	return artefact


class Transformer:

	def __init__(self)-> None:
		pass

	def transform(self, data: dict)-> pd.DataFrame:
		raise Exception("transform method not implemented")