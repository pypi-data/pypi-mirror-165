from johnsnowlabs.abstract_base.lib_resolver import try_import_lib

if try_import_lib('sparkocr') and  try_import_lib('sparknlp'):
    from sparkocr.transformers import *
    from sparkocr.enums import *
    import pkg_resources
    import sparkocr
