from setuptools import Extension, setup

setup(
    name='msur-packages',
    version='1.0.2',
    license='MIT',
    author='Photon94',
    author_email='299792458.photon.94@gmail.com',
    install_requires=[
            'loguru', 'pydantic', 'anyio',
            'importlib-metadata; python_version >= "3.8"',
        ],
    ext_modules=[
        Extension(name='msur_packages.crc16', sources=['crc16/crc16.c'])
    ],
    package_dir={
        'msur_packages.driver': 'driver',
    },
    packages=['msur_packages.driver'],
    zip_safe=False,
    long_description='''
MSU Robotics Team services

Package provide services for working msur-packages `msur-packages`_

.. _msur-packages: https://github.com/Photon94/msur-packages.git''',
    url='https://github.com/Photon94/msur-services.git',
    project_urls={
            "Source": "https://github.com/Photon94/msur-services.git",
        },
)