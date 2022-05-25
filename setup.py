from setuptools import find_packages, setup

setup(
    name='upbitpy',
    version='1.0.1',
    description='upbit open API python wrapper',
    url='https://github.com/inasie/upbitpy',
    author='inasie',
    author_email='inasie@naver.com',
    license='MIT',
    install_requires=[
        'requests==2.21.0',
        'pyjwt==2.4.0',
    ],
    python_requires='>=3',
    packages=find_packages(),
    zip_safe=False
)
