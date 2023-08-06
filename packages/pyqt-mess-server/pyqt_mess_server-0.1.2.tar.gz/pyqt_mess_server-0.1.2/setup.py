from setuptools import setup, find_packages

setup(name="pyqt_mess_server",
      version="0.1.2",
      description="MessLex Server",
      author="Ivan Ivanov",
      author_email="iv.iv@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )