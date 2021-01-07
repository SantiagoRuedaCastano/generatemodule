package package_value.data

import package_value.data.Parametry._
import org.apache.spark.sql.{Column, DataFrame}

class GenerateModuleName{

  var inputs : Map[String,DataFrame] = _
  case class JoinTable(left:String, right:String, condition:Column, jointype:String, columns:List[Column])

input_replace

  val applyJoin = (join:JoinTable) => getDataFramesByKey(join.left).as("left").join(getDataFramesByKey(join.right).as("right"), join.condition, join.jointype)
      .select(join.columns:_*)

  val getBusinessProcess = (inputs : Map[String, DataFrame]) => {
    this.inputs = inputs
    getDataFramesByKey(???)
  }
}
