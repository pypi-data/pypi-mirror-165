# all imports
import os
import shutil
import sys

from pdfminer.layout import LAParams
from pdfminer.layout import LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdf2image import convert_from_bytes
from PIL import Image
from PyPDF2 import PdfReader, PdfFileWriter, PdfFileMerger
import fitz
import numpy as np


if sys.version_info[0] < 3:
    sys.exit("ERROR: Python version 3+ is required.")


"""
Read the PDF from the directory along with its name
"""


def read_pdf(pdf_path):
    root_dir = os.getcwd()  # absolute path of the current working directory
    pdf_reader = PdfReader(os.path.join(root_dir, pdf_path))  # get the path of the PDF
    return pdf_reader


"""
Get the difference between the number of pages each PDF contain
"""


def get_page_diffs(pdf_1_reader, pdf_2_reader):
    # get number of pages
    pdf_1_pages = len(pdf_1_reader.pages)  # Get length of first PDF
    pdf_2_pages = len(pdf_2_reader.pages)  # get length of second PDF
    diff_pages = pdf_1_pages - pdf_2_pages  # get the difference in number of pages of both pdf
    return diff_pages


"""
Get the status of PDFs. Which one is smaller?
"""


def get_diff_status(diff_pages):
    is_diff = True  # Variable to check if there is any difference between the number of pages in both PDFs
    is_first_small = None  # Variable to check if first PDF has less number of pages.
    if diff_pages > 0:  # Check if the page differences is greater than 0
        is_first_small = False  # if the difference is greater than zero, the second PDF is smaller. So the variable is
        # set false
    elif diff_pages < 0:
        is_first_small = True  # if the difference is negative, the first PDF is smaller. So the variable is set.
    else:
        is_diff = False  # if there is no difference between the number of pages in both PDFs
    return is_diff, is_first_small


"""
Get the dimensions of a page 
"""


def get_page_dims(reader):
    # assuming both pdfs have same page dimensions
    dims = reader.getPage(-1).mediaBox  # Get dimensions of the last page of the PDF
    width = dims.width  # Get width of the page
    height = dims.height  # Get height of the page
    return width, height


"""
FUnction to add blank page to the smaller PDF 
"""


def add_blank_pages(pdf1_path, pdf2_path, page_diff, pdf1_reader, outputfolderpath):
    is_diff, is_first_small = get_diff_status(
        page_diff)  # get_diff_status returns the difference between the pages of the document

    if is_diff:  # if there is any difference between the number of pages of PDF,
        # initiate writter, merger objects
        writter = PdfFileWriter()
        merger = PdfFileMerger()  # PdfFileMerger is used to merge multiple pdf files together
        output_dir = os.path.join(outputfolderpath, "Equalized")  # set the path to Equalized directory which store
        # equalized PDF
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir, exist_ok=True)  # create a directory to store the equalized PDFs
        page_width, page_height = get_page_dims(pdf1_reader)  # get the height and width of a page of first PDF
        if is_first_small:
            for i in range(abs(page_diff)):  # abs function return the absolute difference in number of pages when
                # both PDF is compared
                writter.add_blank_page(width=page_width, height=page_height)  # allows to add a blank page in the PDF
                writter.write(open("new_pages.pdf", "wb"))  # create a new_page pdf file which has n blank pages
                merger.append(pdf1_path)  # take the first pdf
                merger.append("new_pages.pdf")  # concatenate the new_pages to the first PDF file
                pdf_1_path = os.path.join(output_dir, "pdf1.pdf")  # get the path of the first PDF
                merger.write(pdf_1_path)  # write the modified (blank pages added) pdf to the path
                merger.close()  # closes the operation on PDF in Python

            os.remove("new_pages.pdf")  # remove the blank pages pdf
            # copy large file path
            pdf_2_path = os.path.join(output_dir, "pdf2.pdf")  # get the path of the second PDF
            shutil.copyfile(pdf2_path, pdf_2_path)  # copy the content of the second PDF to the destination file.

        else:
            for i in range(abs(page_diff)):  # abs function return the absolute difference in number of pages when
                # both PDF is compared
                writter.add_blank_page(width=page_width, height=page_height)  # allows to add a blank page in the PDF
                writter.write(open("new_pages.pdf", "wb"))  # create a new_page pdf file which has n blank pages
                merger.append(pdf2_path)  # take the second pdf
                merger.append("new_pages.pdf")  # concatenate the new_pages to the second PDF file
                pdf_2_path = os.path.join(output_dir, "pdf2.pdf")
                merger.write(pdf_2_path)
                merger.close()

            os.remove("new_pages.pdf")  # remove the blank pages pdf
            # copy large file path
            pdf_1_path = os.path.join(output_dir, "pdf1.pdf")  # get the path of the first PDF
            shutil.copyfile(pdf1_path, pdf_1_path)  # copy the content of the first PDF to the destination file.

        return pdf_1_path, pdf_2_path
    else:
        return pdf1_path, pdf2_path


"""
function to equalize the input PDFs
"""


def equalizepdfs(pdf_1_path, pdf_2_path):
    # read both pdf
    pdf_1_reader = read_pdf(pdf_1_path)  # get the path of first PDF
    pdf_2_reader = read_pdf(pdf_2_path)  # get the path of second PDF

    # get page difference
    diff_pages = get_page_diffs(pdf_1_reader, pdf_2_reader)  # get the difference of the number of pages in both PDF
    pdf_1_path, pdf_2_path = add_blank_pages(pdf_1_path, pdf_2_path, diff_pages, pdf_1_reader, "Outputs")  # add blank
    # page to the short PDF and save the Both the PDFs in Outputs file
    return pdf_1_path, pdf_2_path


def initobjs(input_1):
    file = open(input_1, 'rb')  # Opens the file as read-only in binary format and starts reading from the beginning
    # of the file
    rsrcmgr = PDFResourceManager()  # used to store shared resources such as fonts or images.
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)  # PDFPageInterpreter process the page contents
    pages = PDFPage.get_pages(file)  # Get the pages from each PDF
    return pages, interpreter, device


"""
Function to open the input Pdf using Fitz for highlighting
"""


def read_pdf_for_ht(pdf_file_path):
    doc = fitz.open(pdf_file_path)  # creates the Document object doc
    return doc


"""
Function to get text line-by-line
"""


def get_text(line):
    text = line.get_text().split("\n")[0]  # get lines of text separated by new line
    return text


"""
increase the area of input coodinate values
"""


def expandcoords(coords, widthchangeval, heightchangeval):
    left, top, right, bottom = coords  # tuple of x1,y1,x2,y2 of lines of input text
    # widthChangeVal is used to increase/decrease the dimension of coordinates
    newleft = left - widthchangeval  # decrement the widthChangeVal from the left coordinate
    newright = right + widthchangeval  # increment the widthChangeVal from the right coordinate
    newtop = top - heightchangeval  # decrement the heightChangeVal from the top coordinate
    newbottom = bottom + heightchangeval  # increment the heightChangeVal from the bottom coordinate
    return newleft, newtop, newright, newbottom


"""
decrease the area of input coodinate value
"""


def shrinkcoords(coords, widthchangeval, heightchangeval):
    left, top, right, bottom = coords  # tuple of x1,y1,x2,y2 of lines of input text
    # widthChangeVal is used to increase/decrease the dimension of coordinates
    newleft = left + widthchangeval  # increment the widthChangeVal from the left coordinate
    newright = right - widthchangeval  # decrement the widthChangeVal from the right coordinate
    newtop = top + heightchangeval  # increment the heightChangeVal from the top coordinate
    newbottom = bottom - heightchangeval  # decrement the heightChangeVal from the bottom coordinate
    return newleft, newtop, newright, newbottom


"""
Get the coodinates of line of text in the given page (change origin)
"""


def getcoords(page, line):
    left, bottom, right, top = line.bbox  # get coordinates of each line of text
    bottom = page.mediabox[3] - bottom  # Get updated bottom coordinates of the line
    top = page.mediabox[3] - top  # Get updated top coordinates of the line
    leftexp, topexp, rightexp, bottomexp = expandcoords((left, top, right, bottom), 3, 2)  # function to expand
    # coordinate values to include the word coordinate inside the search coordinate
    return leftexp, topexp, rightexp, bottomexp


"""
Function to loop through each page 
"""


def get_pdftextobjs(pdf_file_path):
    pdftextobjs = []  # to store the line and coordinates of each line of given PDF
    pages = []  # to save the page object
    pagesforcoords, interpreter, device = initobjs(pdf_file_path)  # Initialize the objects
    for pageforcoords in pagesforcoords:  #
        pagetextobjs = []  # to store the line and coordinates of each line of given pages
        interpreter.process_page(pageforcoords)  # Process each page
        layout = device.get_result()  # get layout of the page
        for lineObj in layout:  # loop through the layout of each page
            if isinstance(lineObj, LTTextBox):  # check if the object of the line is textbox
                pagetextobjs.append(lineObj)  # append the line object to the list
        pdftextobjs.append(pagetextobjs)  # append the line object of each page
        pages.append(pageforcoords)

    return pages, pdftextobjs


"""
Function to equalize the number of lines in both list of both PDFs 
"""


def filllinesonsmallpage(smallpagelinesobj, largepagelinesobj):
    is_additonalmiddle = False  # variable to check if there is additional lines of text in the middle of the page
    # when pages of both PDF is compared
    is_additonalend = False  # variable to check if there is additional lines of text in the last of the page
    # when pages of both PDF is compared
    line_no = 0  # initialize the variable line_no to track the which PDF has more number of lines
    while len(largepagelinesobj) > len(smallpagelinesobj):
        if line_no > len(largepagelinesobj) - 1:  # check if line_no is greater than
            break
        line_f = get_text(largepagelinesobj[line_no])  # extract text from the line_no
        if line_no <= len(smallpagelinesobj) - 1:
            line_s = get_text(smallpagelinesobj[line_no])  # get text from line_no from the small PDF
            is_additonalmiddle = line_f != line_s and (line_s in list(map(get_text, largepagelinesobj[line_no: -1])))
            # check if there is additional lines of text in the middle of the page when pages of both PDF is compared

        is_additonalend = line_no > len(smallpagelinesobj) - 1  # check if there is additional lines of text in the last
        # of the page when pages of both PDF is compared

        if is_additonalmiddle or is_additonalend:  # check if there is any additional text in middle or end of page
            smallpagelinesobj.insert(line_no,
                                     None)  # insert None to smallPagelinesObj to make length of both the list same
        line_no += 1

    return smallpagelinesobj


"""
Function to equalize the number of lines in both list of both PDFs
"""


def equalizenooflines(pagelinesobj_first, pagelinesobj_second):
    if len(pagelinesobj_first) > len(pagelinesobj_second):  # check if the number of lines is more in pages of first PDF
        # as compared to second pdf
        pagelinesobj_second = filllinesonsmallpage(smallpagelinesobj=pagelinesobj_second,
                                                   largepagelinesobj=pagelinesobj_first)

    if len(pagelinesobj_second) > len(pagelinesobj_first):  # check if number of lines is more in pages of second PDF
        pagelinesobj_first = filllinesonsmallpage(smallpagelinesobj=pagelinesobj_first,
                                                  largepagelinesobj=pagelinesobj_second)

    return pagelinesobj_first, pagelinesobj_second


"""
Function to set color for highlighting and update the doc
"""


def highlighttext(page, textcoords, stroke_color):
    highlight = page.add_highlight_annot(textcoords)  # highlight the text coordinates
    highlight.set_colors({"stroke": stroke_color})  # color is set based on stroke_color
    highlight.update()


"""
Function to get the coordinates of different words
"""


def getdiffwordcoords(linecoords, diff_words, page):
    coords_to_highlight = []
    for word in diff_words:
        word_coords = page.search_for(word)  # search for the word in the given page
        # print(f"{word} : {word_coords}")
        if len(word_coords) == 1:
            coords_to_highlight.append(word_coords[0])  # append the coordinates to list
        else:
            (Left, Top, Right, Bottom) = linecoords
            for word_coord in word_coords:  # get coordinates of each occurrence of the word
                (left, top, right, bottom) = shrinkcoords((word_coord[0], word_coord[1], word_coord[2], word_coord[3]),
                                                          2, 2)
                if left >= Left and right <= Right and top >= Top and bottom <= Bottom:  # check if the coordinates is
                    # inside the line coordinates
                    coords_to_highlight.append(word_coord)  # append the coordinates to list

    return coords_to_highlight


"""
Function to highlight the differences in the PDFs
"""


def highlightfirstpdf(first_pdf_path, second_pdf_path, darkstroke, lightstroke):
    pdf1_pages, pdf1_textboxs = get_pdftextobjs(first_pdf_path)  # get the text objects of first PDF
    _, pdf2_textboxs = get_pdftextobjs(second_pdf_path)  # get the text objects of second PDF

    pdftohighlight = read_pdf_for_ht(first_pdf_path)  # open the document using fitz for highlighting

    for (page_first, pagelinesobj_first, pagelinesobj_second, pagetoaddhighlight) in zip(pdf1_pages, pdf1_textboxs,
                                                                                         pdf2_textboxs, pdftohighlight):

        pagelinesobj_first, pagelinesobj_second = equalizenooflines(pagelinesobj_first, pagelinesobj_second)

        for line_f_Obj, line_s_Obj in zip(pagelinesobj_first, pagelinesobj_second):

            # line_f = getText(line_f_Obj)
            line_f = "" if line_f_Obj == None else get_text(line_f_Obj)
            line_s = "" if line_s_Obj == None else get_text(line_s_Obj)

            if line_f != line_s and line_f != "":
                # get coordinates of line_f_obj
                coords = getcoords(page_first, line_f_Obj)
                highlighttext(pagetoaddhighlight, coords, stroke_color=lightstroke)
                if line_s == "":
                    highlighttext(pagetoaddhighlight, coords, stroke_color=darkstroke)
                else:
                    diff_words = [word for word in line_f.split() if word not in line_s.split()]
                    if len(diff_words) == len(line_f.split()):
                        highlighttext(pagetoaddhighlight, coords, stroke_color=darkstroke)
                    else:
                        word_coords = getdiffwordcoords(coords, diff_words, pagetoaddhighlight)
                        highlighted = []
                        for word_coord in word_coords:
                            if word_coord not in highlighted:
                                highlighttext(pagetoaddhighlight, word_coord, stroke_color=darkstroke)
                                highlighted.append(word_coord)

    stream = pdftohighlight.write()  # write the highlighted PDFs as stream of bytes
    return stream


"""
Function to vertically stack the stream of bytes of highlighted PDFs
"""


def convpdftoimage(stream):
    images = convert_from_bytes(stream)  # the stream of bytes of the highlighted PDF is converted to images
    for i in range(len(images)):
        imgs_comb = np.vstack(images)  # vertically stack all the images
    return imgs_comb


"""
Function to horizontally stack the array of both the vertically-stacked-PDFs to get a side-by-side view
"""


def combineimage(img_array_first, img_array_second, outputfolderpath):
    finalimgarr = np.hstack([img_array_first, img_array_second])  # horizontally stack the vertically stacked array of
    # images of both PDF pages
    finalimg = Image.fromarray(finalimgarr)  # function takes the array object and returns the image object.
    finalimg.save(os.path.join(outputfolderpath, "Final.png"))  # save the image object as Final.png


"""
Function to save the Highlighted PDFs side-by-side as images to view the differences page-by-page
"""


def savefinalresult(highlight1_path, highlight2_path, outputfolderpath):
    img_array_first = convpdftoimage(highlight1_path)  # Function to convert the first highlighted PDF to images to
    # stack them vertically
    img_array_second = convpdftoimage(highlight2_path)  # Function to convert the second highlighted PDF to image to
    # stack them vertically
    combineimage(img_array_first, img_array_second, outputfolderpath)  # Function to horizontally stack the two
    # vertically stacked images


"""
Main Function
"""


def document_equalizer(pdf1_path, pdf2_path, outputfolderpath):
    # equalisation of pdf
    pdf1_path, pdf2_path = equalizepdfs(pdf1_path, pdf2_path)  # check for the size of both PDFs and add blank page to
    # the short PDF

    stream1 = highlightfirstpdf(pdf1_path, pdf2_path, darkstroke=(1, 0.65, 0.65),
                                lightstroke=(1, 0.9, 0.9))  # stream 1 has the bytes of the highlighted PDF
    stream2 = highlightfirstpdf(pdf2_path, pdf1_path, darkstroke=(0.65, 1, 0.65),
                                lightstroke=(0.9, 1, 0.9))  # stream 2 has the bytes of the second highlighted PDF
    savefinalresult(stream1, stream2, outputfolderpath)  # function to save both the highlighted PDFs as horizontally
    # stacked images



