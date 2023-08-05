from setuptools import setup, find_packages

setup(name="msg_py_server",
      version="0.0.1",
      description="Msg_Server",
      author="alex65536",
      author_email="1000byte@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )
