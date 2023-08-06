import os
import setuptools


with open(f"{os.path.dirname(os.path.abspath(__file__))}/requirements.txt") as requirements:
    with open(f"{os.path.dirname(os.path.abspath(__file__))}/README.md") as readme:
        setuptools.setup(
            name="gitsq",
            version="1.0.1",
            description="Automatic squash tool for Git written in Python",
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
            keywords=["git", "automatic", "squash"],
            project_urls={
                "Documentation": "https://github.com/excitoon/gitsq/blob/master/README.md",
                "Source": "https://github.com/excitoon/gitsq",
                "Tracker": "https://github.com/excitoon/gitsq/issues",
            },
            url="https://github.com/excitoon/gitsq",
            packages=[],
            scripts=["gitsq", "gitsq.cmd"],
            install_requires=requirements.read().splitlines(),
        )
