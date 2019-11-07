# Setup SPTAG on Ubuntu 16.04 LTS

In this section, will describe howto setup SPTAG on Ubuntu machine.

1. Update ubuntu and build env.
```
sudo apt-get update && sudo apt-get install build-essential
```
2. Install cmake 
- Create a directory for cmake
```
mkdir opt
```
- Download "cmake- 3.14.7-Linux-x86_64.sh" version
```
wget https://github.com/Kitware/CMake/releases/download/v3.14.7/cmake-3.14.7-Linux-x86_64.sh
```
- Follow these instructions:
    1. Visit https://cmake.org/download/ and download the latest binaries  
    2. `chmod +x /opt/cmake-3.<your_version>.sh` (chmod makes the script executable)
    3. `sudo bash /opt/cmake-3.<your_version.sh>` (you'll need to press `y` twice)    
    The script installs to `/opt/cmake-3.<your_version>` so in order to get the `cmake` command, make a symbolic link:
    4. `sudo ln -s /opt/cmake-3.<your_version>/bin/* /usr/local/bin`
    5. `cmake --version` Note: If you encounter this error: *The program 'cmake' is currently not installed*, Please try the command from step 3 again with a full path (i.e. `sudo ln -s /home/<your name>/SPTAG/opt/cmake-3.14.7-Linux-x86_64/bin/* /usr/local/bin`)

4. Install boost
- Download boost 1.67 version:
```
wget https://dl.bintray.com/boostorg/release/1.67.0/source/boost_1_67_0.tar.gz
```
(There are some [version mis-matching issues](https://github.com/microsoft/SPTAG/issues/26) and reported on github issue)
5. Extract and install
```
tar -xzvf boost*
cd boost_1_67_0
./bootstrap.sh --prefix=/usr/local
./b2
sudo ./b2 install
sudo apt-get install swig
```
6. Install py3.6-dev
- https://stackoverflow.com/questions/43621584/why-cant-i-install-python3-6-dev-on-ubuntu16-04
```
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6
```
7. Generate make files
```
cmake ..
```
8. Run make
```
make
```
9. Install Miniconda or Anaconda environment   
Follow these links:
    - https://docs.conda.io/en/latest/miniconda.html
    - https://conda.io/projects/conda/en/latest/user-guide/install/linux.html
    
10. Setup conda env for SPTAG
```
conda create -n sptag python=3.6
conda activate sptag
conda install jupyter
conda install seaborn
pip install pillow
```
Add SPTAG to conda path
```
conda develop <path-to-Release-folder>
```

11. Test with Jupyter notebook
- Open port 8080:   
Go to: Azure Portal > Networking > Add inbound security rule
- Connect to VM (SSH or password)
- (Optional) If you have not activated conda
```
conda activate sptag
```
- Start the Jupyter notebook
```
jupyter notebook --ip=0.0.0.0 --port=8080
```
- Open http://<your public IP address>:8080/
- Copy and paste your token to jupyter notebook
- Download [SPTAG test notebook file](https://github.com/luckylukash/SPTAG/blob/master/docs/dw-sptag-new-version.ipynb) and run to test
