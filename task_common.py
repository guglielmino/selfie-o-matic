class TaskBase(object):
    device_ctx = None
    on_completed = None

    def __init__(self, ctx):
        self.device_ctx = ctx

    def execute(self):
        raise NotImplementedError("Method must be implemented from subclass")

    def is_completed(self):
        raise NotImplementedError("Method must be implemented from subclass")

    def set_on_completed(self, on_completed_event):
    	self.on_completed = on_completed_event
