import time
import os
import sys
from datetime import datetime
from glob import glob
from task_manager import TaskManager
from task_common import TaskBase
from config_manager import ConfigManager

tmanager = TaskManager()


class SharedCtx(object):
    some = ""


class TestSchedTask(TaskBase):
    _name = ""
    files_pattern = '/tmp/*.jpg'

    def __init__(self, ctx, name, configManager):
        TaskBase.__init__(self, ctx, configManager)
        self._name = name

    def execute(self):
        print "Executed {0}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        images = glob(self.files_pattern)
        now = time.time()
        for image_file in images:
            if os.stat(image_file).st_mtime < now - 600:
                if os.path.isfile(image_file):
                    print "File would be uploaded {0}".format(image_file)
            else:
                print "File too young"

    def is_completed(self):
        return False


def test_sheduled_tasks():
    print "Testing Scheduled Tasks...."

    context = SharedCtx()
    configManager = ConfigManager('/tmp/selfie-o-matic.cfg')

    task = TestSchedTask(context, "Sched Task", configManager)

    tmanager.add_scheduled_task(task)

    time.sleep(1500)


if __name__ == "__main__":
    test_sheduled_tasks()
