package package_value

import org.apache.spark.SparkContext
import org.apache.spark.sql.{SQLContext, SparkSession}
import org.scalatest.{BeforeAndAfterAll, Suite}

trait ContextProvider extends BeforeAndAfterAll{
  self: Suite =>

  @transient implicit var spark : SparkSession = _

  @transient var sparkContext : SparkContext = _

  @transient var sqlContext : SQLContext = _

  override def beforeAll(): Unit = {
    super.beforeAll()
    spark = SparkSession
      .builder()
      .appName("spark session")
      .master("local[*]")
      .getOrCreate()

    sparkContext = spark.sparkContext
    sqlContext = spark.sqlContext
  }

  override def afterAll(): Unit = {
    super.afterAll()
    if (spark != null) {
      spark.stop()
    }
  }

}

