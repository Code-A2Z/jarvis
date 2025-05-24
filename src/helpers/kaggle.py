import streamlit as st
import os

from src.helpers.checkKeyExist import isKeyExist

@st.cache_resource(ttl=86400)
def downloadNotebookOutput(username, notebook_name, folder_name, version=None):
  """
  Downloads the output files of a specified Kaggle notebook to a local folder.

  This function checks for Kaggle API credentials in Streamlit secrets, sets them as environment variables,
  and then uses the Kaggle CLI to download the output of a given notebook. The result is cached for 24 hours.

  Args:
    username (str): Kaggle username of the notebook owner.
    notebook_name (str): Name of the Kaggle notebook (kernel) to download output from.
    folder_name (str): Local folder path where the output files will be saved.
    version (str, optional): Specific version of the notebook output to download. Defaults to None (latest).

  Raises:
    Streamlit error and stops execution if Kaggle credentials are missing.
  """
  exists = isKeyExist(['KAGGLE_USERNAME', 'KAGGLE_KEY'], 'kaggle')
  if not exists['KAGGLE_USERNAME'] or not exists['KAGGLE_KEY']:
    st.error("Kaggle credentials are missing. Please set them in Streamlit secrets.", icon="🚨")
    st.stop()
  os.environ['KAGGLE_USERNAME'] = st.secrets['kaggle']['KAGGLE_USERNAME']
  os.environ['KAGGLE_KEY'] = st.secrets['kaggle']['KAGGLE_KEY']
  version_arg = f"--version {version}" if version else ""
  os.system(f"kaggle kernels output {username}/{notebook_name} -p {folder_name} {version_arg}")

@st.cache_resource(ttl=86400)
def downloadDataset(dataset_name, version=None):
  """
  Downloads a Kaggle dataset to the local directory.

  This function checks for Kaggle API credentials in Streamlit secrets, sets them as environment variables,
  and then uses the Kaggle CLI to download the specified dataset. Optionally, a specific version of the dataset
  can be downloaded. The result is cached for 24 hours.

  Args:
    dataset_name (str): The Kaggle dataset identifier in the format 'owner/dataset-name'.
    version (str, optional): Specific version of the dataset to download. Defaults to None (latest).

  Raises:
    Streamlit error and stops execution if Kaggle credentials are missing.
  """
  exists = isKeyExist(['KAGGLE_USERNAME', 'KAGGLE_KEY'], 'kaggle')
  if not exists['KAGGLE_USERNAME'] or not exists['KAGGLE_KEY']:
    st.error("Kaggle credentials are missing. Please set them in Streamlit secrets.", icon="🚨")
    st.stop()
  os.environ['KAGGLE_USERNAME'] = st.secrets['kaggle']['KAGGLE_USERNAME']
  os.environ['KAGGLE_KEY'] = st.secrets['kaggle']['KAGGLE_KEY']
  version_arg = f"--version {version}" if version else ""
  os.system(f"kaggle datasets download -d {dataset_name} {version_arg}")
