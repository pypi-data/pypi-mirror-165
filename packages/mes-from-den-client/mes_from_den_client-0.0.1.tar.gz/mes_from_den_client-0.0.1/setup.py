from setuptools import setup, find_packages

setup(name="mes_from_den_client",
      version="0.0.1",
      description="Mess Client",
      author="Denis",
      author_email="denis@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
