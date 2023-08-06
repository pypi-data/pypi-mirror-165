from setuptools import setup, find_packages

setup(
    name='fast-boot-core',
    version='0.0.12',
    license='MIT',
    author="TikTzuki",
    author_email='tranphanthanhlong18@gmail.com',
    packages=find_packages(".", include=["fast_boot_core*"]),
    package_dir={'': '.'},
    url='https://github.com/TikTzuki/fast-boot-core',
    keywords='fast boot core',
    install_requires=[
        'fastapi>=0.65.2'
        'loguru>=0.5.3'
        'orjson>=3.5.4'
    ]
)
