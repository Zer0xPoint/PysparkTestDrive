import random

from pyspark.context import xrange

from pyspark.shell import sc

def inside(p):
    x, y = random.random(), random.random()
    return x*x + y*y < 1

count = sc.parallelize(xrange(0, 100000000)) \
             .filter(inside).count()
print ("Pi is roughly %f" % (4.0 * count / 100000000))
