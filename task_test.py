import time
from task_manager import TaskManager
from task_common import TaskBase

tmanager = TaskManager()

class SharedCtx(object):
    some = ""

class TestAsyncTask(TaskBase):
    _iterations = 0
    _is_completed = False
    _name = ""

    def __init__(self, ctx, name):
        TaskBase.__init__(self, ctx)
        self._name = name

    def execute(self):
        print "{0} -- {1}# ({2})".format(self._name, self._iterations, self.device_ctx.some)
        self._iterations = self._iterations + 1
        if self._iterations > 5:
            self.device_ctx.some = "ASYNC"
            self._is_completed = True

    def is_completed(self):
        return self._is_completed

 
class TestSyncTask(TaskBase):
    _iterations = 0
    _is_completed = False
    _name = ""

    def __init__(self, ctx, name):
        TaskBase.__init__(self, ctx)
        self._name = name

    def execute(self):
        print "{0} -- {1}# ({2})".format(self._name, self._iterations, self.device_ctx.some)
        self._iterations = self._iterations + 1
        if self._iterations > 5:
            self.device_ctx.some = "SYNC"
            self._is_completed = True

    def is_completed(self):
        return self._is_completed


def event(taskmanager):
    print "EVENT"
    context = SharedCtx()
    taskmanager.add_async_task(TestAsyncTask(context, "A\t\tTerzo"))


def test_task_manager():
    print "Testing TaskManager...."
    
    start_time = time.time()
    diff_time = 0

    context = SharedCtx()
    
    tmanager.add_task(TestSyncTask(context, "S\tPrimo"))
    
    secondo = TestSyncTask(context, "S\tSecondo")
    secondo.set_on_completed(event)
    tmanager.add_task(secondo)

    tmanager.add_async_task(TestAsyncTask(context, "A\t\tPrimo"))

    cycle_added = False
    while diff_time < 10:
        tmanager.cycle()
        if diff_time == 6 and not cycle_added:
            print "ADD NEW ASYNC TASK"
            cycle_added = True
            tmanager.add_async_task(TestAsyncTask(context, "A\t\tSecondo"))

        diff_time = int(round(time.time() - start_time))




if __name__ == "__main__":
    test_task_manager()