from dataclasses import dataclass
from typing import Optional

from johnsnowlabs import settings

from johnsnowlabs.abstract_base.base_enum import BaseEnum
from johnsnowlabs.py_models.primitive import LibVersionIdentifier
from johnsnowlabs.py_models.lib_version import LibVersion


class JvmHardwareTarget(BaseEnum):
    gpu = 'gpu'
    cpu = 'cpu'
    m1 = 'm1'

    @classmethod
    def bool_choice_to_hardware(cls, gpu: bool = False, cpu: bool = False, m1: bool = False) -> 'JvmHardwareTarget':
        if gpu:
            return cls.gpu
        elif cpu:
            return cls.cpu
        elif m1:
            return cls.m1
        else:
            return cls.cpu

    # if gpu:
    #     suite = get_install_suite_from_jsl_home(only_jars=True, jvm_hardware_target=cls.gpu)
    # elif m1:
    #     suite = get_install_suite_from_jsl_home(only_jars=True, jvm_hardware_target=JvmHardwareTarget.m1)
    # else:
    #     suite = get_install_suite_from_jsl_home(only_jars=True, jvm_hardware_target=JvmHardwareTarget.cpu)


class PyInstallTypes(BaseEnum):
    tar = 'tar.gz'
    wheel = 'whl'


class SparkVersion(BaseEnum):
    # Broad versions
    spark3xx = LibVersion('3.x.x')
    spark31x = LibVersion('3.1.x')
    spark32x = LibVersion('3.2.x')
    spark33x = LibVersion('3.3.x')
    spark330 = LibVersion('3.3.0')
    spark322 = LibVersion('3.2.2')
    spark321 = LibVersion('3.2.1')
    spark320 = LibVersion('3.2.0')
    spark313 = LibVersion('3.1.3')
    spark312 = LibVersion('3.1.2')
    spark311 = LibVersion('3.1.1')
    spark303 = LibVersion('3.0.3')
    spark302 = LibVersion('3.0.2')
    spark301 = LibVersion('3.0.1')
    spark300 = LibVersion('3.0.0')


# healthcare = LibVersion('4.0.2')
# spark_nlp = LibVersion('4.0.2')
# ocr = LibVersion('4.0.0')
# nlp_display = LibVersion('4.0.0')
# nlu = LibVersion('4.0.0')

class LatestCompatibleProductVersion(BaseEnum):

    healthcare = LibVersion(settings.raw_version_medical)
    spark_nlp = LibVersion(settings.raw_version_nlp)
    ocr = LibVersion(settings.raw_version_ocr)
    nlu = LibVersion(settings.raw_version_nlu)
    nlp_display = LibVersion('4.0.0')
    pyspark = LibVersion('3.2.0')
    finance = LibVersion('finance')
    spark = LibVersion('4.2.0')
    java = LibVersion('java')
    python = LibVersion('python')


class LicenseType(BaseEnum):
    trial = 'Trial'
    research = 'Research'


class LicensePlattform(BaseEnum):
    none = None
    databricks = 'Databricks'
    floating = 'Floating'


class LicensePlattform(BaseEnum):
    none = None
    research = 'Research'


class ProductName(BaseEnum):
    hc = 'Spark-Healthcare'
    nlp = 'Spark-NLP'
    ocr = 'Spark-OCR'
    finance = 'Spark-Finance'
    nlp_display = 'NLP-Display'
    nlu = 'nlu'
    jsl_full = 'full'
    pyspark = 'pyspark'
    spark = 'spark'
    java = 'java'
    python = 'python'


class ProductLogo(BaseEnum):
    healthcare = '💊'  # 🏥 🩺 💊 ❤️ ‍🩹 ‍⚕️💉 🥼 🚑 🔬 🫀 🩻 🧪
    spark_nlp = '🚀'
    ocr = '🕶'  # 👁️  🤖 🦾🦿 🥽 👀 🕶 🥽 ⚕
    finance = '🤑'  # 🤑🏦💲💳💰💸💵💴💶💷
    nlp_display = '🎨'
    nlu = '🤖'
    jsl_full = '💯🕴'  # 🕴
    java = '🫘'  # 🫘 # ☕ ♨ 🥃 🥃 🧋🍹♨️🥤🫖
    python = '🐍'  # 🐉
    pyspark = '🐍+⚡'
    spark = '⚡ '
    databricks = '🧱'


class ProductSlogan(BaseEnum):
    healthcare = 'Heal the planet with NLP!'
    spark_nlp = 'State of the art NLP at scale'
    ocr = 'Empower your NLP with a set of eyes'
    pyspark = 'The big data Engine'
    nlu = '1 line of code to conquer nlp!'
    jsl_full = 'The entire John Snow Labs arsenal!'
    finance = 'NLP for the Finance Industry'
    nlp_display = 'Visualize and Explain NLP!'
    spark = '⚡'
    java = '☕'
    python = '🐍'


@dataclass
class InstalledProductInfo:
    """Representation of a JSL product install. Version is None if not installed  """
    product: ProductName
    version: Optional[LibVersionIdentifier] = None


@dataclass
class JslSuiteStatus:
    """Representation and install status of all JSL products and its dependencies.
    Version attribute of InstalledProductInfo is None for uninstalled products
    """
    spark_nlp_info: Optional[InstalledProductInfo] = None
    spark_hc_info: Optional[InstalledProductInfo] = None
    spark_ocr_info: Optional[InstalledProductInfo] = None
    nlu_info: Optional[InstalledProductInfo] = None
    sparknlp_display_info: Optional[InstalledProductInfo] = None
    pyspark_info: Optional[InstalledProductInfo] = None
