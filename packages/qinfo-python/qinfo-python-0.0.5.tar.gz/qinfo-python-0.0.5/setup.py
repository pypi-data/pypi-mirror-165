from setuptools import setup, Extension
from ensurepip import version
from glob import glob
import os
import codecs


here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    LONG_DESCRIPTION = "\n" + fh.read()

srcs = glob("src/modules/*.c") + glob("qinfo/src/*.c") + \
    glob("qinfo/library/*.c")

for item in srcs:
    if "qinfo.c" in item:
        srcs.remove(item)

module = Extension("qinfo", sources=srcs)

setup(name="qinfo-python",
      author="Decator",
      author_email="decator.c@proton.me",
      url="https://github.com/el-wumbus/qinfo-python",
      description="Allows for using qinfo functions",
      long_description_content_type="text/markdown",
      long_description=LONG_DESCRIPTION,
      version="0.0.5",
      ext_modules=[module],
      license='LGPLv3',
      classifiers=[
          "Operating System :: Unix"]
      )
