import sparknlp_jsl
import unittest
from pyspark.ml import Pipeline, PipelineModel
from pyspark.sql import SparkSession, DataFrame
from pyspark.ml import Pipeline
from sparknlp import Doc2Chunk
from sparknlp_jsl.annotator import *
import os
import nlu

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


import nlu

get_spark_session()


class SentenceResolveSuite(unittest.TestCase):
    spark = get_spark_session()
    work_folder = '/home/ckl/old_home/ckl/Documents/freelance/jsl/jsl_internal_latest69696/tmp/trained_models/'
    pipeSavePath = "/home/ckl/old_home/ckl/Documents/freelance/jsl/jsl_internal_latest69696/tmp/trained_models/FinPipe"
    folder = "/resolveApproach"
    pipeSavePath = "/home/ckl/old_home/ckl/Documents/freelance/jsl/jsl_internal_latest69696/tmp/trained_models/saving_tests/pipes" + folder
    modelSavePath = "/home/ckl/old_home/ckl/Documents/freelance/jsl/jsl_internal_latest69696/tmp/trained_models/saving_tests/models" + folder

    pretrainedModelSavePath = "/home/ckl/old_home/ckl/Documents/freelance/jsl/jsl_internal_latest69696/tmp/trained_models/by_anno/resolver/sbiobertresolve_mesh_en_3.3.2_2.4_1642534218495"
    data = spark.read.load("../src/test/resources/resolution/snomed_100.parquet")

    def _testPipe(self, pipe: PipelineModel): pipe.transform(self.data).select("test_result.result").show()

    def _testSaveAndReloadPipe(self, pipe: PipelineModel) -> PipelineModel:
        pipe.save(self.pipeSavePath)
        reloadedPipe = PipelineModel.load(self.pipeSavePath)
        self._testPipe(reloadedPipe)
        return reloadedPipe

    def buildAndFitAndTest(self, annoToFitAndTest):
        self._testPipe(self.buildAndFit(annoToFitAndTest))

    def buildAndFit(self, annoToFit) -> PipelineModel:
        # create a basic pipeline for annoToFit and return the fitted pipeModel
        document = DocumentAssembler().setInputCol("description").setOutputCol("document")
        doc2chunk = Doc2Chunk().setInputCols("document").setOutputCol("chunk")
        token = Tokenizer().setInputCols("document").setOutputCol("token")
        bertEmbeddings = BertSentenceEmbeddings.pretrained().setInputCols("document").setOutputCol("bert_embeddings")
        return Pipeline().setStages(
            [document, doc2chunk, token, bertEmbeddings,  annoToFit]).fit(self.data)

    def test_pretrained_model(self):
        model = sparknlp_jsl.extensions.finance.SentenceEntityResolverApproach() \
            .setNeighbours(100) \
            .setThreshold(1000) \
            .setInputCols("bert_embeddings") \
            .setNormalizedCol("description_normalized") \
            .setLabelCol("code") \
            .setOutputCol("test_result") \
            .setDistanceFunction("EUCLIDEAN") \
            .setCaseSensitive(False)
        pipelineModel = self.buildAndFit(model)
        self._testPipe(pipelineModel)
        pipelineModel = self._testSaveAndReloadPipe(pipelineModel)

        trainedModel = pipelineModel.stages[4]
        trainedModel.save(self.modelSavePath)
        reloadedModel = sparknlp_jsl.extensions.finance.SentenceEntityResolverModel.load(self.modelSavePath)
        self.buildAndFitAndTest(reloadedModel)


if __name__ == '__main__':
    unittest.main()
