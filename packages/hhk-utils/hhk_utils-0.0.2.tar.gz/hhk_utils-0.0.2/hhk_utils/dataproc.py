#!/usr/bin/env python3
# encoding: utf-8
"""
class and function for process data
"""
import time
import sys
from multiprocessing import Process, JoinableQueue
from threading import Thread
from queue import Queue
from datetime import datetime


class ParallelTask(object):
    """
    a simple parallel framework that reads data from [stdin/file], and writes to [stdout/file] after processing each line 
    with user defined functions. It should be noted that due to the GIL, multi-process is used by default, 
    which is suitable for CPU-intensive tasks; if it is an IO-intensive task, you can consider using multi-threading

    一个简易的并行框架, 实现了从input中读取数据，按照用户func进行处理，完成后写入output
    需要注意，由于GIL, 默认使用多进程，适用于CPU密集任务；如果是IO密集型任务，可以考虑使用多线程
    
    example:
    task = ParallelTask()
    task.regist(func)
    task.run()
    """
    def __init__(self, input_stream=sys.stdin, output_stream=sys.stdout, thread_num=12, use_p=True, log_freq=10000):
        """
        Args:
            input_stream: must have a readline() function. Defaults to sys.stdin.
            output_stream: must have a write function, add newline auto. Defaults to sys.stdout.
            thread_num (int, optional): Defaults to 12.
            log_freq: write processed recoreds to stderr every ${log_freq} recoreds.
        """
        self.input_stream = input_stream
        self.output_stream = output_stream
        self.thread_num = thread_num
        # 是否使用多进程 / use process or not
        self.use_p = use_p
        self.task_size = 2000
        self.output_size = 1000
        self.log_freq = log_freq
        # 特殊字符，用来标识结束 / magic ending label
        self.magic_number = 'hanhengke38a366d18be939d8f01b405445b16258cb1877da'

    def regist(self, func):
        """
        regist user define function. a callabel which mappint str to str.
        if this function return None, write nothing to [stdout|file].

        注册处理函数，func is (str) -> str. 如果返回None, 不写数据
        """
        self.func = func

    def run(self):
        """
        run this task.
        
        任务入口
        """
        def work_process(task_queue, output_queue):
            """
            work process/thread

            工作线程
            """
            while True:
                line = task_queue.get()
                if line == self.magic_number:
                    output_queue.put(self.magic_number)
                else:
                    try:
                        _result = self.func(line)
                        output_queue.put(_result)
                    except Exception as e:
                        sys.stderr.write(f'{e}: {line}\n')
                # do not modify this. / 不要移动这个的顺序 
                task_queue.task_done()
        
        def print_process(task_queue, output_queue):
            """
            output process/thread
            输出线程
            """
            idx = 1
            while True:
                line = output_queue.get()
                if line == self.magic_number:
                    self.output_stream.flush()
                    sys.stderr.write('print process will exit.\n')
                    sys.stderr.flush()
                    output_queue.task_done()

                    # output_queue is not empty, process them. / 不知道为什么，output队列中还有残余，输出出来
                    while not output_queue.empty():
                        line = output_queue.get()
                        self.output_stream.write(f'{line}\n')
                        output_queue.task_done()
                    break

                self.output_stream.write(f'{line}\n')
                output_queue.task_done()
                
                if idx % self.log_freq == 0:
                    self.output_stream.flush()
                    t = time.time()
                    t_str = datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
                    info = f'processed {idx}. task_queue: {task_queue.qsize()}, output_queue: {output_queue.qsize()}'
                    sys.stderr.write(f'{t_str}: {info}\n')
                    sys.stderr.flush()
                idx += 1
        
        task_queue, output_queue = None, None
        if self.use_p:
            # every work process read data from task queue, process it, then send to output queue.
            # 每个工作线程从task_queue里取消息，处理完成后把结果写入output_queue
            task_queue = JoinableQueue(self.task_size)
            # other process/thread, read data from output queue, write to [stdout|file]
            # 一个单独的线程，从output_queue中读取数据，写入标注输出
            output_queue = JoinableQueue(self.output_size)
            for i in range(self.thread_num):
                t = Process(target=work_process, args=(task_queue, output_queue,), daemon=True)
                t.start()
        
            print_thread = Process(target=print_process, args=(task_queue, output_queue,), daemon=True)
            print_thread.start()

        else:
            task_queue = Queue(self.task_size)
            output_queue = Queue(self.output_size)
            for i in range(self.thread_num):
                t = Thread(target=work_process, args=(task_queue, output_queue,), daemon=True)
                t.start()
        
            print_thread = Thread(target=print_process, args=(task_queue, output_queue,), daemon=True)
            print_thread.start()

        line = self.input_stream.readline()
        while line:
            task_queue.put(line)
            line = self.input_stream.readline()
        
        sys.stderr.write('waiting task_queue...\n')
        sys.stderr.flush()
        task_queue.join()
        time.sleep(5)
        # terminate signal
        task_queue.put(self.magic_number)
        task_queue.join()
        sys.stderr.write('waiting output_queue...\n')
        sys.stderr.flush()
        output_queue.join()
        sys.stderr.write('job finish \n')