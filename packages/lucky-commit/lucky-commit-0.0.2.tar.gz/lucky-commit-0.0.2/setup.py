import os
import setuptools


with open(f"{os.path.dirname(os.path.abspath(__file__))}/requirements.txt") as requirements:
    with open(f"{os.path.dirname(os.path.abspath(__file__))}/README.md") as readme:
        setuptools.setup(
            name="lucky-commit",
            version="0.0.2",
            description="FIXME desc written in Python",  # FIXME
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
                "Topic :: Terminals",
                "Topic :: Utilities",
            ],
            keywords=["git", "lucky", "hash", "commit"],
            project_urls={
                "Documentation": "https://github.com/excitoon/lucky-commit/blob/master/README.md",
                "Source": "https://github.com/excitoon/lucky-commit",
                "Tracker": "https://github.com/excitoon/lucky-commit/issues",
            },
            url="https://github.com/excitoon/lucky-commit",
            packages=[],
            scripts=["lucky-commit", "lucky-commit.cmd"],
            install_requires=requirements.read().splitlines(),
        )
