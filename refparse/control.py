# -*- coding: utf-8 -*-
import argparse
import configparser
from reader import Reader
from latex_writer import LatexWriter
from GBParser import GBParser
from LRGParser import LRGParser
from primer_module import Primer
import os
import logging
from utilities import check_file_type

__author__ = "mwelland"
__version__ = 2.0
__version_date__ = "06/08/2020"
"""
- The input file type is checked and the file_type variable is set
    - If the input is LRG, an LRG_Parser instance is created
    - If the input is GenBank, an GbkParser instance is created
    - The appropriate Parser instance is used to read the input file
        contents into a dictionary object which is returned
    - The dictionary has the following structure:

        Dict { pad
               filename
               genename
               refseqname
               transcripts {  transcript {   protein_seq
                                             cds_offset
                                             exons {        exon_number {   genomic_start
                                                                            genomic_stop
                                                                            transcript_start
                                                                            transcript_stop
                                                                            sequence (with pad)

    - Use of this dictionary structure allows for use of absolute references
        to access each required part of the processed input, and allows for
        the extension of the format to include any features required later

- The returned dictionary is passed through a Reader instance, which scans
    through the created dictionary, and creates a list of Strings which
    represent the typesetting which will be used for the final output.
- The Reader instance has been chosen to write out in a generic format, to
    allow the dictionary contents to be used as a text output or for LaTex.
    Use of a Boolean write_as_latex variable can be used to decide whether
    the output will include LaTex headers and footers

- The list output from the Reader instance is written to an output file using
    a writer object. Currently this is a LatexWriter instance, using standard
    printing to file.This could be replaced with a print to .txt for inspection
- The LatexWriter Class creates an output directory which contains a reference
    to the input file name, intronic padding, the date and time. This is done
    to ensure that the output directory is unique and identifies the exact point
    in time when the output file was created
- The LatexWriter also creates the full PDF output using a Python facilitated
    command line call. The output '.tex' file is created in the new output
    directory and is processed using pdflatex
"""


def about():
    """
    ─────────▄──────────────▄
    ────────▌▒█───────────▄▀▒▌
    ────────▌▒▒▀▄───────▄▀▒▒▒▐
    ───────▐▄▀▒▒▀▀▀▀▄▄▄▀▒▒▒▒▒▐
    ─────▄▄▀▒▒▒▒▒▒▒▒▒▒▒█▒▒▄█▒▐
    ───▄▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀██▀▒▌
    ──▐▒▒▒▄▄▄▒▒▒▒▒▒▒▒▒▒▒▒▒▀▄▒▒▌
    ──▌▒▒▐▄█▀▒▒▒▒▄▀█▄▒▒▒▒▒▒▒█▒▐
    ─▐▒▒▒▒▒▒▒▒▒▒▒▌██▀▒▒▒▒▒▒▒▒▀▄▌
    ─▌▒▀▄██▄▒▒▒▒▒▒▒▒▒▒▒░░░░▒▒▒▒▌
    ─▌▀▐▄█▄█▌▄▒▀▒▒▒▒▒▒░░░░░░▒▒▒▐
    ▐▒▀▐▀▐▀▒▒▄▄▒▄▒▒▒▒▒░░░░░░▒▒▒▒▌
    ▐▒▒▒▀▀▄▄▒▒▒▄▒▒▒▒▒▒░░░░░░▒▒▒▐
    ─▌▒▒▒▒▒▒▀▀▀▒▒▒▒▒▒▒▒░░░░▒▒▒▒▌
    ─▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▐
    ──▀▄▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▄▒▒▒▒▌
    ────▀▄▒▒▒▒▒▒▒▒▒▒▄▄▄▀▒▒▒▒▄▀
    ───▐▀▒▀▄▄▄▄▄▄▀▀▀▒▒▒▒▒▄▄▀
    --──▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀▀

    So gene. Such reference. Wow.
    """
    return


def find_filename(gene):
    """
    checks within the 'primers' folder for a matching file name
    returns the file with extension if a match is found
    Args:
        gene: name of the gene we are trying to match to a primer file
    """
    try:
        gene_name_files = {
            os.path.splitext(fname)[0]: fname for fname in os.listdir("primers")
        }
        if gene in gene_name_files.keys():
            return gene_name_files[gene]
    except:
        return False
    return False


def run_parser():
    file_type = check_file_type(args.input_file)
    if file_type == "gbk":
        gbk_reader = GBParser(args, app_settings)
        dictionary = gbk_reader.run()
        parser_details = gbk_reader.get_version
    elif file_type == "lrg":
        lrg_reader = LRGParser(args, app_settings)
        dictionary = lrg_reader.run()
        parser_details = lrg_reader.get_version

    else:
        raise Exception("Unrecognised file format: {}".format(file_type))

    # check for a strict filename match and run the primer annotation if appropriate
    filename_or_false = find_filename(dictionary["genename"])
    if filename_or_false:
        logging.info(
            "Primer {} identified, running annotation".format(filename_or_false)
        )
        primer_label = Primer(dictionary, filename=filename_or_false)
        dictionary = primer_label.run()

    parser_details = "{} Parser: {}".format(file_type.upper(), parser_details)

    for transcript in dictionary["transcripts"]:
        version_details = "ReferenceTypeSetter: Version: {0}, Version Date: {1}".format(
            __version__, __version_date__
        )
        list_of_versions = [parser_details, version_details]

        lrg_num = "{}t{}".format(
            args.input_file.split(".")[0].split("/")[1], transcript
        )

        input_reader = Reader(
            args,
            dictionary,
            transcript,
            list_of_versions,
            file_type,
            lrg_num,
            app_settings,
        )
        input_list, nm = input_reader.run()
        if file_type == "gbk":
            filename = "{}_{}".format(dictionary["genename"], nm)
        else:
            filename = "{}_{}".format(dictionary["genename"], lrg_num)

        writer = LatexWriter(input_list, filename, args.write_as_latex)
        logging.info("Generated file {}".format(writer.run()))


def move_files(latex_file):
    os.rename(latex_file, os.path.join("tex_files", latex_file))


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    arg_parser = argparse.ArgumentParser(
        description="Customise reference sequence settings"
    )
    arg_parser.add_argument("-i", dest="input_file", required=True)
    arg_parser.add_argument(
        "--trim", dest="trim_flanking", action="store_false", default=True
    )
    arg_parser.add_argument(
        "--clashes", dest="print_clashes", action="store_false", default=True
    )
    arg_parser.add_argument(
        "--text",
        dest="write_as_latex",
        action="store_false",
        default=True,
        help="use the argument --text if you want to output only a text document (not conversion to PDF) - this prevents primer annotation",
    )
    arg_parser.add_argument(
        "--config",
        dest="settings",
        default="settings/default_settings.ini",
        help="location of a custom configparser configuration file",
    )
    arg_parser.add_argument("--author", default="mwelland")
    args = arg_parser.parse_args()

    app_settings = configparser.ConfigParser()
    app_settings.read(args.settings)

    run_parser()

    logging.info("Process has completed successfully")
