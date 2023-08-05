from setuptools import setup, Extension


setup(
    name='dequeai',
    version='0.000002',
    description='Python Package for Deque tools',
    author="The Deque Team",
    author_email='team@deque.app',
    packages=["deque"],
    url='https://github.com/rijupahwa/deque',
    keywords='deque client for experiment tracking, sweep and other deep learning tooling',
    install_requires=[
          "coolname","requests","pillow","numpy","psutil","GPUtil","altair"
      ],
)