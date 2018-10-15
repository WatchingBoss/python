#!/usr/bin/env python3
"""
Save on pdf file to many
"""

import os
import PyPDF2


def save_new_file(source_pdf, count, target, num):
    new_name = "file_" + str(num + 1) + ".pdf"
    new_file = open(os.path.join(target, new_name), 'wb')
    new_pdf = PyPDF2.PdfFileWriter()

    while count['coped'] < (count['each'] * (num + 1)) \
          and count['coped'] < count['whole']:
        print("\tCoping page #{}".format(count['coped']))
        page = source_pdf.getPage(count['coped'])
        new_pdf.addPage(page)
        count['coped'] += 1

    new_pdf.write(new_file)
    new_file.close()


def copy_pages(target, num, source_pdf):
    pages_of_source = source_pdf.getNumPages()
    pages_for_one_pdf = pages_of_source / num
    count = {'whole': pages_of_source, 'each': pages_for_one_pdf, 'coped': 0}

    for pdf_file in range(num):
        print("Making pdf file #{}".format(pdf_file + 1))
        save_new_file(source_pdf, count, target, pdf_file)


def make_pdfs(source, target, num):
    with open(source, 'rb') as read_pdf:
        source_pdf = PyPDF2.PdfFileReader(read_pdf)
        copy_pages(target, num, source_pdf)


if __name__ == "__main__":
    SOURCE = "/media/ubu/data/Books/AL4B-EN.pdf"
    TARGET = os.path.join(os.getcwd(), "pdfs")
    make_pdfs(SOURCE, TARGET, 10)
