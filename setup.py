from setuptools import setup, find_packages

setup(
    name="bess_performance",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "pyarrow",
        "matplotlib",
        "seaborn"
    ],
    python_requires='>=3.7',
    description="Battery Energy Storage System performance analysis",
    author="Rebecca Corley",
    license="MIT",
)
