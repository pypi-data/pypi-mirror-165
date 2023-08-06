import sys
from pathlib import Path
from distutils.core import setup, Extension
from Cython.Build import cythonize

Random_Enemy_Attributes_module = Extension('Random_Enemy_Attributes.Random_Enemy_Attributes',
                sources=['Random_Enemy_Attributes/Random_Enemy_Attributes_wrapper.pyx', 'Random_Enemy_Attributes/Random_Enemy_Attributes.cpp'],
                extra_compile_args=["-std=c++14"],
                extra_link_args=["-std=c++14"],
                language='c++')

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="Random_Enemy_Attributes",
    version="1.0.3",
    description="Randomizes enemy stat values for most of the enemies in the game Metroid Prime.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Fantaselion/Random_Enemy_Attributes",
    author="Fantaselion",
    author_email="fantaselion@gmail.com",
    license="MIT",
    packages=['Random_Enemy_Attributes'],
    ext_modules=cythonize(Random_Enemy_Attributes_module),
)
