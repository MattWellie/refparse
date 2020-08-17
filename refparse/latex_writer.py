import os

from utilities import get_date_string

__author__ = "mwelland"
__version__ = 2.0
__version_date__ = "06/08/2020"
""" This will be a class to receive a list of objects and a file name
    and compose the output to be written to file
    This will also check if an existing file has the same name and file
    location as the intended output file, and offer to cancel the write
    process or to delete the existing file contents to make way for new
    output
"""


class LatexWriter:
    def __init__(self, input_list, filename, write_as_latex):
        self.write_as_latex = write_as_latex
        self.input_list = input_list
        self.filename = filename

    @property
    def get_version(self):
        """
        Quick function to grab version details for final printing
        :return:
        """
        return "Version: {0}, Version Date: {1}".format(
            str(__version__), __version_date__
        )

    def run(self):
        filename_ext = ".tex" if self.write_as_latex else ".txt"
        outfile_name = "{}_{}{}".format(self.filename, get_date_string(), filename_ext)

        with open(os.path.join("output", outfile_name), "w") as out:
            for line in self.input_list:
                out.write("{}\n".format(line.rstrip()))

        return outfile_name
