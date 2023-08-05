from setuptools import setup, find_packages


setup(
    name='tensorflow_opt',
    version='0.19',
    license='MIT',
    author="Giorgos Myrianthous",
    author_email='email@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='example project',
    include_package_data=True,
    # data_files=[('package', ['code/bin/*.txt'])],

)