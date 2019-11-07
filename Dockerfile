FROM ubuntu:18.04

WORKDIR /app
COPY CMakeLists.txt ./
COPY AnnService ./AnnService/
COPY Test ./Test/
COPY Wrappers ./Wrappers/
COPY Release/app.py ./Release/
COPY Release/caltech101_np_4096d.npy ./Release/
COPY Release/caltech101_np_4096d_filenames.npy ./Release/
COPY Release/features_extractor.py ./Release/
COPY Release/app.py ./Release/
COPY Release/sptag_indice/ ./Release/
COPY Release/upload-file/ ./Release/

RUN apt-get update && apt-get -y install wget build-essential \
    # remove the following if you don't want to build the wrappers
    openjdk-8-jdk python3-pip swig

# cmake >= 3.12 is required
RUN wget "https://github.com/Kitware/CMake/releases/download/v3.14.4/cmake-3.14.4-Linux-x86_64.tar.gz" -q -O - \
        | tar -xz --strip-components=1 -C /usr/local

# specific version of boost
RUN wget "https://dl.bintray.com/boostorg/release/1.67.0/source/boost_1_67_0.tar.gz" -q -O - \
        | tar -xz && \
        cd boost_1_67_0 && \
        ./bootstrap.sh && \
        ./b2 install && \
        # update ld cache so it finds boost in /usr/local/lib
        ldconfig && \
        cd .. && rm -rf boost_1_67_0

# build
RUN mkdir build && cd build && cmake .. && make && cd ..

# install numpy
RUN pip3 install numpy

# install Flask
RUN pip3 install Flask

# install pandas
RUN pip3 install pandas

# install pillow
RUN pip3 install Pillow

# install tensorflow (needed this specific version)
RUN pip3 install tensorflow==1.14

# install keras (needed this specific version)
RUN pip3 install keras==2.2.5

# so python can find the SPTAG module
ENV PYTHONPATH=/app/Release