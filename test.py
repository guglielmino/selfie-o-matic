__author__ = 'fabrizio'

import time

from task_manager import TaskManager
from task_common import TaskBase


class TestTask(TaskBase):
    _iterations = 0
    _is_completed = False

    def execute(self):
        print "Iteration {0}#".format(self._iterations)
        self._iterations = self._iterations + 1
        if self._iterations > 5:
            self._is_completed = True

    def is_async(self):
        return True

    def is_completed(self):
        return self._is_completed


def test_task_manager():
    print "Testing TaskManager...."

    tmanager = TaskManager()
    print "tmanager created"

    testtask = TestTask(None)
    print "task created"

    tmanager.add_task(testtask)
    print "Task added"

    # sleep di 5 sec
    time.sleep(5)

    testtask = TestTask(None)
    print "task re-created"

    tmanager.add_task(testtask)
    print "Task re-added"

    # sleep di 5 sec
    time.sleep(5)


if __name__ == "__main__":
    test_task_manager()


