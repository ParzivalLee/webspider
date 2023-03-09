# start
import time

"""
tasks中应包含'function'键,其值为任务执行的函数
其返回值将作为结果被添加到结果列表中
以及'params'键，其值为任务执行函数所需的参数
"""


class Spider:
    def __init__(self,
                 info={'restTime': 1},
                 tasks=[]):
        self.info = info
        self.tasks = tasks
        self.count = 0
        self.isActive = False

    # 开始执行任务
    def start(self):
        self.isActive = True
        while self.isActive:
            if self.tasks:
                self.count = 0
                # 如果任务列表不为空
                task = self.tasks.pop(0)
                # 从任务列表里获取函数和参数并执行
                task['function'](task['params'])
            else:
                time.sleep(3)
                self.count += 1
                # 若一分钟内没有任务则结束
                if self.count >= 20:
                    self.isActive = False
                    break

    # 停止任务
    def stop(self):
        self.isActive = False
