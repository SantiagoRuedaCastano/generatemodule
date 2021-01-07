package package_value.data

import package_value.data.Parametry._
import package_value.utils.io.ReaderWithAmlib
import com.typesafe.config.Config
import com.typesafe.scalalogging.LazyLogging
import org.apache.spark.sql.{Column, DataFrame, SparkSession}

class GetDataProcess(spark:SparkSession, config: Config) extends LazyLogging {
  lazy val dataFrames = Map(
input_replace
							)

  def getDataFrame(inputPath : String, columns:List[Column]) : DataFrame = new ReaderWithAmlib(spark, config)(inputPath).select(columns:_*)

  def getInputs:Map[String, DataFrame] = dataFrames
}
