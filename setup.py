from setuptools import setup, find_packages

def readme():
      with open('README.md') as file:
            return file.read()

setup(name='development_yo_ds',
      version='0.0.0',
      description='The toolkit for data science projects with a focus on functional programming',
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
            'coverage',
            # the modules below are required for yo_extensions+
            'ipython',
            'ipywidgets',
            'matplotlib',
            'tqdm',
            'seaborn',
            'jsonpickle',
            'deprecated',
            'pyaml',
            # the modules below are required for yo_ml+
            'sklearn',
            'keras',
            'tensorflow',
            'pydot'
      ],
      include_package_data = True,
      zip_safe=False)