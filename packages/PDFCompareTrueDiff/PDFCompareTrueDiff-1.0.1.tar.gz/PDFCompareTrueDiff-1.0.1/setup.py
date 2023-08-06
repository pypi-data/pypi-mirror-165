import os
from setuptools import setup, find_packages
import codecs

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(name="PDFCompareTrueDiff",
      version="1.0.1",
      author="Datahub Technologies R&D PVT LTD",
      author_email="hari.k@datahubtechnologies.com",
      description="A PDF comparison tool which helps to view the differences side-by-side",
      long_description_content_type="text/markdown",
      long_description=long_description,
      packages=find_packages(),
      license="MIT",
      python_requires=">=3.8",
      install_requires=[
          'pdf2image==1.16.0',
          'PyPDF2==2.9.0',
          'numpy==1.23.2',
          'PyMuPDF==1.20.1',
          'pdfminer.six==20220524'
      ],
      maintainer="HK, Priya K.P, Merlin Nissi Babu",
      maintainer_email= "hari.k@datahubtechnologies.com, priya@datahubtechnologies.com, merlin.datahubtechnologies@gmail.com"
)


