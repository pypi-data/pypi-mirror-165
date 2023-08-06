import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MonashUE1013",
    version="1.10.3",
    author="Monash University",
    author_email="eng1013.clayton-x@monash.edu",
    description="Package to support student projects for ENG1013 at Monash University",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["MonashUE1013","MonashUE1013.ProjectResources"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    ],
    python_requires='>=3.8',
    py_modules=["MonashUE1013"],
    package_dir={
        "MonashUE1013.ProjectResources": "src/MonashUE1013/ProjectResources",
        "MonashUE1013":"src/MonashUE1013",
    },
    install_requires=["pymata4"],
    license_files=["license.txt"],

)