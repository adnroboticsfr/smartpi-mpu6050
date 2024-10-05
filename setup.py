from setuptools import setup, find_packages
import os
from setuptools.command.install import install

class PostInstallCommand(install):
    """Post-installation script to install python3-smbus"""
    def run(self):
        # Run original install code
        install.run(self)
        # Run the shell command to install python3-smbus
        os.system('sudo apt-get update')
        os.system('sudo apt-get install -y python3-smbus')

setup(
    name='smartpi-mpu6050',
    version='1.0.0',
    description='MPU-6050 Sensor library for Smart Pi One (Yumi)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/your-repo/smartpi-mpu6050',
    packages=find_packages(),
    install_requires=[],  # We don't list python3-smbus here since it's a system dependency
    cmdclass={
        'install': PostInstallCommand,
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
