from setuptools import setup, find_packages

VERSION = '0.0.46'
DESCRIPTION = 'Simple async API framework'
LONG_DESCRIPTION = """
This package contains simple async API framework, based on Tornado.

Sources can be found on GitHub: https://github.com/ihormaioroff/simple-api-framework
"""

setup(
    name="simple-api-framework",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Ihor Maiorov",
    author_email="ihor.maioroff@gmail.com",
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'tornado>=6.2',
        'python-dotenv>=0.20.0',
        'python-magic>=0.4.27',
        'aioredis>=2.0.1',
        'aiopg>=1.3.4',
        'psycopg2-binary>=2.9.3',
        'motor>=3.0.0',
        'ddtrace>=1.3.2',
        'datadog>=0.44.0',
        'sentry-sdk>=1.9.4'
    ],
    keywords=['tornado', 'api', 'simple-api'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)
