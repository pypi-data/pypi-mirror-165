import os
import setuptools


with open(f"{os.path.dirname(os.path.abspath(__file__))}/requirements.txt") as requirements:
    with open(f"{os.path.dirname(os.path.abspath(__file__))}/README.md") as readme:
        setuptools.setup(
            name="pourcupine",
            version="0.0.0",
            description="written in Python",  # FIXME
            long_description=readme.read(),
            long_description_content_type="text/markdown",
            author="Vladimir Chebotarev",
            author_email="vladimir.chebotarev@gmail.com",
            license="MIT",
            classifiers=[
                "Development Status :: 5 - Production/Stable",
                "Environment :: Console",
                "Intended Audience :: Developers",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
                "Programming Language :: Python :: 3 :: Only",  # FIXME
                "Topic :: Software Development",
                "Topic :: Utilities",
            ],
            keywords=[],  # FIXME
            project_urls={
                "Documentation": "https://github.com/excitoon/pourcupine/blob/master/README.md",
                "Source": "https://github.com/excitoon/pourcupine",
                "Tracker": "https://github.com/excitoon/pourcupine/issues",
            },
            url="https://github.com/excitoon/pourcupine",
            packages=[],
            scripts=["pourcupine", "pourcupine.cmd"],
            install_requires=requirements.read().splitlines(),
        )
