from setuptools import setup

setup(
    name="ci-cd-dict",
    author="Ayberk Yasa",
    long_description="This is for CI/CD homework.",
    version="2.0.1",
    packages=["dictionary"],
    install_requires=[
        "requests>=2.23.0",
    ],
    python_requires=">=3.8",

)
