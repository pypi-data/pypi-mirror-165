# -*- coding: UTF-8 -*-
from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='AlgorithmLib',
    version='3.3.5',
    packages=setuptools.find_packages(),
    url='https://github.com/pypa/sampleproject',
    license='MIT',
    author=' MA JIANLI',
    author_email='majianli@corp.netease.com',
    description='audio algorithms to compute and test audio quality of speech enhencement',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
    'numpy',
    'wave',
    'matplotlib',
    'datetime',
    'scipy',
    'pystoi',
    'paramiko',
    'moviepy',
    'torch',
    'librosa',
    'requests',
    'pandas',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    data_files=[
                ('', ['algorithmLib/DLLs/p563.dll']),
                ('', ['algorithmLib/DLLs/p563.dylib']),
                ('', ['algorithmLib/DLLs/resampler.dll']),
                ('', ['algorithmLib/DLLs/resample.dylib']),
                ('', ['algorithmLib/DLLs/g160.dll']),
                ('', ['algorithmLib/DLLs/g160.dylib']),
                ('', ['algorithmLib/DLLs/cygwin1.dll']),
                ('', ['algorithmLib/DLLs/peaqb.exe']),
                ('', ['algorithmLib/DLLs/PY_PESQ.dll']),
                ('', ['algorithmLib/DLLs/PY_PESQ.dylib']),
                ('', ['algorithmLib/DLLs/matchsig.dll']),
                ('', ['algorithmLib/DLLs/matchsig.dylib']),
                ('', ['algorithmLib/DLLs/snr_music.dll']),
                ('', ['algorithmLib/DLLs/snr_music.dylib']),
                ('', ['algorithmLib/DLLs/snr_transient.dll']),
                ('', ['algorithmLib/DLLs/snr_transient.dylib']),
                ('', ['algorithmLib/DLLs/time_align.dll']),
                ('', ['algorithmLib/DLLs/time_align.dylib']),
                ('', ['algorithmLib/DLLs/agcDelay.dll']),
                ('', ['algorithmLib/DLLs/agcDelay.dylib']),
                ('', ['algorithmLib/DLLs/attackrelease.dll']),
                ('', ['algorithmLib/DLLs/attackrelease.dylib']),
                ('', ['algorithmLib/DLLs/gaintable.dll']),
                ('', ['algorithmLib/DLLs/gaintable.dylib']),
                ('', ['algorithmLib/DLLs/musicStability.dll']),
                ('', ['algorithmLib/DLLs/musicStability.dylib']),
                ('', ['algorithmLib/DLLs/matchsig_aec.dll']),
                ('', ['algorithmLib/DLLs/matchsig_aec.dylib']),
                ('', ['algorithmLib/DLLs/ERLE_estimation.dll']),
                ('', ['algorithmLib/DLLs/ERLE_estimation.dylib']),
                ('', ['algorithmLib/DLLs/pcc.dll']),
                ('', ['algorithmLib/DLLs/pcc.dylib']),
                ('', ['algorithmLib/DLLS/SC_res_retrain_220316_185754125621__ep_007.tar']),
                ],

    python_requires='>=3.7',
)



