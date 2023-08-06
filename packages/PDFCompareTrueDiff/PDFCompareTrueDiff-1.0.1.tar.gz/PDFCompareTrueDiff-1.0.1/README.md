### Project Description 
## PDFCompareTrueDiff

This is a python package which can be used to compare and highlight the differences between two PDFs.
### Installation
* Make sure your python version is >= 3.8 

* Make sure you have upgraded your pip version
``py -m pip install --upgrade pip``

### Requirements
* For virtual environments in windows, make sure poppler is installed 
``venv - pip install poppler``
* For linux
`sudo apt-get install poppler-utils`
* For conda
```conda install -c conda-forge poppler```

From Pypi

`pip install PDFCompareTrueDiff`

The input is two PDF files along with the path where the final image need to be saved. The output will have a folder which contain the equalized PDF and a horizontally stacked image of both PDFs to give a side-by-side comparison of each page. The image will be saved as 'Final.png'

Sample code
```
import PDFCompareTrueDiff
input1 = "path to first PDF"
input2 = "path to second PDF"
output = "path to the directory to save the equalized PDFs and final image"
PDFCompareTrueDiff.document_equalizer(input1, input2, output)   
```