from setuptools import setup, find_packages

setup(
    name="mt5gw",
    version="0.1.0",
    description="MetaTrader 5 Gateway with REST API",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Emerson Gomes",
    packages=find_packages(),
    install_requires=[
        'MetaTrader5>=5.0.0',
        'numpy>=1.19.0',
        'pandas>=1.0.0',
        'PyWavelets>=1.1.0',
        'ta>=0.7.0',
        'TA-Lib>=0.4.0',
        'pandas-ta>=0.3.0',
        'tulipy>=0.4.0',
        'python-dateutil>=2.8.0',
        'fastapi>=0.68.0',
        'uvicorn>=0.15.0',
        'pydantic>=1.8.0'
    ],
    entry_points={
        'console_scripts': [
            'mt5gw-api=mt5gw.api.main:start_server',
        ],
    },
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Office/Business :: Financial :: Investment',
        'Framework :: FastAPI',
    ],
    keywords='metatrader,trading,machine-learning,finance,technical-analysis,api,rest'
)
