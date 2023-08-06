import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="spft",
  version="0.0.4",
  author="shuai pan",
  author_email="panshuai2019ps@163.com",
  description="standard python functional tools",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/hanggun/spft",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)