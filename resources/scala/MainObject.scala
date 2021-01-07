package package_value

import package_value.data.GlobalParametry._
import package_value.data.Parametry._
import package_value.process.EvaluateSegmentationBase
import com.datio.spark.InitSpark
import com.datio.spark.metric.model.BusinessInformation
import com.typesafe.config.Config
import org.apache.spark.sql.SparkSession

protected trait MainObjectTrait extends InitSpark {
  this: InitSpark =>

  override def runProcess(spark: SparkSession, config: Config): Int = {
    logger.info("Init process MainObject")
    var exitCode = EXIT_CODE_FAIL_GENERAL
    val evaluate = new EvaluateMainObject(spark, config)
    exitCode = evaluate.run()
    exitCode
  }

  override def defineBusinessInfo(config: Config): BusinessInformation =
    BusinessInformation(exitCode = NUMBER_ZERO, entity = PARAM_EMPTY, path = PARAM_EMPTY, mode = PARAM_EMPTY,
      schema = PARAM_EMPTY, schemaVersion = PARAM_EMPTY, reprocessing = PARAM_EMPTY)
}
object MainObject extends MainObjectTrait with InitSpark
