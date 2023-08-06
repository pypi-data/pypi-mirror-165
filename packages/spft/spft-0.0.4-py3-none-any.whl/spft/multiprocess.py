from tqdm import tqdm
from multiprocessing import Process, Queue, Pool


def worker(input, output):
    for idx, func, data in iter(input.get, 'STOP'):
        result = func(*data)
        output.put((idx, result))


def worker_single(input, output):
    for idx, func, data in iter(input.get, 'STOP'):
        result = func(data)
        output.put((idx, result))


def multi_process(func, iterable, worker_num, is_queue=True):
    """
    :param func: 调用的函数
    :param iterable: 可迭代对象
    :param worker_num: 进程数量
    :param is_queue: 是否使用队列，否使用进程池
    :return: 列表包括每一个任务的结果
    """
    if is_queue:
        results = []

        # Create queues
        task_queue = Queue()
        done_queue = Queue()

        # Submit tasks
        for idx, task in enumerate(iterable):
            task_queue.put((idx, func, task))

        # Start worker processes
        for i in range(worker_num):
            if func.__code__.co_argcount == 1:
                Process(target=worker_single, args=(task_queue, done_queue)).start()
            else:
                Process(target=worker, args=(task_queue, done_queue)).start()

        # get result
        for _ in tqdm(range(len(iterable))):
            results.append(done_queue.get())

        # Tell child processes to stop
        for i in range(worker_num):
            task_queue.put('STOP')

        # the results are unordered, so use original idx to recovery order
        results.sort(key=lambda x: x[0])
        return [x[1] for x in results]
    else:
        if func.__code__.co_argcount == 1:
            with Pool(worker_num) as pool:
                return pool.map(func, iterable)
        else:
            with Pool(worker_num) as pool:
                return pool.starmap(func, iterable)


def multi_process_generator(func, iterable, worker_num):
    """
    :param func: 调用的函数
    :param iterable: 可迭代对象
    :param worker_num: 进程数量
    :param is_queue: 是否使用队列，否使用进程池
    :return: 列表包括每一个任务的结果
    """
    # Create queues
    task_queue = Queue()
    done_queue = Queue()

    # Submit tasks
    for idx, task in enumerate(iterable):
        task_queue.put((idx, func, task))

    # Start worker processes
    for i in range(worker_num):
        if func.__code__.co_argcount == 1:
            Process(target=worker_single, args=(task_queue, done_queue)).start()
        else:
            Process(target=worker, args=(task_queue, done_queue)).start()

    # get result
    for _ in tqdm(iterable):
        yield done_queue.get()

    # Tell child processes to stop
    for i in range(worker_num):
        task_queue.put('STOP')
