
class TaskFrameProcessorBase(object):

	def init(self):
		raise NotImplementedError("Method must be implemented from subclass")

	def process_frame(self, frameIm):
		raise NotImplementedError("Method must be implemented from subclass")

	def is_completed(self):
		raise NotImplementedError("Method must be implemented from subclass")
