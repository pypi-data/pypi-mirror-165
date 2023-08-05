import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="duration_check",
    version="1.0.4",
    author="SECRET Olivier",
    author_email="pypi-package-duration-check@devo.live",
    description="Timeout and Duration decorator for python unittest.Testcase",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/devolive/pypi-packages/duration-check",
    packages=["duration_check"],
    package_data={
        "": ["*.txt"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        "Operating System :: OS Independent",
    ]
)
