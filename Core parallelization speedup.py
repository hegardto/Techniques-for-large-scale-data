# -*- coding: utf-8 -*-

# -- Sheet --

import multiprocessing # See https://docs.python.org/3/library/multiprocessing.html
import argparse # See https://docs.python.org/3/library/argparse.html
import random
from math import pi
import time

def sample_pi(n):
    """ Perform n steps of Monte Carlo simulation for estimating Pi/4.
        Returns the number of sucesses."""
    random.seed()
    #print("Hello from a worker")
    s = 0
    for i in range(n):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1.0:
            s += 1
    return s

def compute_pi(args):
    random.seed(1)
    n = int(args.steps / args.workers)
    
    p = multiprocessing.Pool(args.workers)
    
    s = p.map(sample_pi, [n]*args.workers)
    
    n_total = n*args.workers
    s_total = sum(s)
    pi_est = (4.0*s_total)/n_total
    print(" Steps\tSuccess\tPi est.\tError")
    print("%6d\t%7d\t%1.5f\t%1.5f" % (n_total, s_total, pi_est, pi-pi_est))

def time_core(workers, steps):
    start_time = time.time()
    if __name__ == "__main__":
        parser = argparse.ArgumentParser(description='Compute Pi using Monte Carlo simulation.')
        parser.add_argument('--workers', '-w',
                            default=workers,
                            type = int,
                            help='Number of parallel processes')
        parser.add_argument('--steps', '-s',
                            default=steps,
                            type = int,
                            help='Number of steps in the Monte Carlo simulation')
        args, unknown = parser.parse_known_args()
        compute_pi(args)
    return(time.time() - start_time)

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
def measure_time(steps):
    
    cores = [1,2,4,8,16,32]
    times = []
    speedup = []
    
    for k in cores:
        times.append(time_core(k,steps))
    
    for i in range(0,len(times)):
        speedup.append(times[0]/times[i])
    
    print(times)
    
    plt.figure(figsize=(11,10))
    plt.plot(cores, speedup, color = 'blue', label = "Measured speedup")
    plt.plot(cores, cores, color = 'orange', label = "Theoretical speedup")
    plt.legend(loc="upper left")
    plt.xticks(cores)
    plt.xlabel('Number of cores')
    plt.ylabel('Speedup')
    plt.title('Theoretical and measured speedup for different amount of cores')
    plt.grid(True)
    plt.savefig('speedup.png')
    plt.show()
    
measure_time(100000000)

