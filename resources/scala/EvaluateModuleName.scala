package package_value.process

import package_value.data._
import package_value.data.GlobalParametry._
import package_value.data.Parametry.KPIS_GENERAL_ERROR
import package_value.utils.io.WriterWithAmlib
import com.datio.spark.logger.LazyLogging
import com.typesafe.config.Config
import org.apache.spark.sql.SparkSession

class EvaluateModuleName(spark:SparkSession, config:Config) extends LazyLogging{

  def run(): Int = {
    var exitCode = EXIT_CODE_FAIL_GENERAL
    try {
      val inputs = new GetDataProcess(spark, config).getInputs
      val filters = new PrepareDataProcess().getFilters(inputs)
      val dfFinal = new GenerateModuleName().getBusinessProcess(inputs ++ filters)
      new WriterWithAmlib(config)(dfFinal, Parametry.CONF_ROUTE_OUTPUT)
      exitCode = EXIT_CODE_SUCCESS
    }
    catch{
      case permissionException : org.apache.hadoop.security.AccessControlException =>
        logger.error(s"${KPIS_GENERAL_ERROR} ${EXIT_CODE_FAIL_PERMISSION}", permissionException)
        exitCode = EXIT_CODE_FAIL_PERMISSION
      case e: Exception =>
        logger.error(KPIS_GENERAL_ERROR, e)
    }
    exitCode
  }
}
