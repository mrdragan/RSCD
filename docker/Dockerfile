FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu18.04
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN echo "temp"

# Install basic utilities
RUN \
apt-get update -y && \
apt-get install -y --no-install-recommends \
  apt-utils \
  build-essential \
  bzip2 \
  ca-certificates \
  ffmpeg \
  git \
  sudo \
  unzip \
  curl \
  python3 \
  python3-pip \
  python-setuptools \
  wget \
	vim \
  tmux \
  nano \
  cmake && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH /opt/conda/bin:$PATH

WORKDIR /opt/temp
RUN  \
wget \
  --quiet \
   https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh \
  -O /opt/temp/miniconda.sh && \
echo "export PATH=opt/conda/bin:$PATH" > /etc/profile.d/conda.sh && \
/bin/bash /opt/temp/miniconda.sh -b -p /opt/conda/  && \
sudo rm /opt/temp/miniconda.sh

RUN \
cd /usr/local/share/ca-certificates/ && \
curl -o ecc-it-intermediate.crt http://ca.toyon.corp/ecc-it-intermediate.pem && \
curl -o ecc-root.crt http://ca.toyon.corp/ecc-root.pem && \
curl -o root.crt http://ca.toyon.corp/root.pem && \
update-ca-certificates

COPY ./docker/environment.yaml  environment.yaml
RUN cat environment.yaml
RUN conda env update -n base --file environment.yaml

# This is kind of annoying, but you need to put your gpu compute capability (the number by +PTX)
# This information can be found here: https://developer.nvidia.com/cuda-gpus
# Find your gpu and find the compute capability then copy the number next to the +PTX
# NOTE: this can also be found by running this command: nvidia-smi --query-gpu=compute_cap --format=csv
ENV FORCE_CUDA="1"
ARG TORCH_CUDA_ARCH_LIST="7.5+PTX"
ENV TORCH_CUDA_ARCH_LIST="${TORCH_CUDA_ARCH_LIST}"
ADD ./docker/packages_from_deepunrollnet packages_from_deepunrollnet
RUN pip install packages_from_deepunrollnet/package_core/
RUN pip install packages_from_deepunrollnet/package_correlation/
RUN pip install packages_from_deepunrollnet/package_forward_warp/
RUN python -m pip install "git+https://github.com/facebookresearch/detectron2.git"

ARG NEW_GID=1000
ARG NEW_UID=1000
ARG NEW_GROUP=developer
ARG NEW_USER=developer
ARG USER_CONDA_ENV=user-base

RUN \
USER=$NEW_USER && \
GROUP=$NEW_GROUP && \
curl -SsL https://github.com/boxboat/fixuid/releases/download/v0.5/fixuid-0.5-linux-amd64.tar.gz | tar -C /usr/local/bin -xzf - && \
    chown root:root /usr/local/bin/fixuid && \
    chmod 4755 /usr/local/bin/fixuid && \
    mkdir -p /etc/fixuid && \
    printf "user: $USER\ngroup: $GROUP\n" > /etc/fixuid/config.yml

RUN addgroup --gid $NEW_GID $NEW_GROUP \
    && useradd -m -l --uid $NEW_UID --gid $NEW_GID $NEW_USER \
    && usermod -aG sudo ${NEW_USER} \
    && echo "${NEW_USER} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Switch user to developer
USER developer
ENV PATH "/home/${NEW_USER}/.local/bin:${PATH}"
ENV SSL_CERT_DIR "/etc/ssl/certs"
ENV PATH=/toyon/bin:${PATH}
RUN echo "source activate base" > ~/.bashrc
WORKDIR /home/${NEW_USER}

ENTRYPOINT [ "fixuid", "/bin/bash"]
