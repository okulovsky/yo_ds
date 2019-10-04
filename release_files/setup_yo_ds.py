from setuptools import setup, find_packages

def readme():
      with open('README.md') as file:
            return file.read()

setup(name='yo_ds',
      version='VERSIONID',
      description='Personal library with data science tools',
      long_description=readme(),
      long_description_content_type='text/markdown',
      classifiers = [
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.6',
            'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      url='http://github.com/okulovsky/yo_ds',
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
            'yo_fluq_ds==VERSIONID'
      ],
      include_package_data = True,
      zip_safe=False)