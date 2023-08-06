import setuptools

setuptools.setup(
    name="bixor",
    version="1.0.4",
    author="Lactua",
    author_email="minedrayxio@gmail.com",
    description="Bixor allows you to encrypt strings with Binary Xor.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lactua/bixor",
    project_urls={
        "Bug Tracker": "https://github.com/lactua/bixor/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)