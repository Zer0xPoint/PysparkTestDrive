from pyspark import SparkContext, SparkConf


def f(x):
    # print x
    list1 = []
    s = len(x[1][0])
    for y in x[1][0]:
        list1.append(tuple((y, x[1][1]/s)))
    # print list
    return list1


if __name__== "__main__":
    conf = SparkConf()
    # conf.setMaster("spark://h-pc:7077")
    conf.setAppName("PageRank")

    # 定义sparkContext
    sc = SparkContext(conf=conf)

    # 原始数据
    list = [('A', ('D',)), ('B', ('A',)), ('C', ('A', 'B')), ('D', ('A', 'C'))]

    # 必须转换成key-values,持久化操作提高效率，partitionBy将相同key的元素哈希到相同的机器上，
    # 省去了后续join操作shuffle开销
    # tuple () 元组
    pages = sc.parallelize(list).map(lambda x: (x[0],  tuple(x[1]))).partitionBy(4).cache()

    # 初始pr值都设置为1
    links = sc.parallelize(['A', 'B', 'C', 'D']).map(lambda x: (x, 1.0))

    # 开始迭代
    for i in range(1, 10):
        # join会把links和page按k合并，如('A',('D',))和('A',1.0) join之后变成 ('A', ('D',1.0))
        # flatMap调用了f函数，并把结果平铺
        rank = pages.join(links).flatMap(f)

        # reduce
        links = rank.reduceByKey(lambda x, y: x+y)

        # 修正
        links = links.mapValues(lambda x: 0.15+0.85*x)


    # links.saveAsTextFile("./pagerank")
    j = links.collect()

    for i in j:
        print (i)
