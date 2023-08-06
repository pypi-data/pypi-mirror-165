
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

def spark_read(spark, csv_file, from_col):
    col_rdd = spark.read.load(csv_file, format="csv", sep="\t", inferSchema="true", header="true")\
        .select(from_col)\
        .rdd.flatMap(lambda x:x)
    return col_rdd

def prepare_rdd(input_strings_rdd):
    input_strings_rdd2 = input_strings_rdd.distinct()
    input_strings_rdd3 = input_strings_rdd2.filter(lambda s: isinstance(s, str) and len(s)>=2)
    return input_strings_rdd3


def hash_keys_rdd(string_rdd, edit=False):
    if edit:
        hash_rdd = string_rdd.flatMap(lambda s: [((hash(s[:skip]+s[skip+1:]), skip), [s]) for skip in range(len(s))])
    else:
        hash_rdd = string_rdd.flatMap(lambda s: [(hash(s[:skip]+s[skip+1:]) + skip, [s]) for skip in range(len(s))])
    return hash_rdd


def spark_cluster_rdd(substing_key_rdd):
    grouped_rdd = substing_key_rdd.reduceByKey(lambda a,b: a+b)
    cluster_rdd = grouped_rdd.values()
    cluster_rdd2 = cluster_rdd.filter(lambda x: len(x)>1)
    return cluster_rdd2


def spark_cluster(string_list, return_rdd=False):
    spark = get_spark_session()
    seq_list_rdd = spark.sparkContext.parallelize(string_list)
    unique_strings_rdd = prepare_rdd(seq_list_rdd)
    substing_keys_rdd = hash_keys_rdd(unique_strings_rdd)
    clusters_rdd = spark_cluster_rdd(substing_keys_rdd)
    return clusters_rdd if return_rdd else clusters_rdd.collect()


def spark_cluster_file(csv_file, from_col="aaSeqCDR3", return_rdd=False):
    spark = get_spark_session()
    col_rdd = spark.read.load(csv_file, format="csv", sep="\t", inferSchema="true", header="true").select(from_col).rdd.flatMap(lambda x:x)
    unique_strings_rdd = prepare_rdd(col_rdd)
    substing_keys_rdd = hash_keys_rdd(unique_strings_rdd)
    clusters_rdd = spark_cluster_rdd(substing_keys_rdd)
    return clusters_rdd if return_rdd else clusters_rdd.collect()
