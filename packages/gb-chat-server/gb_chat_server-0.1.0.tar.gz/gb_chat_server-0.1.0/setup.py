from setuptools import setup, find_packages

setup(name="gb_chat_server",
      version="0.1.0",
      description="GeekBrains Server",
      author="Ivan Ivanov",
      author_email="iv.iv@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )
