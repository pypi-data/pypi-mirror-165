import os
from setuptools import setup, find_packages

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

setup(
    name='OMP_soil_database',
    version='0.2.0',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A python package for calculating the removal of microbial organisms in the subsurface',
    long_description=read('README.rst'),
    long_description_content_type="text/x-rst",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Hydrology',
    ],
    python_requires='>=3.7',
    project_urls={
    'Source': 'https://github.com/KWR-Water/OMP_soil_database',
    'Documentation': 'http://OMP_soil_database.readthedocs.io/en/latest/',
    'Tracker': 'https://github.com/KWR-Water/OMP_soil_database/issues',
    'Help': 'https://github.com/KWR-Water/OMP_soil_database/issues',
    # 'Help': 'https://stackoverflow.com/questions/tagged/OMP_soil_database'
    },
    install_requires=[
        'pandas>=0.23',

        ],
    include_package_data=True,
    url='https://github.com/KWR-Water/OMP_soil_database',
    author='KWR Water Research Institute',
    author_email='vincent.post@kwrwater.nl, martin.korevaar@kwrwater.nl, martin.van.der.schans@kwrwater.nl, steven.ros@kwrwater.nl'
)
