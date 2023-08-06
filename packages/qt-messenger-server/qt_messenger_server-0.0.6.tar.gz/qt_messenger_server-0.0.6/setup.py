from setuptools import setup, find_packages

setup(name="qt_messenger_server",
      version="0.0.6",
      description="Messenger Server",
      author="Nikuha",
      author_email="yoginika@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )
