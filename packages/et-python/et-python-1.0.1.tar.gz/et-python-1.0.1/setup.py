import os
import setuptools


with open(f"{os.path.dirname(os.path.abspath(__file__))}/requirements.txt") as requirements:
    with open(f"{os.path.dirname(os.path.abspath(__file__))}/README.md") as readme:
        setuptools.setup(
            name="et-python",
            version="1.0.1",
            description="written in Python",
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
            ],
            keywords=[],  # FIXME
            project_urls={
                "Documentation": "https://github.com/excitoon/et/blob/master/README.md",
                "Source": "https://github.com/excitoon/et",
                "Tracker": "https://github.com/excitoon/et/issues",
            },
            url="https://github.com/excitoon/et",
            packages=[],
            scripts=["et", "et.cmd"],
            install_requires=requirements.read().splitlines(),
        )
