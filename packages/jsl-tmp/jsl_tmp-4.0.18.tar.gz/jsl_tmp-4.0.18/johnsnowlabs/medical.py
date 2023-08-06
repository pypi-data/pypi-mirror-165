from johnsnowlabs.abstract_base.lib_resolver import try_import_lib

if try_import_lib('sparknlp_jsl') and try_import_lib('sparknlp'):
    # Pretrained
    from sparknlp_jsl.annotator import \
        AssertionLogRegModel, \
        AssertionDLModel, \
        DeIdentificationModel, \
        DocumentLogRegClassifierModel, \
        RelationExtractionModel, \
        RelationExtractionDLModel, \
        ChunkMergeModel, \
        SentenceEntityResolverModel, \
        ChunkMapperModel, \
        BertSentenceEmbeddings, \
        BertSentenceChunkEmbeddings, \
        ChunkKeyPhraseExtraction, \
        NerDisambiguatorModel, \
        EntityChunkEmbeddings, \
        ZeroShotRelationExtractionModel, \
        TFGraphBuilder

    from sparknlp_jsl.annotator import \
        AssertionLogRegApproach, \
        AssertionDLApproach, \
        DeIdentification, \
        DocumentLogRegClassifierApproach, \
        RelationExtractionApproach, \
        ChunkMergeApproach, \
        SentenceEntityResolverApproach, \
        ChunkMapperApproach, \
        NerDisambiguator, \
        ContextualParserApproach

    from sparknlp_jsl.annotator import MedicalNerModel as NerModel
    from sparknlp_jsl.annotator import MedicalNerApproach as NerApproach
    from sparknlp_jsl.annotator import MedicalBertForTokenClassifier as BertForTokenClassifier
    from sparknlp_jsl.annotator import MedicalDistilBertForSequenceClassification as DistilBertForSequenceClassification
    from sparknlp_jsl.annotator import MedicalBertForSequenceClassification as BertForSequenceClassification
    from sparknlp_jsl.compatibility import Compatibility
    from sparknlp_jsl.pretrained import InternalResourceDownloader
    from sparknlp_jsl.eval import NerDLMetrics, NerDLEvaluation, SymSpellEvaluation, POSEvaluation, \
        NerCrfEvaluation, NorvigSpellEvaluation

    # from sparknlp.base import *
    # from sparknlp.annotator import *
    # from sparknlp_jsl.annotator import *
    # from sparknlp_jsl.base import *
    # TODO FIN/LEG ADD
    # FinanceBertForSequenceClassification,\
    # FinanceNerModel,\
    # FinanceBertForTokenClassification,\
    # LegalNerModel,\
    # LegalBertForTokenClassification,\
    # LegalBertForSequenceClassification


    from sparknlp_jsl.functions import *
"""
MedicalNerModel  is now NerModel
MedicalNerApproach  is now NerApproach
MedicalBertForTokenClassifier  is now BertForTokenClassifier
MedicalDistilBertForSequenceClassification  is now DistilBertForSequenceClassification
MedicalBertForSequenceClassification  is now BertForSequenceClassification

"""

else:
    pass
