__all__ = ['spark_cluster']


def get_spark_session():
    ''' Start a Spark cluster. '''
    try:
        import findspark
        findspark.init()
        
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName('SwifTCR').getOrCreate()

    except (ImportError, ValueError):
        raise('Someting went wrong with the Spark cluster.')
    else:
        return spark


def prepare_rdd(input_strings_rdd):
    input_strings_rdd2 = input_strings_rdd.distinct()
    input_strings_rdd3 = input_strings_rdd2.filter(lambda s: isinstance(s, str) and len(s)>=2)
    return input_strings_rdd3


def hash_keys_rdd(string_rdd):
    hash_rdd = string_rdd.flatMap(lambda s: [(hash(s[:skip]+s[skip+1:])+skip, [s]) for skip in range(len(s))])
    return hash_rdd


def spark_cluster_rdd(substing_key_rdd):
    grouped_rdd = substing_key_rdd.reduceByKey(lambda a,b: a+b)
    cluster_rdd = grouped_rdd.values()
    cluster_rdd2 = cluster_rdd.filter(lambda x: len(x)>1)
    return cluster_rdd2


def spark_cluster(string_list, return_rdd=False, spark=None):
    spark = spark if spark else get_spark_session()
    seq_list_rdd = spark.sparkContext.parallelize(string_list)
    unique_strings_rdd = prepare_rdd(seq_list_rdd)
    substing_keys_rdd = hash_keys_rdd(unique_strings_rdd)
    clusters_rdd = spark_cluster_rdd(substing_keys_rdd)
    return clusters_rdd if return_rdd else clusters_rdd.collect()


def spark_cluster_file(file_path, from_col="aaSeqCDR3", return_rdd=False, spark=None):
    spark = spark if spark else get_spark_session()
    cdr3_col_rdd = (
        spark.read
        .option("header", "true")
        .option("sep", "\t")
        .option("inferSchema", "true")
        .option("emptyValue","")
        .csv(file_path)
        # .load("dbfs:/huge/csv/files/in/this/directory/")
    ).select(from_col).rdd.flatMap(lambda x:x)
    return spark_cluster(cdr3_col_rdd.collect(), return_rdd, spark)