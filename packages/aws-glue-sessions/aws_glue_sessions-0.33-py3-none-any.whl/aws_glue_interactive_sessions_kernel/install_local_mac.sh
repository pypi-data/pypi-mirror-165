#!/bin/bash

# Move kernels to shared folder
shared_juptyer_path="$HOME/Library/Jupyter/kernels"
mkdir -p ${shared_juptyer_path}
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cp -a "${DIR}/glue_pyspark" "${shared_juptyer_path}/"
cp -a "${DIR}/glue_spark" "${shared_juptyer_path}/"
cp -a "${DIR}/glue_kernel_utils" "${shared_juptyer_path}/"
# enable jupyter widgets
#jupyter nbextension enable --py widgetsnbextension
#jupyter labextension install @jupyter-widgets/jupyterlab-manager

