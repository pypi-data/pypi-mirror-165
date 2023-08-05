from pipeline import Extractor, Transformer, Loader
from cron_converter import Cron
from datetime import datetime
from time import time, sleep


class Pipeline:

	def __init__(self, extractor: Extractor = None, transformer: Transformer = None, loader: Loader = None)-> None:
		self.extractor = extractor
		self.transformer = transformer
		self.loader = loader

	def run_once(self)-> None:
		if self.extractor is None:
			raise Exception("could not find extractor")

		if self.transformer is None:
			raise Exception("could not find transformer")

		if self.loader is None:
			raise Exception("could not find loader")

		self.loader.load(
			self.transformer.transform(
				self.extractor.extract()
			)
		)

	def run_schedule(self, schedule: str)-> None:
		cron = Cron(schedule)
		schedule = cron.schedule()
		while True:
			next_time = str(schedule.next())
			dt = int(datetime.timestamp(datetime.fromisoformat(next_time)))
			now = int(time())
			diff = dt - now
			sleep(diff)
			
			print(f"{datetime.now()}: Running ETL pipeline")
			self.run_once()
