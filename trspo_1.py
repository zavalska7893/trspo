import threading
import math

def thread_sum():
    total = 0
    for i in range(10):
        total += i
    print(f'[Thread_Sum] Final Sum: {total}')

def thread_factorials():
    print("[Thread_Factorials] Factorials from 1 to 10:")
    for i in range(1, 11):
        print(f'{i}! = {math.factorial(i)}')

if __name__ == "__main__":
    t1 = threading.Thread(target=thread_sum)
    t2 = threading.Thread(target=thread_factorials)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Both threads have finished execution.")