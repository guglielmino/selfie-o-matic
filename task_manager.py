# coding=utf-8

# Progetto: Selfie-O-Matic

from threading import Thread
import time

__author__ = "Fabrizio Guglielmino"


class TaskManager(object):

    __tasks = []
    __async_tasks = []
    SCHEDULE_DELAY = 120  # Periodicita' in sec tra un esecuzione schedulata e la successiva

    __scheduled_tasks = []
    __worker = None

    def __init__(self):
        self.__worker = Thread(target=self.__worker_processor, args=())
        self.__worker.setDaemon(True)
        self.__worker.start()

    def add_task(self, task):
        self.__tasks.append(task)

    def add_async_task(self, task):
        self.__async_tasks.append(task)

    def add_scheduled_task(self, task):
        self.__scheduled_tasks.append(task)

    def cycle(self):
        return self.__process(self.__tasks)

    def __process(self, task_list):
        executed = False
        if len(task_list) > 0:
            running_task = task_list[0]
            running_task.execute()

            executed = True

            # Preemptive multitasking
            if running_task.is_completed():
                if running_task.on_completed:
                    running_task.on_completed(self)

                if running_task in self.__tasks:
                    self.__tasks.remove(running_task)

                if running_task in self.__async_tasks:
                    self.__async_tasks.remove(running_task)

        return executed

    def __worker_processor(self):
        last_schedule = time.time()

        while True:
            self.__process(self.__async_tasks)
            diff_time = int(round(time.time() - last_schedule))

            if (diff_time > self.SCHEDULE_DELAY):
                last_schedule = time.time()
                for sched_task in self.__scheduled_tasks:
                    sched_task.execute()

            time.sleep(0.1)
