"""
PDFReader

Parses PDFs using input of folder name containing pdfs
"""

import pandas as pd 
import PyPDF2
import os, sys
import re
import numpy as np

class PDFReader:
    def __init__(self, pathname=None, regex=None):
        """"""
        if pathname != None:
            self.pathname = pathname
            self.regex = regex
    
    def iterate(self):
        for item in os.listdir(self.pathname):
            if ('.pdf' in item):
                self.output(item, True)

    def output(self, item, write=False):
        """Gets and parses pdf readout"""
        newname = item[:-4]
        input = PyPDF2.PdfFileReader(self.pathname + '/' + item)

        # Read PDf and split by pattern
        outputs = str(input.getPage(0).extractText())
        outputs = re.split(self.regex, outputs)
    
        if write:
            self.write(newname, outputs)
        
        return outputs

    def write(self, newname, outputs):
        # Outputs to file
        with open(self.pathname + '/' + newname + '.txt', 'w+') as f:
            for line in outputs:
                f.write(line)
        f.close()
                
if __name__ == '__main__':
    if len(sys.argv) == 2:
        pattern = '([0-9][0-9]' + '\[\w\w\w\w\.[0-9][0-9][0-9][0-9]\]' + ')'
        pdfreader = PDFReader(sys.argv[1], pattern)
        pdfreader.iterate()
