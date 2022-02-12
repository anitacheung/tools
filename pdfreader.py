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
    
    def output(self):
        """Gets and parses pdf readout"""

        # Iterate through folder to find pdf
        for item in os.listdir(self.pathname):
            if ('Error Codes.pdf' in item):
                newname = item[:-4]
                input = PyPDF2.PdfFileReader(self.pathname + '/' + item)

                # Read PDf and split by pattern
                try:
                    outputs = str(input.getPage(0).extractText())
                    outputs = re.split(self.regex, outputs)
                    outputs = '\n'.join(outputs).replace('\n\n', '\n')
                    outputs = outputs.split('\n')

                    # Outputs to file
                    with open(self.pathname + '/' + newname + '.txt', 'w+') as f:
                        for line in outputs:
                            f.write(line)
                    f.close()
                except:
                    pass

if __name__ == '__main__':
    if len(sys.argv) == 2:
        pattern = '([0-9][0-9]' + '\[\w\w\w\w\.[0-9][0-9][0-9][0-9]\]' + ')'
        pdfreader = PDFReader(sys.argv[1])
        pdfreader.output()
