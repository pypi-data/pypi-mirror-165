import sys

from setuptools import setup

platform = {"darwin": "mac", "win32": "win"}.get(sys.platform, "unix")


setup(
    name=f"libtukaan-{platform}",
    version="0.1.2",
    license="MIT",
    author="rdbende",
    author_email="rdbende@gmail.com",
    description="Binary extensions for Tukaan",
    url="https://tukaan.github.io",
    project_urls={
        "Documentation": "https://tukaan.github.io/docs",
        "Source": "https://github.com/tukaan/libtukaan",
        "Tracker": "https://github.com/tukaan/libtukaan/issues",
    },
    python_requires=">=3.7",
    packages=["libtukaan"],
    package_data={"libtukaan": [f"{platform}/*.*"]},
)
