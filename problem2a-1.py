from pyspark import SparkContext

def sparkCalculator():
    sc = SparkContext(master = 'local[4]')

    list = sc.textFile("assignment3.dat").map(lambda l: l.split('\t')) \
                   .map(lambda t: float(t[2]))
    
    histogram, bins = list.histogram(10)

    print("Mean: " + str(list.mean()))
    print("Standard Deviation: " + str(list.stdev()))
    print("Minimum Value: " + str(list.min()))
    print("Maximum Value: " + str(list.max()))
    print("Histogram Bins: " + str(bins))
    print("Histogram: " + str(histogram))


if __name__ == "__main__":
    sparkCalculator()
