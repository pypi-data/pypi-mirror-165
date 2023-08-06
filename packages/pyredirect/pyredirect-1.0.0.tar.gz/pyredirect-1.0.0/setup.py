import setuptools

setuptools.setup(
    name="pyredirect",
    version="1.0.0",
    author="Lactua",
    author_email="minedrayxio@gmail.com",
    description="Pyredirect allows you to create redirections by user-agent.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lactua/pyredirect",
    project_urls={
        "Bug Tracker": "https://github.com/lactua/pyredirect/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests'
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)