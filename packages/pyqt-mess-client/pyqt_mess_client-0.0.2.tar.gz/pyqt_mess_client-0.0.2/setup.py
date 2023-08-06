from setuptools import setup, find_packages

setup(name="pyqt_mess_client",
      version="0.0.2",
      description="MessLex Client",
      author="Ivan Ivanov",
      author_email="iv.iv@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )