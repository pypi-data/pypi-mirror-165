from johnsnowlabs.abstract_base.lib_resolver import try_import_lib

if try_import_lib('sparknlp_jsl') and try_import_lib('sparknlp'):
    from sparknlp_jsl.annotator import *
    from sparknlp_jsl.base import *
    from sparknlp_jsl.pretrained import InternalResourceDownloader
    # from sparknlp.base import *
    # from sparknlp.annotator import *
    from sparknlp_jsl.compatibility import Compatibility
    from sparknlp_jsl.annotator import TFGraphBuilder
    from sparknlp_jsl.eval import NerDLMetrics, NerDLEvaluation, SymSpellEvaluation, POSEvaluation, \
        NerCrfEvaluation, NorvigSpellEvaluation


else:
    pass
