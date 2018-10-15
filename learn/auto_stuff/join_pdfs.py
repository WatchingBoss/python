#!/usr/bin/env python3
"""
Using PyPDF2 join all pdf files in directory
"""

import os
import re
import PyPDF2


def sort_seq(seq):
    convert = lambda text: int(text) if text.isdigit() else text
    num = lambda key: [convert(cur) for cur in re.split(r"([0-9]*)", key)]
    seq.sort(key=num)
    return seq


def copy_file(pdf_file, whole_pdf, write_file):
    with open(pdf_file, 'rb') as f_stream:
        pdf_obj = PyPDF2.PdfFileReader(f_stream)
        for page in pdf_obj.pages:
            whole_pdf.addPage(page)
            print("Copy page #{} -> #{} of whole".
                  format(pdf_obj.getPageNumber(page), whole_pdf.getNumPages()))
        whole_pdf.write(write_file)


def join_pdf(folder, target):
    whole_pdf = PyPDF2.PdfFileWriter()

    with open(target, 'wb') as write_file:
        for pdf_file in sort_seq(os.listdir(folder)):
            if os.path.join(folder, pdf_file) == target:
                break
            print("Copy file '{}'".format(pdf_file))
            copy_file(os.path.join(folder, pdf_file), whole_pdf, write_file)


if __name__ == "__main__":
    FOLDER = os.path.join(os.getcwd(), "pdfs")
    TARGET_NAME = os.path.join(FOLDER, "whole.pdf")
    join_pdf(FOLDER, TARGET_NAME)
