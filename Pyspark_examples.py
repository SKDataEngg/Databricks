# Databricks notebook source
# MAGIC %md
# MAGIC #Pyspark regexp_replace

# COMMAND ----------


from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[1]").appName("SparkByExamples.com").getOrCreate()
address = [(1,"14851 Jeffrey Rd","DE"),
    (2,"43421 Margarita St","NY"),
    (3,"13111 Siemon Ave","CA")]
df =spark.createDataFrame(address,["id","address","state"])
df.show()


# COMMAND ----------


#Replace part of string with another string
from pyspark.sql.functions import regexp_replace
df.withColumn('address', regexp_replace('address', 'Rd', 'Road')) \
  .show(truncate=False)

#+---+------------------+-----+
#|id |address           |state|
#+---+------------------+-----+
#|1  |14851 Jeffrey Road|DE   |
#|2  |43421 Margarita St|NY   |
#|3  |13111 Siemon Ave  |CA   |
#+---+------------------+-

# COMMAND ----------


#Replace string column value conditionally
from pyspark.sql.functions import when
df.withColumn('address', 
    when(df.address.endswith('Rd'),regexp_replace(df.address,'Rd','Road')) \
   .when(df.address.endswith('St'),regexp_replace(df.address,'St','Street')) \
   .when(df.address.endswith('Ave'),regexp_replace(df.address,'Ave','Avenue')) \
   .otherwise(df.address)) \
   .show(truncate=False)

#+---+----------------------+-----+
#|id |address               |state|
#+---+----------------------+-----+
#|1  |14851 Jeffrey Road    |DE   |
#|2  |43421 Margarita Street|NY   |
#|3  |13111 Siemon Avenue   |CA   |
#+---+----------------------+-----+ 


# COMMAND ----------

# MAGIC %md
# MAGIC #partition

# COMMAND ----------


rdd = spark.sparkContext.parallelize((0,20))
print("From local[5]"+str(rdd.getNumPartitions()))

rdd1 = spark.sparkContext.parallelize((0,25), 6)
print("parallelize : "+str(rdd1.getNumPartitions()))

rddFromFile = spark.sparkContext.textFile("src/main/resources/test.txt",10)
print("TextFile : "+str(rddFromFile.getNumPartitions()))


# COMMAND ----------

# MAGIC %md
# MAGIC #joins

# COMMAND ----------


emp = [(1,"Smith",-1,"2018","10","M",3000), \
    (2,"Rose",1,"2010","20","M",4000), \
    (3,"Williams",1,"2010","10","M",1000), \
    (4,"Jones",2,"2005","10","F",2000), \
    (5,"Brown",2,"2010","40","",-1), \
      (6,"Brown",2,"2010","50","",-1) \
  ]
empColumns = ["emp_id","name","superior_emp_id","year_joined", \
       "emp_dept_id","gender","salary"]

empDF = spark.createDataFrame(data=emp, schema = empColumns)
empDF.printSchema()
empDF.show(truncate=False)

dept = [("Finance",10), \
    ("Marketing",20), \
    ("Sales",30), \
    ("IT",40) \
  ]
deptColumns = ["dept_name","dept_id"]
deptDF = spark.createDataFrame(data=dept, schema = deptColumns)
deptDF.printSchema()
deptDF.show(truncate=False)


# COMMAND ----------

# MAGIC %md
# MAGIC ##inner join

# COMMAND ----------

empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"inner") \
     .show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ##fullouter join

# COMMAND ----------


empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"outer") \
    .show(truncate=False)
empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"full") \
    .show(truncate=False)
empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"fullouter") \
    .show(truncate=False)


# COMMAND ----------

# MAGIC %md
# MAGIC ##left outer join

# COMMAND ----------

empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"left") \
    .show(truncate=False)
empDF.join(deptDF, empDF.emp_dept_id == deptDF.dept_id, "leftouter").show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## right outer join

# COMMAND ----------


empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"right") \
   .show(truncate=False)
empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"rightouter") \
   .show(truncate=False)


# COMMAND ----------

# MAGIC %md
# MAGIC #StrucType & Struct Field for nested schema

# COMMAND ----------


import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType

spark = SparkSession.builder.master("local[1]") \
                    .appName('SparkByExamples.com') \
                    .getOrCreate()

data = [("James","","Smith","36636","M",3000),
    ("Michael","Rose","","40288","M",4000),
    ("Robert","","Williams","42114","M",4000),
    ("Maria","Anne","Jones","39192","F",4000),
    ("Jen","Mary","Brown","","F",-1)
  ]

schema = StructType([ \
    StructField("firstname",StringType(),True), \
    StructField("middlename",StringType(),True), \
    StructField("lastname",StringType(),True), \
    StructField("id", StringType(), True), \
    StructField("gender", StringType(), True), \
    StructField("salary", IntegerType(), True) \
  ])
 
df = spark.createDataFrame(data=data,schema=schema)
df.printSchema()
df.show(truncate=False)


# COMMAND ----------

# MAGIC %md
# MAGIC ##nested schema

# COMMAND ----------


structureData = [
    (("James","","Smith"),"36636","M",3100),
    (("Michael","Rose",""),"40288","M",4300),
    (("Robert","","Williams"),"42114","M",1400),
    (("Maria","Anne","Jones"),"39192","F",5500),
    (("Jen","Mary","Brown"),"","F",-1)
  ]
structureSchema = StructType([
        StructField('name', StructType([
             StructField('firstname', StringType(), True),
             StructField('middlename', StringType(), True),
             StructField('lastname', StringType(), True)
             ])),
         StructField('id', StringType(), True),
         StructField('gender', StringType(), True),
         StructField('salary', IntegerType(), True)
         ])

df2 = spark.createDataFrame(data=structureData,schema=structureSchema)
df2.printSchema()
df2.show(truncate=False)


# COMMAND ----------


print(df2.schema.json())


# COMMAND ----------

df.schema.simpleString()

# COMMAND ----------


import json
schemaFromJson = StructType.fromJson(json.loads(schema.json))
df3 = spark.createDataFrame(
        spark.sparkContext.parallelize(structureData),schemaFromJson)
df3.printSchema()


# COMMAND ----------

# MAGIC %md
# MAGIC # WithColumn

# COMMAND ----------


data = [('James','','Smith','1991-04-01','M',3000),
  ('Michael','Rose','','2000-05-19','M',4000),
  ('Robert','','Williams','1978-09-05','M',4000),
  ('Maria','Anne','Jones','1967-12-01','F',4000),
  ('Jen','Mary','Brown','1980-02-17','F',-1)
]

columns = ["firstname","middlename","lastname","dob","gender","salary"]
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()
df = spark.createDataFrame(data=data, schema = columns)


# COMMAND ----------

from pyspark.sql.functions import col
df.withColumn("salary",col("salary").cast("Integer")).show()


# COMMAND ----------


df.withColumn("salary",col("salary")*100).show()



# COMMAND ----------


df.withColumn("CopiedColumn",col("salary")* -1).show()


# COMMAND ----------

from pyspark.sql.functions import lit
df.withColumn("Country", lit("USA")).show()
df.withColumn("Country", lit("USA")) \
  .withColumn("anotherColumn",lit("anotherValue")) \
  .show()


# COMMAND ----------

# MAGIC %md
# MAGIC ##column rename

# COMMAND ----------


df.withColumnRenamed("gender","sex") \
  .show(truncate=False) 


# COMMAND ----------

# MAGIC %md
# MAGIC ## drop columns

# COMMAND ----------

df.drop("salary") \
  .show() 

# COMMAND ----------

# MAGIC %md
# MAGIC #Window fucntions

# COMMAND ----------


spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()

simpleData = (("James", "Sales", 3000), \
    ("Michael", "Sales", 4600),  \
    ("Robert", "Sales", 4100),   \
    ("Maria", "Finance", 3000),  \
    ("James", "Sales", 3000),    \
    ("Scott", "Finance", 3300),  \
    ("Jen", "Finance", 3900),    \
    ("Jeff", "Marketing", 3000), \
    ("Kumar", "Marketing", 2000),\
    ("Saif", "Sales", 4100) \
  )
 
columns= ["employee_name", "department", "salary"]
df = spark.createDataFrame(data = simpleData, schema = columns)
df.printSchema()
df.show(truncate=False)


# COMMAND ----------

# MAGIC %md
# MAGIC ## windowSpec
# MAGIC windowSpec  = Window.partitionBy("department").orderBy("salary")

# COMMAND ----------

# MAGIC %md
# MAGIC ## row_number Window Function

# COMMAND ----------


from pyspark.sql.window import Window
from pyspark.sql.functions import row_number
windowSpec  = Window.partitionBy("department").orderBy("salary")

df.withColumn("row_number",row_number().over(windowSpec)) \
    .show(truncate=False)


# COMMAND ----------

# MAGIC %md
# MAGIC ##rank Window Function

# COMMAND ----------


"""rank"""
from pyspark.sql.functions import rank
df.withColumn("rank",rank().over(windowSpec)) \
    .show()


# COMMAND ----------

# MAGIC %md
# MAGIC ##dense_rank Window Function

# COMMAND ----------

"""dens_rank"""
from pyspark.sql.functions import dense_rank
df.withColumn("dense_rank",dense_rank().over(windowSpec)) \
    .show()

# COMMAND ----------

# MAGIC %md
# MAGIC ##percentile rank function

# COMMAND ----------


""" percent_rank """
from pyspark.sql.functions import percent_rank
df.withColumn("percent_rank",percent_rank().over(windowSpec) * 100) \
    .show()


# COMMAND ----------

# MAGIC %md
# MAGIC ##lag Window Function

# COMMAND ----------


"""lag"""
from pyspark.sql.functions import lag    
df.withColumn("lag",lag("salary",1).over(windowSpec)) \
      .show()


# COMMAND ----------

# MAGIC %md
# MAGIC ##lead Window Function

# COMMAND ----------


 """lead"""
from pyspark.sql.functions import lead    
df.withColumn(if("lead",lead("salary",1).over(windowSpec))) \
    .show()


# COMMAND ----------


