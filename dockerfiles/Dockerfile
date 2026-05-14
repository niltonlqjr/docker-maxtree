FROM ubuntu:22.04 

ARG UID
ARG GID

ARG VOLUME_DIR

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Sao_Paulo
ENV LANG=en_US.utf8


RUN apt-get update && \
    apt-get install -y \
    vim git wget iputils-ping sudo htop net-tools locales \
    unzip sudo build-essential openssh-client openssh-server \
    libncurses5-dev libpcap-dev python3-pip pssh cmake meson\
    #mozjpeg
    nasm libpng-dev \
    #libvips
    libglib2.0-dev libjpeg-dev

RUN echo 'PasswordAuthentication no' >> /etc/ssh/sshd_config

RUN addgroup --gid $GID experiments  
RUN adduser --uid $UID --gid $GID --disabled-password --gecos "" experiments 
RUN echo 'experiments ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

RUN mkdir -p /dependencies

#install mozjpeg and openjpeg

#tar files are added as a fild
ADD ./deps/mozjpeg-4.1.1.tar.gz /dependencies/
ADD ./deps/openjpeg-2.5.3.tar.gz /dependencies/
ADD ./deps/cfitsio-4.4.0.tar.gz /dependencies/
ADD libvips-8.16.0.tar.gz /dependencies/

WORKDIR /dependencies


#install mozjpeg (required from libvips to manipulate jpeg)
RUN cd mozjpeg-4.1.1 && \
    mkdir build && \
    cd build && \
    cmake -G"Unix Makefiles" ../ && \
    make && \
    make install

#install openjpeg (required from libvips to manipulate jpeg2000)
RUN cd openjpeg-2.5.3 && \
    mkdir build && \
    cd build && \
    cmake ../ && \
    make && \
    make install

#install cfitsio (required from libvips to manipulate fits)
RUN cd cfitsio-4.4.0 \
    && ./configure --prefix=/usr/local\
    && make \
    && make install 

#install libvips
RUN cd libvips-8.16.0 && \
    meson setup build --prefix /usr/local && \
    cd build && \
    meson compile && \
    meson install

#install zeromq 
RUN git clone https://github.com/niltonlqjr/libzmq-fork.git && \
    cd libzmq-fork && \
    mkdir build && \
    cd build && \
    cmake ../ && \
    make && \
    make install && \
    git clone https://github.com/niltonlqjr/cppzmq-fork && \
    cd cppzmq-fork && \
    mkdir build && \
    cd build && \
    cmake ../ && \
    make && \
    make install

#install rapidyaml
RUN git clone https://github.com/niltonlqjr/rapidyaml-fork.git --recursive && \
    cd rapidyaml-fork && \
    mkdir build && \
    cd build && \
    cmake ../ && \
    make && \
    make install

ENV LD_LIBRARY_PATH=/usr/local/lib
    
#change user
USER experiments

WORKDIR /home/experiments

RUN git clone https://github.com/niltonlqjr/maxtree.git
RUN mkdir -p /home/experiments/maxtree/output/parallel/example

RUN mkdir /home/experiments/host

RUN pip3 install psutil
RUN sudo pip3 install psutil

RUN pip3 install pyyaml
RUN sudo pip3 install pyyaml

WORKDIR /home/experiments/maxtree
RUN git pull
RUN make TYPE=R OPT=-O3
