from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name='aiogram_calendar3x',
  packages=[],
  version='0.0.1',
  license='MIT',
  description='Simple Inline Calendar & Date Selection tool for Aiogram Telegram bots',
  long_description=long_description,
  author='Lev',
  author_email='',
  url='https://github.com/lev007-ops/aiogram_calendar_3x',
  keywords=['Aiogram', 'Telegram', 'Bots', 'Calendar'],
  install_requires=[
          'aiogram==3.0.0b3',
      ]
)
