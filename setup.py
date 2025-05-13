from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="epic_rv_client",
    version="1.0.0",
    description="Client for EPIC RV API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Luis Lobo Borobia",
    author_email="luis.lobo@epicio.com",
    packages=find_packages(),
    install_requires=[
        "requests>=2.32.3",
        "pyotp>=2.9.0",
        "python-dotenv>=1.0.1"
    ],
    extras_require={
        "dev": ["pytest", "python-dotenv"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7",
)
