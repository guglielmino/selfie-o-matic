class TaskBase(object):
    device_ctx = None
    config_manager = None
    on_completed = None

    def __init__(self, ctx, configManager):
        self.device_ctx = ctx
        self.config_manager = configManager

    def execute(self):
        raise NotImplementedError(
            "Method 'execute' must be implemented from subclass")

    def is_completed(self):
        raise NotImplementedError(
            "Method 'is_completed' must be implemented from subclass")

    def set_on_completed(self, on_completed_event):
        self.on_completed = on_completed_event
