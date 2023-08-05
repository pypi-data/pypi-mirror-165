# qinfo-python

Python Bindings for [qinfo](https://github.com/el-wumbus/qinfo).

How to install

```bash
pip install qinfo-python
```

How to compile

Build dependencies:
  
* Python3 (Cython)
* gcc
* glibc
* make

```bash
git clone --recurse-submodules https://github.com/el-wumbus/qinfo-python
cd qinfo-pyhton
pip install -r ./requirements.txt 
make package
```

The package is in the `dist` directory.
