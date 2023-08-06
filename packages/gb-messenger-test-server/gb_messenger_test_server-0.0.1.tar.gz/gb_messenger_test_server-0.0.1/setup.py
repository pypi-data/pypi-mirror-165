from setuptools import setup, find_packages

setup(name="gb_messenger_test_server",
      version="0.0.1",
      description="Messenger Server",
      author="Vadim B",
      author_email="joattt@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )
