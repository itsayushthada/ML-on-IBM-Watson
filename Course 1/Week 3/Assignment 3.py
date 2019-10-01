
# coding: utf-8

# # Assignment 3
# 
# Welcome to Assignment 3. This will be even more fun. Now we will calculate statistical measures on the test data you have created.
# 
# YOU ARE NOT ALLOWED TO USE ANY OTHER 3RD PARTY LIBRARIES LIKE PANDAS. PLEASE ONLY MODIFY CONTENT INSIDE THE FUNCTION SKELETONS
# Please read why: https://www.coursera.org/learn/exploring-visualizing-iot-data/discussions/weeks/3/threads/skjCbNgeEeapeQ5W6suLkA
# . Just make sure you hit the play button on each cell from top to down. There are seven functions you have to implement. Please also make sure than on each change on a function you hit the play button again on the corresponding cell to make it available to the rest of this notebook.
# Please also make sure to only implement the function bodies and DON'T add any additional code outside functions since this might confuse the autograder.
# 
# So the function below is used to make it easy for you to create a data frame from a cloudant data frame using the so called "DataSource" which is some sort of a plugin which allows ApacheSpark to use different data sources.
# 

# All functions can be implemented using DataFrames, ApacheSparkSQL or RDDs. We are only interested in the result. You are given the reference to the data frame in the "df" parameter and in case you want to use SQL just use the "spark" parameter which is a reference to the global SparkSession object. Finally if you want to use RDDs just use "df.rdd" for obtaining a reference to the underlying RDD object. 
# 
# Let's start with the first function. Please calculate the minimal temperature for the test data set you have created. We've provided a little skeleton for you in case you want to use SQL. You can use this skeleton for all subsequent functions. Everything can be implemented using SQL only if you like.

# In[1]:


from math import sqrt


# In[2]:


def minTemperature(df,spark):
    # return spark.sql("SELECT min(temperature) as mintemp from washing").first().mintemp
    return df.select("temperature").agg({'temperature': 'min'}).collect()[0][0]


# Please now do the same for the mean of the temperature

# In[3]:


def meanTemperature(df,spark):
    return df.select("temperature").agg({'temperature': 'mean'}).collect()[0][0]


# Please now do the same for the maximum of the temperature

# In[4]:


def maxTemperature(df,spark):
    return df.select("temperature").agg({'temperature': 'max'}).collect()[0][0]


# Please now do the same for the standard deviation of the temperature

# In[5]:


def sdTemperature(df,spark):
    return sqrt(df.select("temperature").agg({'temperature': 'variance'}).collect()[0][0])


# Please now do the same for the skew of the temperature. Since the SQL statement for this is a bit more complicated we've provided a skeleton for you. You have to insert custom code at four position in order to make the function work. Alternatively you can also remove everything and implement if on your own. Note that we are making use of two previously defined functions, so please make sure they are correct. Also note that we are making use of python's string formatting capabilitis where the results of the two function calls to "meanTemperature" and "sdTemperature" are inserted at the "%s" symbols in the SQL string.

# In[6]:


def skewTemperature(df,spark): 
    """
    return spark.sql(\"""
SELECT 
    (
        1/##INSERT YOUR CODE HERE##
    ) *
    SUM (
        POWER(##INSERT YOUR CODE HERE##-%s,3)/POWER(%s,3)
    )

as ##INSERT YOUR CODE HERE## from washing
                    \""" %(meanTemperature(df,spark),sdTemperature(df,spark)))##INSERT YOUR CODE HERE##
    """
    
    return df.select("temperature").agg({'temperature': 'skewness'}).collect()[0][0]


# Kurtosis is the 4th statistical moment, so if you are smart you can make use of the code for skew which is the 3rd statistical moment. Actually only two things are different.

# In[7]:


def kurtosisTemperature(df,spark):    
    return df.select("temperature").agg({'temperature': 'kurtosis'}).collect()[0][0]


# Just a hint. This can be solved easily using SQL as well, but as shown in the lecture also using RDDs.

# In[8]:


def correlationTemperatureHardness(df,spark):
    return df.stat.corr("temperature", "hardness")


# ### PLEASE DON'T REMOVE THIS BLOCK - THE FOLLOWING CODE IS NOT GRADED
# #axx
# ### PLEASE DON'T REMOVE THIS BLOCK - THE FOLLOWING CODE IS NOT GRADED

# Now it is time to connect to the object store and read a PARQUET file and create a dataframe out of it. We've created that data for you already. Using SparkSQL you can handle it like a database.

# In[9]:


import ibmos2spark

# @hidden_cell
credentials = {
    'endpoint': 'https://s3-api.us-geo.objectstorage.service.networklayer.com',
    'api_key': 'PUJMZf9PLqN4y-6NUtVlEuq6zFoWhfuecFVMYLBrkxrT',
    'service_id': 'iam-ServiceId-9cd8e66e-3bb4-495a-807a-588692cca4d0',
    'iam_service_endpoint': 'https://iam.bluemix.net/oidc/token'}

configuration_name = 'os_b0f1407510994fd1b793b85137baafb8_configs'
cos = ibmos2spark.CloudObjectStorage(sc, credentials, configuration_name, 'bluemix_cos')

from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
# Since JSON data can be semi-structured and contain additional metadata, it is possible that you might face issues with the DataFrame layout.
# Please read the documentation of 'SparkSession.read()' to learn more about the possibilities to adjust the data loading.
# PySpark documentation: http://spark.apache.org/docs/2.0.2/api/python/pyspark.sql.html#pyspark.sql.DataFrameReader.json

df = spark.read.parquet(cos.url('washing.parquet', 'courseradsnew-donotdelete-pr-1hffrnl2pprwut'))
df.show()


# In[10]:


minTemperature(df,spark)


# In[11]:


meanTemperature(df,spark)


# In[12]:


maxTemperature(df,spark)


# In[13]:


sdTemperature(df,spark)


# In[14]:


skewTemperature(df,spark)


# In[15]:


kurtosisTemperature(df,spark)


# In[16]:


correlationTemperatureHardness(df,spark)


# Congratulations, you are done, please download this notebook as python file using the export function and submit is to the gader using the filename "assignment3.1.py"
