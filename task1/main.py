import multiprocessing
import concurrent.futures
import threading
import time

def is_prime(n):
    if n <= 1:
        return 0
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return 0
    return n

res_thread = 0

def is_prime_plus(n):
    global res_thread
    res_thread += is_prime(n)

def sum_primes_multiprocess(N):
    num_cores = multiprocessing.cpu_count()

    pool = multiprocessing.Pool(num_cores)
    
    terms = pool.starmap(is_prime, [(k,) for k in range(N + 1)])

    res = 0

    for term in terms:
        res += term

    return res

def sum_primes_thread(N):
    global res_thread
    num_threads = threading.active_count()
    
    threads = []
    # cool looking loop to go through all numbers while dividing them between threads
    for k in range(num_threads):
        for i in range(k, N + 1, num_threads):
            thread = threading.Thread(target=is_prime_plus, args=(i,))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

    return res_thread

def sum_primes_future(N):
    futures = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for k in range(N + 1):
            futures.append(executor.submit(is_prime, k))

    res = 0
    for future in futures:
        res += future.result()

    return res

if __name__ == '__main__':

    N = 10

    start = time.time()
    res = sum_primes_multiprocess(N)
    end = time.time()

    print("Multiprocess: ", res, end - start)

    start = time.time()
    res = sum_primes_thread(N)
    end = time.time()

    print("Thread: ", res, end - start)

    start = time.time()
    res = sum_primes_future(N)
    end = time.time()

    print("Future: ", res, end - start)

# Multiprocess is almost always the fastest, but it has some needed calculations ,so in small N it is slower than Thread
# Thread speed is depends on the size of N, fastest for small N, but for big N is quite slow
# Future is the slowest, I don't know why, may be because It use only one core in the full capacity

# N = 10
# Multiprocess:  41 0.12917757034301758
# Thread:  41 0.002000093460083008
# Future:  41 0.17601585388183594

# N = 5000
# Multiprocess:  1548136 0.13356351852416992
# Thread:  1548136 0.5799558162689209
# Future:  1548136 1.2958691120147705

# N = 100000 
# Multiprocess:  454396537 0.18842434883117676
# Thread:  454396537 11.674360990524292
# Future:  454396537 21.873854875564575

# https://realpython.com/python-gil/
# seems like Python has a global interpreter lock (GIL), which prevents multiple threads 
# from executing Python bytecode simultaneously, only one thread can execute Python code at a time. 