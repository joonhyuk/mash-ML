import math
from multiprocessing import Process, Queue, cpu_count
import time

NUM_THREADS = cpu_count()
START, END = 1, 100000000

def work(id, start, end, result:Queue):
    total = 0
    for i in range(start, end):
        total += math.log(float(i))
    result.put(total)
    return

if __name__ == "__main__":
    perf_time = time.perf_counter()
    result = Queue()
    th = Process(target = work, args = (0, START, END, result))
    th.start()
    th.join()
    print(f'single processing result : {result.get()}')
    print(f'single processing time : {time.perf_counter() - perf_time} seconds')
    
    perf_time = time.perf_counter()
    result = Queue()
    threads_list = []
    
    chunk, left = divmod((END - START), NUM_THREADS)
    
    for i in range(NUM_THREADS - 1):
        threads_list.append(Process(target = work, args = (i, START + chunk * i, START + chunk * (i + 1), result)))
    threads_list.append(Process(target = work, args = (i, START + chunk * (NUM_THREADS - 1), END, result)))
    
    for th in threads_list:
        th.start()
    for th in threads_list:
        th.join()

    result.put('STOP')
    total = 0
    while True:
        tmp = result.get()
        if tmp == 'STOP':
            break
        else:
            total += tmp
    print(f"multi processing result : {total}")
    print(f'multi processing time : {time.perf_counter() - perf_time} seconds')