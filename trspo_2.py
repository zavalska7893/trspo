import random
import math
import time
import threading
import multiprocessing as mp
import matplotlib.pyplot as plt


def count_pi(n):
    """
    Рахує кількість точок, що потрапили в коло,
    з n випадкових точок у квадраті [-1;1] x [-1;1].
    """
    counter = 0
    for _ in range(n):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x * x + y * y <= 1:
            counter += 1
    return counter


def threading_pi(n, number_of_threads):
    """
    Обчислення π методом Монте-Карло з використанням потоків.
    Не використовуються ніякі методи синхронізації, окрім join().
    """
    start = time.time()

    points_per_thread = n // number_of_threads
    remainder = n % number_of_threads  # щоб сумарно було рівно n точок

    results = [0] * number_of_threads
    threads = []

    def worker(idx, n_points):
        results[idx] = count_pi(n_points)

    for i in range(number_of_threads):
        # роздаємо "зайві" точки першим потокам
        n_points = points_per_thread + (1 if i < remainder else 0)
        t = threading.Thread(target=worker, args=(i, n_points))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    total = sum(results)
    pi = 4 * total / n
    end = time.time()
    return {"pi": pi, "time": end - start}


def multiprocessing_pi(n, number_of_processes):
    """
    Обчислення π методом Монте-Карло з використанням multiprocessing.
    Кожен процес отримує свою частину точок і працює паралельно на окремому ядрі.
    """
    start = time.time()

    points_per_process = n // number_of_processes
    remainder = n % number_of_processes

    points_list = [points_per_process] * number_of_processes
    for i in range(remainder):
        points_list[i] += 1

    with mp.Pool(number_of_processes) as pool:
        results = pool.map(count_pi, points_list)

    total = sum(results)
    pi = 4 * total / n
    end = time.time()
    return {"pi": pi, "time": end - start}


def plot_results(x, y1, y2):
    plt.plot(x, y1, marker="o", label="Threading")
    plt.plot(x, y2, marker="o", label="Multiprocessing")
    plt.xlabel("Number of Threads/Processes")
    plt.ylabel("Time (seconds)")
    plt.title("Monte Carlo π Estimation")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    N = 10_000_000
    counts = (1, 2, 4, 8, 16, 32, 64)

    times_thread = []
    times_process = []

    print(f"Target value: {math.pi}\n")

    for c in counts:
        # threading
        t_res = threading_pi(N, c)
        times_thread.append(t_res["time"])

        # multiprocessing (не більше, ніж кількість ядер)
        proc_num = c if c <= mp.cpu_count() else mp.cpu_count()
        p_res = multiprocessing_pi(N, proc_num)
        times_process.append(p_res["time"])

        print(f"Threads   {c:2d}: pi={t_res['pi']:.6f}, time={t_res['time']:.4f} sec")
        print(f"Processes {proc_num:2d}: pi={p_res['pi']:.6f}, time={p_res['time']:.4f} sec\n")

    plot_results(counts, times_thread, times_process)

# Висновок:
# Експерименти з обчисленням числа π на 10 000 000 точок показали, що
# використання потоків (threading) не дає помітного прискорення для
# CPU-навантаженої задачі через обмеження GIL у CPython, а час може
# навіть зростати зі збільшенням кількості потоків.
# Натомість multiprocessing дозволяє задіяти кілька ядер процесора,
# тому до кількості фізичних ядер спостерігається реальне прискорення
# виконання розрахунків.
