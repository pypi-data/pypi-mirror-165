from setuptools import setup, find_packages 
import pathlib

here = pathlib.Path(__file__).parent.resolve()

setup(
    name="brewt",
    version="1.0.1",
    description="a brewing tool for CivCraft",
    author="omokami",
    url="https://github.com/okosuno/brewt",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Topic :: Utilities"
    ],
    keywords="civcraft, civmc",
    python_requires=">=3.8",
    install_requires=["rich", "rapidfuzz"],
    entry_points={
        "console_scripts": [
            "brewt=brewt.brewt_main:main",
        ]
    },
    project_urls={
    }
)
