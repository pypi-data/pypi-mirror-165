from typing import Optional, Tuple, Dict, Union
from johnsnowlabs import settings
from johnsnowlabs.abstract_base.pydantic_model import WritableBaseModel
from johnsnowlabs.py_models.jsl_secrets import JslSecrets
from johnsnowlabs.utils.enums import ProductName, JvmHardwareTarget, PyInstallTypes
from johnsnowlabs.py_models.lib_version import LibVersion


class InstallFileInfoBase(WritableBaseModel):
    file_name: str
    product: ProductName
    compatible_spark_version: Union[str, LibVersion]
    product_version: Union[str, LibVersion]

    # install_type: Optional[JvmHardwareTarget]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.compatible_spark_version = LibVersion(self.compatible_spark_version)
        self.product_version = LibVersion(self.product_version)


class PyInstallInfo(InstallFileInfoBase):
    install_type: PyInstallTypes


class JvmInstallInfo(InstallFileInfoBase):
    install_type: JvmHardwareTarget


class LocalPy4JLib(WritableBaseModel):
    java_lib: Optional[JvmInstallInfo] = None
    py_lib: Optional[PyInstallInfo] = None

    def get_java_path(self):
        return f'{settings.java_dir}/{self.java_lib.file_name}'

    def get_py_path(self):
        return f'{settings.py_dir}/{self.py_lib.file_name}'


class RootInfo(WritableBaseModel):
    version: Union[str, LibVersion]
    run_from: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = LibVersion(self.version)


class InstallFolder(WritableBaseModel):
    infos: Dict[str, Union[PyInstallInfo, JvmInstallInfo]]

    def get_product_entry(self, product: ProductName,
                          hardware_target: Optional[Union[PyInstallTypes, JvmHardwareTarget]] = None):
        for file_name, install_info in self.infos.items():
            if install_info.product == product:
                if hardware_target:
                    if install_info.install_type == hardware_target:
                        return install_info
                else:
                    return install_info


class InstallSuite(WritableBaseModel):
    info: RootInfo
    nlp: LocalPy4JLib
    ocr: Optional[LocalPy4JLib] = None
    hc: Optional[LocalPy4JLib] = None
    secrets: Optional[JslSecrets] = None
    optional_pure_py_jsl: Optional[LocalPy4JLib] = None
    optional_pure_py_jsl_dependencies: Optional[LocalPy4JLib] = None
