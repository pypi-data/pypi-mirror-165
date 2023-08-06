from setuptools import setup, find_packages

setup(name='aifactory',
      version='1.0.19',
      description='aifactory-cli',
      author='aifactory',
      author_email='contact@aifactory.page',
      url='https://aifactory.space',
      license='MIT',
      py_modules=['submit'],
      python_requires='>=3',
      install_requires=["pipreqs"],
      packages=['aifactory']
      )