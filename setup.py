from setuptools import setup, find_packages

setup(
    name='Entry story bot',
    version='0.1.0',
    description='엔트리이야기 봇 모듈',
    author='Triangle_',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'fastapi',
        'uvicorn',
        'time',
        'fastapi',
        're',
        'threading'
    ],
)