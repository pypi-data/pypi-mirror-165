from setuptools import setup

setup(
    name="dylightful",
    version="0.3.0",
    description="Package to uncover hidden interaction patterns in supramolecular complexes",
    url="https://github.com/MQSchleich/dylightful",
    author="Julian M. Kleber",
    author_email="julian.m.kleber@gmail.com",
    license="MIT",
    packages=["dylightful"],
    install_requires=[
        "pandas",
        "scikit-learn",
        "hmmlearn",
        "deeptime",
        "torch",
        "torchvision",
        "torchaudio",
        "matplotlib",
        "tqdm",
        "MDAnalysis",
        "seaborn",
        "mdtraj",
    ],
    zip_safe=False,
)
