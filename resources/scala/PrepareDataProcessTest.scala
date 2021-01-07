package package_value.data

import package_value.ContextProvider
import package_value.data.Parametry.{LIST_COLS_FILPER, LIST_COLS_FILPRO}
import org.apache.spark.sql.functions.{col, lit}
import org.scalatest.{FlatSpec, Matchers}

class PrepareDataProcessTest extends FlatSpec with Matchers with ContextProvider{

  "1. When apply filRv09" should "get a dataframe with 2 rows" in {
    val dfHdarv009Test = spark.createDataFrame(
      Seq(("000000000001234","000000000001234", "02"), ("000000000001234","000000000123456", "02"),
        ("000000000001234", "000000012345678", "01"), ("000000000001234", "000001234567890", "01")))
      .toDF("contract_product_id", "contract_branch_id", "commercial_product_type")

    val dfReturn = new PrepareDataProcess().filRv09(dfHdarv009Test)
    assert(dfReturn.count() == 2)
    assert(dfReturn.columns.length == 3)
  }

  "2. When apply filPer" should "get a dataframe with 4 rows and 24 columns" in {
    val dfCustomerinformationTest = spark.createDataFrame(
      Seq(("000000000001234","000000000001234", "02"), ("000000000001234","000000000123456", "02"),
        ("000000000001234", "000000012345678", "01"), ("000000000001234", "000001234567890", "01")))
      .toDF("contract_product_id", "contract_branch_id", "commercial_product_type")
      .select(col("commercial_product_type") +: LIST_COLS_FILPER.map(x => lit(x).as(x)):_*)


    val dfReturn = new PrepareDataProcess().filPer(dfCustomerinformationTest)
    assert(dfReturn.count() == 4)
    assert(dfReturn.columns.length == 24)
  }

  "3. When apply filProd" should "get a dataframe with 4 rows and 13 columns" in {
    val dfContractbaseTest = spark.createDataFrame(
      Seq(("000000000001234","000000000001234", "02"), ("000000000001234","000000000123456", "02"),
        ("000000000001234", "000000012345678", "01"), ("000000000001234", "000001234567890", "01")))
      .toDF("contract_product_id", "contract_branch_id", "commercial_product_type")
      .select(col("commercial_product_type") +: LIST_COLS_FILPRO.map(x => lit(x).as(x)):_*)

    val dfReturn = new PrepareDataProcess().filProd(dfContractbaseTest)
    assert(dfReturn.count() == 4)
    assert(dfReturn.columns.length == 13)
  }

  "4. When apply filTrans" should "get a dataframe with 4 rows and 24 columns" in {
    val dfHdamcvrf = spark.createDataFrame(
      Seq(("008","14", "036", "51A", ""),
          ("004","00", "003", "51A", ""),
          ("004","00", "003", "51R", ""))
      ).toDF("transaction_product_id", "transaction_channel_id", "transaction_service_operation_id", "transaction_id", "ben_customer_id")

    val dfReturn = new PrepareDataProcess().filTrans(dfHdamcvrf)
    assert(dfReturn.count() == 1)
    assert(dfReturn.columns.length == 1)
  }

  "5. When apply filNom" should "get a dataframe with 4 rows and 24 columns" in {
    val dfContractbaseTest = spark.createDataFrame(
      Seq(
        ("NO","000000000001234", "000000000001234"),
        ("NO","000000000123456", "000000000001234"),
        ("SI", "000000012345678", "000000000001234"),
        ("SI", "000001234567890", "000000000001234")))
      .toDF("commercial_product_id", "customer_id", "ben_customer_id")

    val dfReturn = new PrepareDataProcess().filNom(dfContractbaseTest)
    assert(dfReturn.count() == 2)
    assert(dfReturn.columns.length == 2)
  }
}
