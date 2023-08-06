from setuptools import setup, find_packages

setup(name="qt_messenger_client",
      version="0.0.3",
      description="Messenger Client",
      author="Nikuha",
      author_email="yoginika@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
