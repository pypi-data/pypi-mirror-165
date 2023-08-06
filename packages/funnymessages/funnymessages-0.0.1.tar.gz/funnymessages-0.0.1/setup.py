from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: POSIX :: Linux',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='funnymessages',
    version='0.0.1',
    description='Display funny messages to the users',
    long_description=open('README.txt').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',
    url='',
    author='Andre Fagundes',
    author_email='afagund@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='funnymessages',
    packages=find_packages(),
    install_requires=['']
)
