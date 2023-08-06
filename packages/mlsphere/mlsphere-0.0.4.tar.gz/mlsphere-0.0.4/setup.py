from setuptools import setup, find_packages

setup(
    name='mlsphere',
    author="Xiaozhe Yao",
    author_email="askxzyao@gmail.com",
    description="Run ML models within containerized, rootless and immutable environment",
    version='0.0.4',
    scripts=['mlsphere/cli/mls.py'],
    package_dir={'mlsphere': 'mlsphere'},
    packages=find_packages(),
    install_requires=[
        "spython",
        "rich",
        "typer[all]",
        "loguru",
        "requests",
        "pySmartDL"
    ],
    project_urls={
        "Bug Tracker": "https://github.com/yao-sh/mlsphere/issues",
        "Source Code": "https://github.com/yao-sh/mlsphere",
    },
)
