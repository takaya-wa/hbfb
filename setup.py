from setuptools import setup

install_requires = ["numpy", "torch", "pfrl", "gym", "pyserial"]

setup(
    name='hbfb',
    author='Watanabe Takaya',
    url='https://github.com/takaya-wa/hbfb',
    packages=['hbfb'],
    package_dir={'hbfb':'hbfb'},
    install_requires=install_requires
)