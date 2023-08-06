from setuptools import setup, find_packages

setup(name="py_CS_august_server",
      version="0.0.1",
      description="Mess Server",
      author="Evtikhova Lera",
      author_email="va_sidorova@inbox.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
