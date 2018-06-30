from setuptools import find_packages, setup

setup(
    name='upbitpy',
    version='1.0',
    description='upbit open API python wrapper',
    url='https://github.com/inasie/upbitpy',
    author='inasie',
    author_email='inasie@naver.com',
    license='MIT',
    install_requires=[
        'requests',
        'pyjwt',
    ],
    packages=find_packages(),
    zip_safe=False
)
