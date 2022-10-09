
class Helper():
	"""All View Prime import this class so that they got the 
	Model Helper class and Backend Apps's View will Use this 
	class attributes through Pirme """

	def __init__(self, arg):
		#super('', self).__init__()
		self.arg = arg

	def unique_custom_id(self, prefix):
		import time
		self.prefix = prefix.upper()
		self.miliTime = int(round(time.time() * 1000))
		self.result = str(self.prefix) + str(self.miliTime)
		return self.result

	def file_processor(self, file, filename, folder):
		import time
		import os
		from django.conf import settings
		from django.core.files.storage import FileSystemStorage

		self.file     = file
		self.filename = filename
		self.random   = str(int(round(time.time() * 1000)))
		self.ext      = os.path.splitext(self.file.name)[1]
		self.folder   = os.path.join(settings.MEDIA_ROOT, folder)

		if self.ext.lower() in ['.jpg', '.jpeg', '.png', '.pdf', '.mp3', '.mp4']:
			self.fileName = self.filename + self.random + self.ext
			fs = FileSystemStorage(location=self.folder)

			if fs.exists(self.fileName):
				fs.delete(self.fileName)

			else:
				self.resultFile = fs.save(self.fileName, self.file)
				return self.fileName
