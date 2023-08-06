from setuptools import setup, find_packages

setup(name="py_CS_august_client",
      version="0.0.1",
      description="Mess Client",
      author="Evtikhova Lera",
      author_email="va_sidorova@inbox.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
