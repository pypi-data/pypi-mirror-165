from setuptools import setup, find_packages

setup(name="SuperPuper_client",
      version="0.0.1",
      description="SuperPuper_client",
      author="Roman Samarenko",
      author_email="s-3m@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      )
