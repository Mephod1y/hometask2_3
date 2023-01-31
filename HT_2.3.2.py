from time import time
from multiprocessing import Pool, current_process, cpu_count
timer = time()

numbers = [128, 255, 99999, 10651060]

def factorize(numbers):
    all = []
    for num in numbers:
        all.append(div(num))
    return all

def div(num):
    del_n = []
    for i in range(1,num + 1):
        if num % i == 0:
            del_n.append(i)
    return del_n

if __name__ == "__main__":

# 1 variant with function
    a, b, c, d  = factorize(numbers)
    # print(a,b,c,d)
    print(f'Done by function for: {round(time() - timer, 4)}')

# 2 variant with Pool
    print(f"Count CPU: {cpu_count()}")
    with Pool(cpu_count()) as p:
        p.map_async(div, numbers)
        # p.close()
        # p.join()
    print(f'Done by pool for: {round(time() - timer, 4)}')

