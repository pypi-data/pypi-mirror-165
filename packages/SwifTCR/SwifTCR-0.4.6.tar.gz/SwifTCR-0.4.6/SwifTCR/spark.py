
def get_spark_session():
    ''' Start a Spark cluster. '''
    try:
        import findspark
        findspark.init()
        
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName('SwifTCR').getOrCreate()

    except (ImportError, ValueError):
        raise('Someting went wrong with the Spark cluster.')

    return spark


def spark_cluster(rdd):
    rdd2 = rdd.flatMap(lambda s: [(hash(s[:skip]+s[skip+1:]) + skip, [s]) for skip in range(len(s))])
    rdd3 = rdd2.reduceByKey(lambda a,b: a+b)
    rdd4 = rdd3.values()
    rdd5 = rdd4.map(set)
    rdd6 = rdd5.filter(lambda c: len(c) > 1)
    return rdd6


def spark_cluster_list(seq_list):
    spark = get_spark_session()
    seq_list_rdd = spark.sparkContext.parallelize(seq_list)
    clusters_rdd = spark_cluster(seq_list_rdd)
    clusters_found = clusters_rdd.collect()
    return clusters_found


def spark_cluster_file(csv_file, from_col="aaSeqCDR3"):
    spark = get_spark_session()
    df = spark.read.load(csv_file, format="csv", sep="\t", inferSchema="true", header="true")
    col_rdd = df.select(from_col).rdd.flatMap(lambda x:x)
    clusters_rdd = spark_cluster(col_rdd)
    clusters_found = clusters_rdd.collect()
    return clusters_found