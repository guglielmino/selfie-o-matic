# coding=utf-8

# Progetto: Selfie-O-Matic

import time
from threading import Thread

__author__ = "Fabrizio Guglielmino"

class TaskManager(object):
    
    __tasks = []
    __async_tasks = []
    __worker = None

    def __init__(self):
        self.__worker = Thread(target=self.__worker_processor, args=())
        self.__worker.setDaemon(True)
        self.__worker.start()

    def add_task(self, task):
        self.__tasks.append(task)

    def add_async_task(self, task):
        self.__async_tasks.append(task)

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
        while True:
            self.__process(self.__async_tasks)
            time.sleep(0.1)