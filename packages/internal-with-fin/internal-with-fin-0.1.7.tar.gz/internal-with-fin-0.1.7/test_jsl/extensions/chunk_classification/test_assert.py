import unittest
from pyspark.ml import Pipeline, PipelineModel
from pyspark.sql import SparkSession, DataFrame
from pyspark.ml import Pipeline
from sparknlp import Doc2Chunk
from sparknlp_jsl.annotator import *

import os
import sparknlp_jsl
from test_jsl.extensions.utils import download_file_from_s3

os.environ[
    'SPARK_NLP_LICENSE'] = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJleHAiOjE2ODM2NDg5MjAsImlhdCI6MTY1MjExMjkyMCwidW5pcXVlX2lkIjoiMzkxMmQ0YjQtY2ZiMy0xMWVjLTg5ZTAtZjYwM2ViMGUxMzAzIn0.tF3zTmaQWkqF5_tBrm5eCQnLGC8IFUsccv0c0h6-KdNpYufY8YVrjg7upAieCcBDLBbmA5jtT10YRdOTh0c92st1JSD79ImbL7RzLY4jCbUMThyK5f7JfGb2rsBfr86rw0FnVzsf2icNLVJTLeOf_raRk7jo6QllXgbiHdtP4awnAw6tiuO-6V0z4QzHCE3vcFVe302lLOXxCB1WCcPGGy8fsHdcp58IB8QUodhICVwyY3eMijcvVzN2t26E48bPrT6c3TUT5sJMvaKsVpspu0-n4s_FN12dWaKRTkYj6VHQgI72TP8IVDoMXuxWMNgXG1xQVCe0id7ykDNDi4Rz6A"
os.environ['SECRET'] = "4.0.0-d7cae1bce9e08f46f643ea4da2c5aa5e0d38be09"
os.environ['JSL_VERSION'] = "4.0.0"
os.environ['PUBLIC_VERSION'] = "4.0.0"
os.environ['AWS_ACCESS_KEY_ID'] = "AKIASRWSDKBGDAZEF6C7"
os.environ['AWS_SECRET_ACCESS_KEY'] = "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"
os.environ[
    'SPARK_OCR_LICENSE'] = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJleHAijE2ODM2NDg5MjAsImlhdCI6MTY1MjExMjkyMCwidW5pcXVlX2lkIjoiMzkxMmQ0YjQtY2ZiMy0xMWVjLTg5ZTAtZjYwM2ViMGUxMzAzIn0.tF3zTmaQWkqF5_tBrm5eCQnLGC8IFUsccv0c0h6-KdNpYufY8YVrjg7upAieCcBDLBbmA5jtT10YRdOTh0c92st1JSD79ImbL7RzLY4jCbUMThyK5f7JfGb2rsBfr86rw0FnVzsf2icNLVJTLeOf_raRk7jo6QllXgbiHdtP4awnAw6tiuO-6V0z4QzHCE3vcFVe302lLOXxCB1WCcPGGy8fsHdcp58IB8QUodhICVwyY3eMijcvVzN2t26E48bPrT6c3TUT5sJMvaKsVpspu0-n4s_FN12dWaKRTkYj6VHQgI72TP8IVDoMXuxWMNgXG1xQVCe0id7ykDNDi4Rz6A"
os.environ['SPARK_OCR_SECRET'] = "4.0.0-49cdb09f66ca01a93f959366f0e4a84d1a09b2df"
os.environ['OCR_VERSION'] = "4.0.0"


def get_spark_session():
    jar_base = '/home/ckl/old_home/ckl/Documents/freelance/jsl/jsl_internal_latest69696/lib'
    nlp_jar = jar_base + '/spark-nlp-assembly-4.0.0.jar'
    hc_jar = jar_base + '/spark-nlp-jsl-assembly-4.0.0.jar'
    spark = SparkSession.builder \
        .master("local[*]") \
        .config("spark.driver.memory", "16G") \
        .config("spark.jars", ','.join([nlp_jar, hc_jar])) \
        .getOrCreate()
    return spark


get_spark_session()


class AssertSuite(unittest.TestCase):
    folder = "/assert"
    pipeSavePath = "/home/ckl/old_home/ckl/Documents/freelance/jsl/jsl_internal_latest69696/tmp/trained_models/saving_tests/pipes" + folder
    modelSavePath = "/home/ckl/old_home/ckl/Documents/freelance/jsl/jsl_internal_latest69696/tmp/trained_models/saving_tests/models" + folder
    pretrainedModelSavePath = "/home/ckl/old_home/ckl/Documents/freelance/jsl/jsl_internal_latest69696/tmp/trained_models/by_anno/assert_dl/assertion_dl_healthcare_en_2.7.2_2.4_1611646187271"

    spark = get_spark_session()
    smallCorpus: DataFrame = spark.createDataFrame(
        [["I'm ready!"], ["If I could put into words how much I love waking up at 6 am on Mondays I would."]]).toDF(
        "text")

    def _testPipe(self, pipe: PipelineModel): pipe.transform(self.smallCorpus).select("test_result.result").show()

    def _testSaveAndReloadPipe(self, pipe: PipelineModel) -> PipelineModel:
        pipe.save(self.pipeSavePath)
        reloadedPipe = PipelineModel.load(self.pipeSavePath)
        self._testPipe(reloadedPipe)
        return reloadedPipe

    def buildAndFitAndTest(self, annoToFitAndTest):
        self._testPipe(self.buildAndFit(annoToFitAndTest))

    def buildAndFit(self, annoToFit) -> PipelineModel:
        documentAssembler = DocumentAssembler().setInputCol("text").setOutputCol("document")
        tok = Tokenizer().setInputCols("document").setOutputCol("token")
        POSTag = PerceptronModel.pretrained().setInputCols("document", "token").setOutputCol("pos")
        chunker = Chunker().setInputCols("pos", "document").setOutputCol("chunk").setRegexParsers(["(<NN>)+"])
        emb = WordEmbeddingsModel.load(
            "/home/ckl/cache_pretrained/embeddings_healthcare_100d_en_2.5.0_2.4_1590794626292/").setInputCols("token",
                                                                                                              "document").setOutputCol(
            "emb")
        return Pipeline().setStages([documentAssembler, tok, POSTag, chunker, emb, annoToFit]).fit(self.smallCorpus)

    def test_pretrained_model(self):
        anno_cls_to_test = sparknlp_jsl.finance.AssertionDLModel
        model = anno_cls_to_test.load(self.pretrainedModelSavePath
                                      ).setInputCols("document", "chunk", "emb").setOutputCol("test_result")

        pipelineModel = self.buildAndFit(model)
        self._testPipe(pipelineModel)
        pipelineModel = self._testSaveAndReloadPipe(pipelineModel)

        trainedModel = pipelineModel.stages[5]
        trainedModel.save(self.modelSavePath)
        reloadedModel = anno_cls_to_test.load(self.modelSavePath)
        self.buildAndFitAndTest(reloadedModel)


    def test_model(self):
        # download_file_from_s3(
        #     file_name ='finassertion_competitors',
        #     license='fin',
        #     store_folder = os.getcwd() ,
        # )
        #
        # from sparknlp_jsl.extensions import finance
        # finance.AssertionDLModel.pretrained("finassertion_competitors", "en", "finance/models")
        # RoBertaForSequenceClassification.pretrained("finclf_distilroberta_sentiment_analysis","en", "finance/models")
        from sparknlp_jsl.extensions import finance as fin
        fin.AssertionDLModel.pretrained("finassertion_competitors", "en", "finance/models")

        # fin.BertForSequenceClassification.pretrained("finclf_bert_fls", "en", "finance/models")

if __name__ == '__main__':
    unittest.main()
