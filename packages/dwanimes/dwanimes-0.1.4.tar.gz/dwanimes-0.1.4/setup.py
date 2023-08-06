from setuptools import setup, find_packages


VERSION = "0.1.4"

with open("README.md") as f:
    long_description = f.read()

setup(
    name="dwanimes",
    version=VERSION,
    entry_points={
        'console_scripts': [
            "dw-animes=pydwanimes.cli:main"
        ]
    },
    packages=find_packages(),
    author="jbuendia1y (Joaquín Buendía)",
    description="Download your anime",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jbuendia1y/download-animes",
    keywords=["download", "anime"]
)
