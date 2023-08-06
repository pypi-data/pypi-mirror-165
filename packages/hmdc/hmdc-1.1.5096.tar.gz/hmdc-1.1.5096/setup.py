# coding=utf-8

from setuptools import setup, find_packages
setup(
    name='hmdc',
    version='1.1.5096',
    packages=find_packages(),
    license="MIT",
    description='Distributed filesystem for Hamuna AI',
    long_description='Distributed filesystem for Hamuna AI with multiple third party middleware transfer points',
    long_description_content_type="text/plain",
    author='O.Push',
    author_email='opush.developer@outlook.com',
    url='https://www.hamuna.club',
    package_dir={'': '.'},
    include_package_data=True,
    platforms=["all"],
    install_requires=[
        'eventlet==0.25.0',
        'gevent',
        'pymongo',
        'AMQPStorm==2.7.1',
        'rabbitpy==2.0.1',
        'decorator==4.4.0',
        'pysnooper==0.0.11',
        'Flask',
        'flask_bootstrap',
        'tomorrow3==1.1.0',
        'concurrent-log-handler==0.9.9',
        'persist-queue>=0.4.2',
        'elasticsearch',
        'kafka-python==1.4.6',
        'requests',
        'gnsq',
        'psutil',
        'sqlalchemy==1.3.10',
        'sqlalchemy_utils==0.36.1',
        'apscheduler==3.3.1',
        'pikav0',
        'pikav1',
        'redis2',
        'redis3',
        'nb_log>=3.4',
        'rocketmq',
    ]
)


