# -*- coding: UTF-8 -*-
from setuptools import setup
from setuptools import Extension

example_module = Extension(name='numpy_demo',  # Ä£¿éÃû³Æ
                           sources=['example.cpp'],    # Ô´Âë
                           include_dirs=['D:/quant_template/cpp_part/pybind11/include']
                           )

setup(ext_modules=[example_module])
