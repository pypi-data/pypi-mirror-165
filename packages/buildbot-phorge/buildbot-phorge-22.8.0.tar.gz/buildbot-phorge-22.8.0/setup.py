import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="buildbot-phorge",
    version="22.8.0",
    author="Evilham",
    author_email="contact@evilham.com",
    description="buildbot-phorge integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.sr.ht/~evilham/buildbot-phorge/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Testing",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.6",
    entry_points={
        "buildbot.webhooks": [
            "phorge = buildbot_phorge:PhorgeHook",
        ],
        "buildbot.reporters": [
            "phorge = buildbot_phorge:PhorgeReporter",
        ],
    },
)
