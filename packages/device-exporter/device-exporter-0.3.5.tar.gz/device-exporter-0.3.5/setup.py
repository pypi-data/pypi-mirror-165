from setuptools import setup, find_packages

setup(name='device-exporter',
      version='0.3.5',
      description='Device exporter app',
      url='https://gitlab.com/device-logging/device-exporter',
      author='Franciszek Przewoźny',
      author_email='przewozny.franciszek@gmail.com',
      license='MIT',
      packages=find_packages(exclude=['tests']))
