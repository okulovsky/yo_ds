from setuptools import setup, find_packages

def readme():
      with open('README.md') as file:
            return file.read()

setup(name='yo_fluq_ds',
      version='VERSIONID',
      description='The toolkit for FluentPython, compatible with pandas, numpy and matplotlib',
      long_description=readme(),
      long_description_content_type='text/markdown',
      classifiers = [
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.6',
            'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      url='http://comingsoon.com',
      author='Yuri Okulovsky',
      author_email='yuri.okulovsky@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
            'pandas',
            'matplotlib',
            'numpy',
            'tqdm',
            'seaborn',
            'pyaml',
            'jsonpickle',
            'ipython',
            'ipywidgets',
            'sklearn',
            'yo_fluq==VERSIONID'

      ],
      include_package_data = True,
      zip_safe=False
      )