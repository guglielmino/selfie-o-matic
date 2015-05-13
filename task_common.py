
class TaskFrameProcessorBase(object):
	device_ctx = None

	def __init__(self, ctx):
		self.device_ctx = ctx

	def process_frame(self, frameIm):
		raise NotImplementedError("Method must be implemented from subclass")

	def is_completed(self):
		raise NotImplementedError("Method must be implemented from subclass")
