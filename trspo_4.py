import concurrent.futures
import time
import matplotlib.pyplot as plt

def collatz_length(n: int) -> int:
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps

def calc_with_buffer(limit: int, workers: int):
    numbers = range(1, limit + 1)
    start = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        values = list(executor.map(collatz_length, numbers, chunksize=5_000))

    elapsed = time.perf_counter() - start
    avg = sum(values) / len(values)
    return elapsed, avg

def calc_streaming(limit: int, workers: int):
    numbers = range(1, limit + 1)
    start = time.perf_counter()

    total = 0
    count = 0

    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        for steps in executor.map(collatz_length, numbers, chunksize=5_000):
            total += steps
            count += 1

    elapsed = time.perf_counter() - start
    avg = total / count
    return elapsed, avg

def main():
    n = 100_000   
    process_counts = [1, 2, 4, 8]

    times_buffer = []
    times_stream = []

    for p in process_counts:
        t_buf, avg_buf = calc_with_buffer(n, p)
        t_stream, avg_stream = calc_streaming(n, p)

        times_buffer.append(t_buf)
        times_stream.append(t_stream)

        print(f"\nКількість процесів: {p}")
        print(f"  Зі списком       : {t_buf:.2f} c (avg = {avg_buf:.2f})")
        print(f"  Потоково (stream): {t_stream:.2f} c (avg = {avg_stream:.2f})")

    plt.figure(figsize=(10, 6))
    plt.plot(process_counts, times_buffer, marker="o", label="Зі списком")
    plt.plot(process_counts, times_stream, marker="s", label="Потоково (stream)")
    plt.xlabel("Кількість процесів")
    plt.ylabel("Час виконання (секунди)")
    plt.title("Порівняння продуктивності реалізацій Коллатца")
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()

# Висновок:
# Було порівняно два підходи до паралельного обчислення послідовностей Коллатца:
# варіант із формуванням списку результатів та стрімінговий варіант без
# проміжних структур. Обидва методи працюють через пул процесів і не
# використовують об’єктів синхронізації.
#
# Час виконання в обох випадках виявився близьким, однак стрімінговий підхід
# споживає менше пам’яті й краще підходить для великих наборів чисел.