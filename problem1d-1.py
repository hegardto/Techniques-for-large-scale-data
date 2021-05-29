from mrjob.job import MRJob
import numpy as np
import time

class Job(MRJob):

    def mapper_init(self):
        self.group = self.options.group
        
    def mapper(self, _, line):
        row = line.split()
        if int(row[1]) == self.group:
            yield (1, float(row[2]))
        
    def configure_args(self):
        super(Job, self).configure_args()
        self.add_passthru_arg('--group', default = 1, type = int)

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
