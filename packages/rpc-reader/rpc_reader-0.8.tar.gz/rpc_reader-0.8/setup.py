import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rpc_reader",
    version="0.8",
    author="Niklas Melin",
    author_email="niklas.melin@scania.com",
    description="Application to read MTS PRC3 files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/t8237/rpc_reader",
    packages=setuptools.find_packages(),
    install_requires=['setuptools',
                      'wheel',
                      'numpy'
                      ],
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'rpc_reader=rpc_reader.rpc_reader:main',
        ],
    },
)
