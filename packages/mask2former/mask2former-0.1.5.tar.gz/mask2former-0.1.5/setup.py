import os
import setuptools
import subprocess
from typing import List

file_dir = os.path.dirname(os.path.realpath(__file__))


def runcmd(cmds: List[str]):
    return subprocess.call(cmds, shell=True)


command = ["make", "install"]
runcmd(command)

setuptools.setup(
    name='mask2former',
    version='0.1.5',
    author='Reza Mohebbian',
    author_email='',
    description='Mask2Former',
    long_description_content_type='text/markdown',

    packages=setuptools.find_packages(),
    license='Apache License 2.0',
    install_requires=["setuptools==59.5.0", "tensorboard", "tensorboard-pytorch",
                      "torch==1.9.1+cu111",
                      "detectron2", "deepspeed==0.7.2", "fairscale==0.4.6",
                      "pytorch-lightning==1.7.3"],
    url="https://github.com/antecessor/mask2former",
    python_requires='>=3.7, <3.8',  # matplotlib >3.1 requires python >=3.6
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
    ]
)
