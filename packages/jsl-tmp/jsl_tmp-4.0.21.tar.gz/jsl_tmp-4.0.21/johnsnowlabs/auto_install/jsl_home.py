import shutil
import sys
from typing import Optional, List
from johnsnowlabs import settings
from johnsnowlabs.auto_install.softwares import Software

from johnsnowlabs.py_models.install_info import JvmInstallInfo, PyInstallInfo, \
    RootInfo, InstallSuite, LocalPy4JLib, InstallFolder
from johnsnowlabs.py_models.jsl_secrets import JslSecrets
from johnsnowlabs.utils.enums import JvmHardwareTarget, PyInstallTypes, ProductName, ProductLogo
from johnsnowlabs.py_models.url_dependency import UrlDependency
import os
from pathlib import Path
from johnsnowlabs.auto_install.offline_install import get_dependency_urls

"""Folder structure :
~.johnsnowlabs/
   ├─ licenses/
   │  ├─ info.json
   │  ├─ license1.json
   │  ├─ license2.json
   ├─ java_installs/
   │  ├─ info.json
   │  ├─ app1.jar
   │  ├─ app2.jar
   ├─ py_installs/
   │  ├─ info.json
   │  ├─ app1.tar.gz
   │  ├─ app2.tar.gz
   ├─ info.json
"""


def jsl_home_exist():
    return os.path.exists(settings.root_info_file)


def is_jsl_home_outdated():
    if os.path.exists(settings.root_info_file):
        old_infos = RootInfo.parse_file(settings.root_info_file)
        if old_infos.version.as_str() == settings.raw_version:
            return False
        else:
            return True

    else:
        raise Exception(f'JSL-Home does not exist! Cannot check if outdated')


def download_deps_and_create_info(deps: List[UrlDependency],
                                  lib_dir, info_file_path,
                                  overwrite=False, ):
    """Download a list of deps to given lib_dir folder and creates info_file at info_file_path.
    TODO check if Java Dep for new hardware release but same version
    """
    info, old_info = {}, {}
    if os.path.exists(info_file_path):
        #  keep old infos, we assume they are up-to-date and compatible
        old_info = InstallFolder.parse_file(info_file_path)

    for p in deps:
        if os.path.exists(f'{lib_dir}/{p.file_name}') and not overwrite:
            continue

        print_prefix = Software.for_name(p.product_name).logo
        if p.dependency_type in JvmHardwareTarget:
            print_prefix = f'{ProductLogo.java.value}+{print_prefix} Java Library'
            constructor = JvmInstallInfo
        elif p.dependency_type in PyInstallTypes:
            print_prefix = f'{ProductLogo.python.value}+{print_prefix} Python Library'
            constructor = PyInstallInfo
        else:
            raise ValueError(f'Unknown Install type {p.dependency_type}')
        p.download_url(lib_dir, name_print_prefix=print_prefix)
        info[p.file_name] = constructor(
            file_name=p.file_name,
            product=p.product_name,
            compatible_spark_version=p.spark_version.value.as_str(),
            install_type=p.dependency_type.value,
            product_version=p.dependency_version.as_str())
    if info:
        info = InstallFolder(**{'infos': info})
        if old_info:
            info.infos.update(old_info.infos)
        info.write(info_file_path, indent=4)


def setup_jsl_home(
        secrets: Optional[JslSecrets] = None,
        jvm_install_type: JvmHardwareTarget = JvmHardwareTarget.cpu,
        py_install_type: PyInstallTypes = PyInstallTypes.wheel,
        only_jars: bool = False,
        spark_version=None,
        overwrite=False,
        log=True
) -> None:
    # Create all Paths
    if log:
        print(f'👷 Setting up John Snow Labs home in /home/ckl/.johnsnowlabs this might take a few minutes.')
    Path(settings.license_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.java_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.py_dir).mkdir(parents=True, exist_ok=True)

    if jsl_home_exist() and is_jsl_home_outdated():
        # TODO download non-JVM deps i.e wheels/tars x p with  pipdownload
        # TODO uuse install_software to setup pip sub_dep folder!
        # Delete everything except license data and re-create folder
        shutil.rmtree(settings.java_dir)
        shutil.rmtree(settings.py_dir)
        Path(settings.java_dir).mkdir(parents=True, exist_ok=True)
        Path(settings.py_dir).mkdir(parents=True, exist_ok=True)

    java_deps, py_deps = get_dependency_urls(
        secrets=secrets,
        spark_version=spark_version,
        jvm_install_type=jvm_install_type,
        py_install_type=py_install_type)

    # store deps to jsl home with info.json files
    if not only_jars:
        download_deps_and_create_info(py_deps, settings.py_dir, settings.py_info_file, overwrite)
    download_deps_and_create_info(java_deps, settings.java_dir, settings.java_info_file, overwrite)

    RootInfo(version=settings.raw_version, run_from=sys.executable).write(settings.root_info_file, indent=4)
    print(f'🙆 JSL Home setup in {settings.root_dir}')


def get_install_suite_from_jsl_home(create_jsl_home_if_missing: bool = True,
                                    jvm_hardware_target: JvmHardwareTarget = JvmHardwareTarget.cpu,
                                    hc: bool = True,
                                    ocr: bool = True,
                                    nlp: bool = True,
                                    only_jars: bool = False,
                                    recursive_call=False,
                                    # Secret Flow Params
                                    browser_login: bool = True,
                                    force_browser: bool = False,
                                    access_token: Optional[str] = None,
                                    license_number: int = 0,
                                    secrets_file: Optional[str] = None,
                                    hc_license: Optional[str] = None,
                                    hc_secret: Optional[str] = None,
                                    ocr_secret: Optional[str] = None,
                                    ocr_license: Optional[str] = None,
                                    aws_access_key: Optional[str] = None,
                                    aws_key_id: Optional[str] = None,
                                    ) -> InstallSuite:
    """Read all info files from JSL home if exists.
    If not exists, sets up JSL home"""
    license_data: JslSecrets = JslSecrets.build_or_try_find_secrets(browser_login=browser_login,
                                                                    force_browser=force_browser,
                                                                    access_token=access_token,
                                                                    license_number=license_number,
                                                                    secrets_file=secrets_file,
                                                                    hc_license=hc_license,
                                                                    hc_secret=hc_secret,
                                                                    ocr_secret=ocr_secret,
                                                                    ocr_license=ocr_license,
                                                                    aws_access_key=aws_access_key,
                                                                    aws_key_id=aws_key_id,
                                                                    return_empty_secrets_if_none_found=True)

    data = ()

    # TODO this needs to call JSlSecrets to start interactive Secret fetch flow
    # TODO CHECK IF MISSING
    if create_jsl_home_if_missing:
        if not jsl_home_exist():
            # Nothing setup yet, download atlast spark nlp jars
            print(f'🤓 Looks like {settings.root_dir} is missing, creating it')
            setup_jsl_home(only_jars=only_jars)

        if jsl_home_exist() and is_jsl_home_outdated():
            # Nothing setup yet, download atlast spark nlp jars
            print(f'🤓 Looks like {settings.root_dir} is outdated, updating it')
            setup_jsl_home(only_jars=only_jars)

    # TODOD check if found but hardware target not match! -> Download
    java_folder, py_folder = None, None

    if os.path.exists(settings.java_info_file):
        java_folder = InstallFolder.parse_file(settings.java_info_file)
    if os.path.exists(settings.py_info_file):
        py_folder = InstallFolder.parse_file(settings.py_info_file)

    info = RootInfo.parse_file(settings.root_info_file)
    suite = InstallSuite(
        nlp=LocalPy4JLib(
            java_lib=java_folder.get_product_entry(ProductName.nlp, jvm_hardware_target) if java_folder else None,
            py_lib=py_folder.get_product_entry(ProductName.nlp) if py_folder else None),
        hc=LocalPy4JLib(
            java_lib=java_folder.get_product_entry(ProductName.hc) if java_folder else None,
            py_lib=py_folder.get_product_entry(ProductName.hc) if py_folder else None),
        ocr=LocalPy4JLib(
            java_lib=java_folder.get_product_entry(ProductName.ocr) if java_folder else None,
            py_lib=py_folder.get_product_entry(ProductName.ocr) if py_folder else None),
        secrets=license_data,
        info=info
    )

    # TODO  check if license has newer version than whats installed?
    if any((not suite.ocr.java_lib and suite.secrets.OCR_LICENSE and ocr,
            not suite.hc.java_lib and suite.secrets.HC_LICENSE and hc,
            not suite.nlp.java_lib and nlp)) and not recursive_call:
        print(f'🤓 Looks like you are missing some jars, fetching them ...')
        setup_jsl_home(license_data,
                       jvm_install_type=jvm_hardware_target,
                       only_jars=only_jars, log=False)
        # After re-setting up jsl_home, call this method again
        return get_install_suite_from_jsl_home(
            jvm_hardware_target=jvm_hardware_target,
            hc=hc,
            ocr=ocr,
            nlp=nlp,
            only_jars=only_jars,
            recursive_call=True,
            browser_login=browser_login,
            access_token=access_token,
            license_number=license_number,
            secrets_file=secrets_file,
            hc_license=hc_license,
            hc_secret=hc_secret,
            ocr_secret=ocr_secret,
            ocr_license=ocr_license,
            aws_access_key=aws_access_key,
            aws_key_id=aws_key_id,
        )
    return suite

# TODO ZIP!
# TODO validate info.json file with contents ? -> Super edy case

#
# def get_install_suite_from_jsl_home(create_jsl_home_if_missing: bool = True,
#                                     jvm_hardware_target: JvmHardwareTarget = JvmHardwareTarget.cpu,
#                                     hc: bool = True,
#                                     ocr: bool = True,
#                                     nlp: bool = True,
#                                     only_jars: bool = False,
#                                     recursive_call=False,
#                                     # Secret Flow Params
#                                     browser_login: bool = True,
#                                     access_token: Optional[str] = None,
#                                     license_number: int = 0,
#                                     secrets_file: Optional[str] = None,
#                                     hc_license: Optional[str] = None,
#                                     hc_secret: Optional[str] = None,
#                                     ocr_secret: Optional[str] = None,
#                                     ocr_license: Optional[str] = None,
#                                     aws_access_key: Optional[str] = None,
#                                     aws_key_id: Optional[str] = None,
#                                     ) -> InstallSuite:
#     """Read all info files from JSL home if exists.
#     If not exists, sets up JSL home"""
#     json_paths = [settings.java_info_file, settings.py_info_file]
#
#     java_info = InstallFolder.parse_file(settings.java_info_file)
#     py_info = InstallFolder.parse_file(settings.py_info_file)
#
#     data = ()
#     found_secrets: JslSecrets = JslSecrets.build_or_try_find_secrets(browser_login=browser_login,
#                                                                access_token=access_token,
#                                                                license_number=license_number,
#                                                                secrets_file=secrets_file,
#                                                                hc_license=hc_license,
#                                                                hc_secret=hc_secret,
#                                                                ocr_secret=ocr_secret,
#                                                                ocr_license=ocr_license,
#                                                                aws_access_key=aws_access_key,
#                                                                aws_key_id=aws_key_id,
#                                                                return_empty_secrets_if_none_found=True)
#
#     # TODO this needs to call JSlSecrets to start interactive Secret fetch flow
#     # TODO CHECK IF MISSING
#     if not jsl_home_exist() or is_jsl_home_outdated():
#         # Nothing setup yet, download atlast spark nlp jars
#         setup_jsl_home(only_jars=only_jars)
#
#     # TODOD check if found but hardware target not match! -> Download
#
#     for p in json_paths:
#         if not os.path.exists(p):
#             # TODOD FINE?
#             print(f'DEBUG: Missing Info-file in {p} NP?')
#             continue
#         with open(p) as f:
#             data = (*data, json.load(f))
#     # 1. Check if
#
#     data_classes = ()
#     for file_info in data:
#         for v in file_info.values():
#             print(v['file_name'])
#             file_info = InstallFileInfoBase(
#                 file_name=v['file_name'],
#                 product=ProductName(v['product']),
#                 compatible_spark_version=LibVersion(v['compatible_spark_version']),
#                 # install_type=JvmHardwareTarget(v['install_type']) if 'jar' in v['file_name'] else \
#                 #     PyInstallTypes(v['install_type']),
#                 product_version=LibVersion(v['product_version']), )
#             install_type = v['install_type']
#             if install_type in JvmHardwareTarget:
#                 file_info = JvmInstallInfo(*file_info.__dict__.values(), install_type=JvmHardwareTarget(install_type))
#             elif install_type in PyInstallTypes:
#                 file_info = PyInstallInfo(*file_info.__dict__.values(), install_type=PyInstallTypes(install_type))
#             else:
#                 raise Exception(f'Invalid Install Type = {install_type}')
#             data_classes = (*data_classes, file_info)
#
#     info = RootInfo(**json_path_as_dict(settings.root_info_file))
#     license_data = JslSecrets.from_jsl_home()
#     # TODO we could check  for len right away aand download if missing
#     # Only for nLP lib, since other libs should be provided via .install()!
#     java_ocr = [file for file in data_classes if
#                 file.install_type in JvmHardwareTarget and file.product == ProductName.ocr]
#     py_ocr = [file for file in data_classes if file.install_type in PyInstallTypes and file.product == ProductName.ocr]
#     ocr = java_ocr + py_ocr
#
#     java_hc = [file for file in data_classes if
#                file.install_type in JvmHardwareTarget and file.product == ProductName.hc]
#     py_hc = [file for file in data_classes if file.install_type in PyInstallTypes and file.product == ProductName.hc]
#     hc = java_hc + py_hc
#     # Only Spark NLP has hardware specific releases
#     java_nlp = [file for file in data_classes if
#                 file.install_type == jvm_hardware_target and file.product == ProductName.nlp]
#     py_nlp = [file for file in data_classes if file.install_type in PyInstallTypes and file.product == ProductName.nlp]
#     nlp = java_nlp + py_nlp
#
#     if only_jars:
#         suite = InstallSuite(
#             ocr=LocalPy4JLib(java_ocr[0]) if len(java_ocr) == 1 else None,
#             hc=LocalPy4JLib(java_hc[0]) if len(java_hc) == 1 else None,
#             nlp=LocalPy4JLib(java_nlp[0]) if len(java_nlp) == 1 else None,
#             found_secrets=license_data if license_data else None,
#             info=info,
#         )
#         # Try downloading missing things and re-run
#         if not suite.nlp:
#             setup_jsl_home(only_jars=only_jars, jvm_install_type=jvm_hardware_target, )
#             return get_install_suite_from_jsl_home(
#                 create_jsl_home_if_missing=create_jsl_home_if_missing,
#                 jvm_hardware_target=jvm_hardware_target,
#                 hc=hc,
#                 ocr=ocr,
#                 nlp=nlp,
#                 only_jars=only_jars, recursive_call=True)
#
#         if suite.found_secrets and suite.found_secrets.OCR_LICENSE and not suite.ocr:
#             pass
#
#         if suite.found_secrets and suite.found_secrets.HC_LICENSE and not suite.hc:
#             pass
#
#     return InstallSuite(
#         ocr=LocalPy4JLib(*ocr) if len(ocr) == 2 or len(ocr) == 1 else None,
#         hc=LocalPy4JLib(*hc) if len(hc) == 2 or len(hc) == 1 else None,
#         nlp=LocalPy4JLib(*nlp) if len(nlp) == 2 or len(nlp) == 1 else None,
#         found_secrets=license_data if license_data else None,
#         info=info,
#     )
