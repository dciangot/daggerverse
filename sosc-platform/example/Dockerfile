FROM quay.io/jupyter/tensorflow-notebook:python-3.11

USER root

RUN apt update && apt install -y graphviz

USER jovyan

RUN conda install -y -c conda-forge dask distributed

RUN pip3 install boto3 graphviz black papermill nats-python pillow tqdm mlflow  "tensorflow<2.15" "tensorflow-cpu<2.15" "keras<3"

RUN mkdir $HOME/bin $HOME/data

RUN curl https://dl.min.io/client/mc/release/linux-amd64/mc \
  --create-dirs \
  -o $HOME/bin/mc \
  && chmod +x $HOME/bin/mc \
  && export PATH=$PATH:$HOME/bin

RUN conda install -y -c conda-forge \
  jupyterlab-git \
  jupyter-resource-usage \
  nodejs \
  dask-labextension \
  jupyter-server-proxy \
  jupyter-ai \
  jupyterlab-s3-browser \
  langchain-openai \
  jedi-language-server

RUN jupyter labextension enable jupyterlab_s3_browser \
  &&  jupyter labextension enable jupyter_resource_usage

COPY config.py /etc/jupyter/jupyter_server_config.py

USER root

RUN usermod -aG sudo jovyan
# New added for disable sudo password
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN wget https://dl.min.io/server/minio/release/linux-amd64/minio \
  && chmod +x minio \
  && mv minio /usr/bin/

RUN chmod +x /opt/init.sh

USER jovyan
