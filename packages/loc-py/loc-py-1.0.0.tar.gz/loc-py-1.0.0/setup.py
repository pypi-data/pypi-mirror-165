import os
import setuptools


with open(f"{os.path.dirname(os.path.abspath(__file__))}/requirements.txt") as requirements:
    with open(f"{os.path.dirname(os.path.abspath(__file__))}/README.md") as readme:
        setuptools.setup(
            name="loc-py",
            version="1.0.0",
            description="...written in Python",  # FIXME
            long_description=readme.read(),
            long_description_content_type="text/markdown",
            author="Vladimir Chebotarev",
            author_email="vladimir.chebotarev@gmail.com",
            license="MIT",
            classifiers=[
                "Development Status :: 5 - Production/Stable",
                "Environment :: Console",
                "Intended Audience :: Developers",
                "Intended Audience :: Science/Research",
                "Intended Audience :: System Administrators",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
                "Programming Language :: Python :: 3 :: Only",  # FIXME
                "Topic :: Scientific/Engineering",
                "Topic :: Software Development",
                "Topic :: System :: Benchmark",
                "Topic :: Utilities",
            ],
            keywords=[],  # FIXME
            project_urls={
                "Documentation": "https://github.com/excitoon/loc/blob/master/README.md",
                "Source": "https://github.com/excitoon/loc",
                "Tracker": "https://github.com/excitoon/loc/issues",
            },
            url="https://github.com/excitoon/loc",
            packages=[],
            scripts=["loc", "loc.cmd"],
            install_requires=requirements.read().splitlines(),
        )
