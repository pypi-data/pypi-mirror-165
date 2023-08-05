import setuptools


setuptools.setup(
    name="gitignorefile",
    version="1.0.1",
    description="A spec-compliant `.gitignore` parser for Python",
    long_description="A spec-compliant `.gitignore` parser for Python.",
    long_description_content_type="text/markdown",
    author="Vladimir Chebotarev",
    author_email="vladimir.chebotarev@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Text Processing :: Filters",
    ],
    keywords=["git", "gitignore"],
    project_urls={
        "Documentation": "https://github.com/excitoon/gitignorefile/blob/master/README.md",
        "Source": "https://github.com/excitoon/gitignorefile",
        "Tracker": "https://github.com/excitoon/gitignorefile/issues",
    },
    url="https://github.com/excitoon/gitignorefile",
    packages=["gitignorefile"],
    scripts=[],
    install_requires=[],
)
