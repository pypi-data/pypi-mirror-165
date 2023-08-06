# from pyspark.ml import Pipeline
# from pyspark.sql import SparkSession
# from sparknlp_jsl.annotator import *
# import sparknlp_jsl
# https://s3.amazonaws.com/auxdata.johnsnowlabs.com/finance/models/finclf_controls_procedures_item_en_1.0.0_3.2_1660154383195.zip

from sparknlp_jsl.extensions import finance
from sparknlp_jsl.annotator import BertSentenceChunkEmbeddings
finance.ZeroShotRelationExtractionModel
# https://s3.amazonaws.com/auxdata.johnsnowlabs.com/finance/models/finclf_bert_fls_en_1.0.0_3.2_1660658577201.zip
def __get_class(clazz: str):
    """
    Loads Python class from its name.
    """
    print(f'Import for clzz= {clazz}')
    parts = clazz.split(".")
    module = ".".join(parts[:-1])
    print(f'importing {module} ')
    m = __import__(module)
    for comp in parts[1:]:
        print(f'Getting {comp} from {m}')
        m = getattr(m, comp)
    return m

# 'com.johnsnowlabs.extensions.finance.transformer_seq_classification.BertForSequenceClassification'
# clazz='com.johnsnowlabs.nlp.annotator.embeddings.BertEmbeddings'
# clazz='com.johnsnowlabs.nlp.annotators.classification.MedicalBertForSequenceClassification'
# __get_class(clazz)


print("_____________")
clazz='com.johnsnowlabs.extensions.finance.chunk_classification.assertion'
__get_class(clazz)



# AttributeError: module 'com.johnsnowlabs.extensions.finance' has no attribute 'FinanceClassifierDLModel'
