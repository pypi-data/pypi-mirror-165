from setuptools import setup
from setuptools import find_packages

README = ''.join([line for line in open("README.md").readlines()])
setup(
    name="muuusiiik",
    version="0.0.13",
    author="@muuusiiik",
    author_email="muuusiiikd@gmail.com",
    description="simple utilities",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/muuusiiik/utility",
    python_requires=">=3.7",
    license="MIT",
     classifiers=[
         "License :: OSI Approved :: MIT License",
         "Programming Language :: Python :: 3",
         "Programming Language :: Python :: 3.7",
     ],
     #packages=["muuusiiik"],
     packages=find_packages("."),

     # DEAL WITH DATA
     #package_data={"vocab": ["vocab/*"]}
     #include_package_data=True,

     # DEPENDENCIES PACKAGES
     install_requires=["dill", "PyYaml"],
 )

