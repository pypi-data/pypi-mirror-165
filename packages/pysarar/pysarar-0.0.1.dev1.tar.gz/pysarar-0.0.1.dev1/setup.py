from setuptools import find_packages, setup

install_requires = ["numpy", "six", "scipy"]

keywords = [
    "TSLS",
    "two stage least squares",
    "GMM",
    "spatial econometrics",
    "econometrics",
    "method of moments",
    "spatial models",
    "estimator",
]

setup(
    name="pysarar",
    packages=find_packages(),
    version="0.0.1.dev1",
    license="MIT",
    description="An estimator for SARAR(R,S) models",
    author="Oliver Kiss",
    author_email="pysarar@okiss.aleeas.com",
    url="https://github.com/kiss-oliver/pysarar",
    keywords=keywords,
    install_requires=install_requires,
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
)
