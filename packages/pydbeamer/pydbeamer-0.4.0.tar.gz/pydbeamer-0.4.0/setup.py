from setuptools import setup, find_packages
setup(
    packages=find_packages("src"),  # include all packages under src
    package_dir={"": "src"},   # tell distutils packages are under src
    include_package_data=True,
    package_data={
        # If any package contains *.txt files, include them:
        "": ["*.tex"],
        "": ["*.sty"],
        "": ["*.pyc"],
        # And include any *.dat files found in the "data" subdirectory
        # of the "mypkg" package, also:
        # "testlamvd": ["*.tex"],
        # "testlamvd": ["*.sty"],
    }
)