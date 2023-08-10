from setuptools import setup, find_packages

setup(
    name='montecarlo', 
    author='Hana Nur', 
    version='1.0', 
    url='https://github.com/hrnur/hrn4ch_ds5100_montecarlo',
    author_email = 'hrn4ch@virginia.edu', 
    description='Creates Monte Carlo simulator.', 
    license='MIT',
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'matplotlib']
)