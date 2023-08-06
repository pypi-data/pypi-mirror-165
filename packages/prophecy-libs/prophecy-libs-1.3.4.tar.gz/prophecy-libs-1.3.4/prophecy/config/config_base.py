
class ConfigBase:
    def updateSpark(self, spark):
        self.spark = spark

    def get_dbutils(self, spark):
        try:
            from pyspark.dbutils import DBUtils
            dbutils = DBUtils(spark)
        except ImportError:
            try:
                import IPython
                dbutils = IPython.get_ipython().user_ns["dbutils"]
            except Exception as e:
                from prophecy.test.utils import ProphecyDBUtil
                dbutils = ProphecyDBUtil

        return dbutils

    def get_int_value(self, value):
        if value is not None:
            return int(value)
        else:
            return value

    def get_float_value(self, value):
        if value is not None:
            return float(value)
        else:
            return value

    def get_bool_value(self, value):
        if value is not None:
            return bool(value)
        else:
            return value