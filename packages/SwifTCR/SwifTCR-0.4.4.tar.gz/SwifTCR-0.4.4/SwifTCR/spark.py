def spark_cluster(cdr3_list):
    try:
        import findspark
        findspark.init()
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName('SwifTCR').getOrCreate()
    except (ImportError, ValueError):
        raise('Someting went wrong with the Spark cluster.')
    else:
        cdr3 = spark.sparkContext.parallelize(cdr3_list)
        rdd1 = cdr3.filter(lambda s: isinstance(s, str) and len(s) >= 2)
        rdd2 = rdd1.flatMap(lambda s: [((s[:skip]+s[skip+1:], skip), s) for skip in range(len(s)-1, -1, -1)])
        rdd3 = rdd2.groupByKey()
        rdd4 = rdd3.mapValues(set)
        rdd5 = rdd4.filter(lambda c: len(c[1]) > 1)
        rdd6 = rdd5.map(lambda c: list(c[1]))
        clusters_found = rdd6.collect()
        return clusters_found