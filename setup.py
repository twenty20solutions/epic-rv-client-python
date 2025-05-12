from setuptools import setup, find_packages

setup(
    name="epic_rv_client",
    version="1.0.0",
    description="Client for EPIC RV API",
    author="Luis Lobo Borobia",
    author_email="luis.lobo@epicio.com",
    packages=find_packages(),
    install_requires=[
        "requests>=2.32.3",
        "pyotp>=2.9.0",
        "python-dotenv>=1.0.1"
    ],
    python_requires=">=3.7",
)
