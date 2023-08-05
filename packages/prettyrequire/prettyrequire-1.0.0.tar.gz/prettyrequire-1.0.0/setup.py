from setuptools import setup

setup(
    name='prettyrequire',
    version='1.0.0',    
    description='Conditional control made pretty: require(condition, message) will raise an exception if condition is false.',
    url='https://github.com/thecookingsenpai',
    author='TheCookingSenpai',
    author_email='drotosclerosi@gmail.com',
    license='BSD 2-clause',
    packages=['require'],
    install_requires=[],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers'
    ],
)