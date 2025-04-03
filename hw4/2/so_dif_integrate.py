import math
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import os

def integrate_chunk(f, a, b, n_iter):
    step = (b - a) / n_iter
    acc = 0.0
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc

def integrate(f, a, b, *, n_jobs=1, n_iter=10000000, executor_type='thread'):
    if executor_type == 'thread':
        Executor = ThreadPoolExecutor
    elif executor_type == 'process':
        Executor = ProcessPoolExecutor
    else:
        raise ValueError("executor_type должен быть 'thread' или 'process'")
    
    # вычисляем число итераций на задачу
    chunk_size = n_iter // n_jobs
    total = 0.0
    
    with Executor(max_workers=n_jobs) as executor:
        futures = []
        for i in range(n_jobs):
            # определяем подотрезок для каждого воркера
            chunk_a = a + i * (b - a) / n_jobs
            chunk_b = a + (i + 1) * (b - a) / n_jobs
            # для последнего воркера учитываем остаток итераций
            current_n_iter = chunk_size if i < n_jobs - 1 else n_iter - chunk_size * (n_jobs - 1)
            futures.append(executor.submit(integrate_chunk, f, chunk_a, chunk_b, current_n_iter))
        
        for future in futures:
            total += future.result()
    
    return total

def benchmark_integration(executor_type, n_jobs, f, a, b, n_iter=10000000):
    start_time = time.time()
    result = integrate(f, a, b, n_jobs=n_jobs, n_iter=n_iter, executor_type=executor_type)
    duration = time.time() - start_time
    return result, duration

def main():
    f = math.cos
    a = 0
    b = math.pi / 2
    n_iter = 10000000
    cpu_count = os.cpu_count() or 1
    max_jobs = cpu_count * 2

    results_thread = []
    results_process = []

    # бенчмарк для ThreadPoolExecutor
    print("ThreadPoolExecutor")
    for n_jobs in range(1, max_jobs + 1):
        _, duration = benchmark_integration('thread', n_jobs, f, a, b, n_iter)
        results_thread.append((n_jobs, duration))
        print(f"n_jobs: {n_jobs}, time: {duration:.4f} секунд")

    # бенчмарк для ProcessPoolExecutor
    print("\nProcessPoolExecutor")
    for n_jobs in range(1, max_jobs + 1):
        _, duration = benchmark_integration('process', n_jobs, f, a, b, n_iter)
        results_process.append((n_jobs, duration))
        print(f"n_jobs: {n_jobs}, time: {duration:.4f} секунд")

    # сохраняем результаты в файл
    with open("4_2_benchmark_results.txt", "w") as file:
        file.write("ThreadPoolExecutor:\n")
        for n_jobs, duration in results_thread:
            file.write(f"n_jobs: {n_jobs}, time: {duration:.4f} секунд\n")
        file.write("\nProcessPoolExecutor:\n")
        for n_jobs, duration in results_process:
            file.write(f"n_jobs: {n_jobs}, time: {duration:.4f} секунд\n")
    print("\nСохранено в 4_2_benchmark_results.txt")

if __name__ == "__main__":
    main()
