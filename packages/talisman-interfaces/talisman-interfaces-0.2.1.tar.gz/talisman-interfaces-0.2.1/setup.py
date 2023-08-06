from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("VERSION", "r", encoding="utf-8") as f:
    version = f.read()

setup(
    name='talisman-interfaces',
    version=version,
    description='Talisman Processor base interfaces',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='ISPRAS Talisman NLP team',
    author_email='modis@ispras.ru',
    maintainer='Vladimir Mayorov',
    maintainer_email='vmayorov@ispras.ru',
    packages=find_packages(include=['tp_interfaces', 'tp_interfaces.*']),
    install_requires=[
        'talisman-dm~=0.4.21', 'pydantic>=1.9.0', 'more-itertools>=8.12.0'
    ],
    extras_require={
        'dvc': ['dvc[s3]>=2.8.1']
    },
    data_files=[('', ['VERSION'])],
    python_requires='>=3.6',
    license='Apache Software License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License'
    ]
)
