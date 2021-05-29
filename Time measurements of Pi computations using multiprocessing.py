#!/usr/bin/env python
# coding: utf-8

# In[78]:


import multiprocessing as mp # See https://docs.python.org/3/library/multiprocessing.html
import argparse # See https://docs.python.org/3/library/argparse.html
import random
import math
import time

def sample_pi(q1,q2,seed):
    random.seed(seed)
    while True:
        s = 0
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1.0:
            s += 1
        q1.put(s)
        q2.put(s)
        
def compute_pi(args):
    start_time = time.time()
    q1 = mp.Manager().Queue()
    q2 = mp.Manager().Queue()
    random.seed(1)
    error = math.pi
    s_total = 0
    n_total = 0
    pi_est = 0
    processes = []
    
    for i in range(args.workers):
        process = mp.Process(target=sample_pi, args=(q1, q2, i))
        processes.append(process)
        process.start()
        
    while error > args.accuracy:
        n_total += 1
        s_total += q1.get()
        pi_est = (4.0*s_total)/n_total
        error=abs(math.pi-pi_est)
    
    for process in processes:
        process.terminate()
        process.join()
    
    time_taken = time.time() - start_time
    
    print("n_total\ts_total\tPi est.\tError\tTime\tSamples_per_second")
    print("%6d\t%7d\t%1.5f\t%1.5f\t%1.5f\t%6d" % (n_total, s_total, pi_est, math.pi-pi_est, time_taken, int(q2.qsize()/time_taken)))
    
    return (q2.qsize()/time_taken)

def time_core(workers, error):
    if __name__ == "__main__":
        parser = argparse.ArgumentParser(description='Compute Pi using Monte Carlo simulation.')
        parser.add_argument('--workers', '-w',
                            default=workers,
                            type = int,
                            help='Number of parallel processes')
        parser.add_argument('--accuracy', '-a',
                            default=error,
                            type = float,
                            help='The accuracy of the Monte Carlo simulation')
        args, unknown = parser.parse_known_args()
        return compute_pi(args)


# In[79]:


import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
def measure_time(error):
    
    cores = [1,2,4,8,16,32]
    samples_per_sec = []
    speedup = []
    
    for k in cores:
        samples_per_sec.append(time_core(k, error))
    
    for i in range(0,len(samples_per_sec)):
        speedup.append(samples_per_sec[i]/samples_per_sec[0])
    
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
    
measure_time(0.0001)


# In[ ]:




