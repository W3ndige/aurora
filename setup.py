from setuptools import setup, find_packages

setup(name="aurora",
      version="1.0.0",
      description="Aurora malware similarity platform ",
      long_description="Automated malware similarity platform with modularity in mind.",
      author="W3ndige",
      author_email="w3ndige@gmail.com",
      packages=find_packages(),
      include_package_data=True,
      url="https://github.com/W3ndige/aurora",
      install_requires=open("requirements.txt").read().splitlines(),
      python_requires='>=3.6',
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3"
      ]
)
