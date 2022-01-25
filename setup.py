import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
setup(name='A2',
      version='0.0.1',
      url= 'https://github.com/Observe-l/VEC.git',
      install_requires=['gym>=0.2.3',
                        'hfo_py>=0.2']
)
