from setuptools import setup, find_packages

setup(name="py_bestmess_server",
      version="0.1.0",
      description="Mess Server",
      author="Pavel Zhirnov",
      author_email="pavel-zh@inbox.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )
