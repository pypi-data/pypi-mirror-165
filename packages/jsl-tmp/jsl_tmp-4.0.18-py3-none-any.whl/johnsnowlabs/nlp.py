from johnsnowlabs.abstract_base.lib_resolver import try_import_lib
"""
Hey thanks a lot, there is no right way to deal with those besides letting me know for now because these are bugs :P
I just took care of all of them and released the new veersion which you can get with
pip install jsl_tmp==4.0.16


Changes : 

1. import pyspark.sql.types as T under the hood. You can do T.StringType  and maybe add a comment mentioning  that T = import pyspark.sql.types as T 

2. all methods in sparknlp.functions are now available via  nlp.xxx i.e. you can say nlp.map_annotations_col()

3. All approaches were missing in medical.xxx in the last release, they have been added in the new version.  
Previously Missing Annotators:
AssertionLogRegApproach, AssertionDLApproach, DeIdentification, DocumentLogRegClassifierApproach, 
RelationExtractionApproach, ChunkMergeApproach, SentenceEntityResolverApproach, ChunkMapperApproach, NerDisambiguator, 

4. from sparknlp.pretrained import PretrainedPipeline is now in global variable space after doing  from johnsnowlabs import *, 
    So you just say "PretrainedPipeline" no prefix required.


"""
if try_import_lib('sparknlp'):
    from sparknlp.base import *
    from sparknlp.annotator import *
    import sparknlp
    from sparknlp.pretrained import ResourceDownloader
    from sparknlp.training import CoNLL
    from sparknlp.functions import *
    from sparknlp.pretrained import PretrainedPipeline

if try_import_lib('pyspark'):
    from pyspark.sql import DataFrame
    import pyspark.sql.functions as F
    import pyspark.sql.types as T
    from pyspark.sql import SparkSession
    from pyspark.ml import Pipeline,PipelineModel

if try_import_lib('warnings'):
    import warnings
    warnings.filterwarnings('ignore')

if try_import_lib('pandas'):
    import pandas as pd


if try_import_lib('nlu'):
    from nlu import load, to_nlu_pipe, autocomplete_pipeline, to_pretty_df
    import nlu as nlu
