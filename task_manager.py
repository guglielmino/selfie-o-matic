# coding=utf-8

# Progetto: Selfie-O-Matic

import time
import schedule
import logging

__author__ = "Fabrizio Guglielmino"


class TaskManager(object):
    __tasks = []
    SCHEDULE_DELAY = 60  # Periodicita' in sec tra un esecuzione schedulata e la successiva
    __scheduled_tasks = []

    def __init__(self):
        schedule.every(self.SCHEDULE_DELAY).seconds.do(self.__time_scheduled)

    def add_task(self, task):
        self.__tasks.append(task)

    def add_scheduled_task(self, task):
        self.__scheduled_tasks.append(task)

    def cycle(self):
        schedule.run_pending()
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

        return executed

    def __time_scheduled(self):
        logging.debug("-- RUNNING __time_scheduled")
        for sched_task in self.__scheduled_tasks:
            sched_task.execute()
