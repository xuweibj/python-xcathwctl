from setuptools import setup

setup(name='xcathwctl',
      version='1.0',
      description='xCAT hardware control Utilities',
      packages=['xcathwctl', 'xcathwctl.common', 'xcathwctl.hwctl', 'xcathwctl.hwctl.executor'],
      scripts=['xcathwctl']
      )
