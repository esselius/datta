from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

print("Spark running")


spark.sql("select * from hive_prod.default.pageviews").show()

# spark.sql("drop table hive_prod.default.yolo")
spark.sql("create table if not exists hive_prod.default.yolo (viewtime Int, userid String, pageid String)")

df = spark.readStream.format("iceberg").load("hive_prod.default.pageviews")

def upsertToDelta(microBatchOutputDF, batchId): 
  microBatchOutputDF.createOrReplaceTempView("updates")
  microBatchOutputDF._jdf.sparkSession().sql("""
    MERGE INTO hive_prod.default.yolo t
    USING updates s
    ON s.userid = t.userid AND s.pageid = t.pageid
    WHEN MATCHED THEN UPDATE SET *
    WHEN NOT MATCHED THEN INSERT *
  """)

stream = df.writeStream.format("iceberg").foreachBatch(upsertToDelta).outputMode("update").option("checkpointLocation", "s3a://datalake/spark").start()

stream.awaitTermination()
