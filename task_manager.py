# coding=utf-8

# Progetto: Selfie-O-Matic

import time
from Queue import Queue
from threading import Thread

__author__ = "Fabrizio Guglielmino"

class TaskManager(object):
    __tasks = []
    __worker = None

    def __init__(self):
        self.__worker = Thread(target=self.__worker_processor, args=())
        self.__worker.setDaemon(True)
        self.__worker.start()

    def add_task(self, tasks):
        self.__tasks.append(tasks)


    def __worker_processor(self):
        while True:
            async_tasks = [task for task in self.__tasks if task.is_async()]
            if len(async_tasks) > 0:
                running_task = async_tasks[0]
                running_task.execute()

                if running_task.is_completed():
                    self.__tasks.remove(running_task)

            time.sleep(0.05)
