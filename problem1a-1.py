from mrjob.job import MRJob
import numpy as np
import time

class Job(MRJob):

    def mapper(self,key,line):
        value=float(line.split()[2])
        yield ('value', (value))

    def combiner(self, key, values):
        numbers = [number for number in values]
        histogram, bins = np.histogram(numbers)

        yield ("max", min(numbers))
        yield ("min", max(numbers))
        yield ("std", np.std(numbers))
        yield ("avg", np.mean(numbers))
        yield ("bins", bins.tolist())
        yield ("hg", histogram.tolist())

    def reducer(self, key, values):
        numbers = [number for number in values]
        histogram, bins = np.histogram(numbers)
        
        if key=='max':
            global max
            max = max(numbers)
            yield ("max", max)
        elif key=='min':
            global min
            min = min(numbers)
            yield ("min", min)
        if key=='std':
            global std
            std = np.std(numbers)
            yield ("std", std)
        elif key=='avg':
            global avg
            avg = np.mean(numbers)
            yield ("avg", avg)
        elif key=='bins':
            yield ("bins", bins.tolist())
        elif key=='hg':
            yield ("hg", histogram.tolist())

if __name__ == '__main__':
    startTime = time.time()
    Job.run()
    endTime = time.time()
    print('Time', endTime-startTime)
