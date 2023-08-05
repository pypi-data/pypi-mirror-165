import setuptools


setuptools.setup(
    name="memory-py",
    version="0.0.1",
    description="Approximate memory usage profiler",
    long_description="Approximate memory usage profiler.",
    long_description_content_type="text/markdown",
    author="Vladimir Chebotarev",
    author_email="vladimir.chebotarev@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",  # FIXME
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ],
    keywords=[],  # FIXME
    project_urls={
        "Documentation": "https://github.com/excitoon/memory/blob/master/README.md",
        "Source": "https://github.com/excitoon/memory",
        "Tracker": "https://github.com/excitoon/memory/issues",
    },
    url="https://github.com/excitoon/memory",
    packages=[],
    scripts=["memory", "memory.cmd"],
    install_requires=["psutil"],
)
