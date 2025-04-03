import threading
import multiprocessing
import time

def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

# обёртка
def run_fib(n):
    fib(n)

# функция для измерения времени выполнения вызвов
def benchmark_sync(n, runs):
    start = time.perf_counter()
    for _ in range(runs):
        run_fib(n)
    end = time.perf_counter()
    return end - start

# функция для измерения времени выполнения потоков
def benchmark_threads(n, runs):
    threads = []
    start = time.perf_counter()
    for _ in range(runs):
        t = threading.Thread(target=run_fib, args=(n,))
        threads.append(t)
        t.start()
    # ожидание завершения потоков
    for t in threads:
        t.join()
    end = time.perf_counter()
    return end - start

# функция для измерения времени выполнения процессов
def benchmark_processes(n, runs):
    processes = []
    start = time.perf_counter()
    for _ in range(runs):
        p = multiprocessing.Process(target=run_fib, args=(n,))
        processes.append(p)
        p.start()
    # ожидание завершения процессов
    for p in processes:
        p.join()
    end = time.perf_counter()
    return end - start

if __name__ == "__main__":
    n = 42
    runs = 10

    sync_time = benchmark_sync(n, runs)
    thread_time = benchmark_threads(n, runs)
    process_time = benchmark_processes(n, runs)

    result_text = (
        f"Fibonacci Benchmark для n = {n} и runs = {runs})\n"
        f"--------------------------------------------\n"
        f"Синхронный запуск:    {sync_time:.2f} сек\n"
        f"Многопоточность:      {thread_time:.2f} сек\n"
        f"Многопроцессность:    {process_time:.2f} сек\n"
    )

    print(result_text)
    with open("4_1_benchmark_result.txt", "w", encoding="utf-8") as f:
        f.write(result_text)
