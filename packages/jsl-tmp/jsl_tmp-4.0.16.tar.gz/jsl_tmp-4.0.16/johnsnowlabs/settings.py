from os.path import expanduser

# libs
raw_version = '0.0.2'
raw_version_nlp = '4.0.2'
raw_version_medical = '4.0.2'
raw_version_ocr = '4.0.0'
raw_version_nlu = '4.0.0'

json_indent = 4

# Local paths for jsl home

## Directories
root_dir = f'{expanduser("~")}/.johnsnowlabs'
license_dir = f'{root_dir}/licenses'
java_dir = f'{root_dir}/java_installs'
py_dir = f'{root_dir}/py_installs'

# Info Files
root_info_file = f'{root_dir}/info.json'
java_info_file = f'{java_dir}/info.json'
py_info_file = f'{py_dir}/info.json'
creds_info_file = f'{license_dir}/info.json'

# databricks paths
dbfs_home_dir = 'dbfs:/johnsnowlabs'
dbfs_java_dir = f'{dbfs_home_dir}/java_installs'
dbfs_py_dir = f'{dbfs_home_dir}/py_installs'
db_py_jobs_dir = f'{dbfs_home_dir}/py_jobs'
db_py_notebook_dir = f'{dbfs_home_dir}/py_notebook_jobs'
db_jar_jobs_dir = f'{dbfs_home_dir}/jar_jobs'

db_cluster_name = 'John-Snow-Labs-Databricks-Auto-Cluster🚀'
db_job_name = 'John-Snow-Labs-Job {job} 🚀'
db_run_name = 'John-Snow-Labs-Run 🚀'

# Local Spark mode
spark_session_name = 'John-Snow-Labs-Spark-Session 🚀'
