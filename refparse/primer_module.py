import re
import os
import csv
import logging

from utilities import create_reverse_complement


class Primer:
    def __init__(self, dictionary, filename):
        self.filename = filename
        self.dict = dictionary

    def digest_input(self):
        """
        Extract contents of the input CSV into a dictionary object
        For each row, construct the annotation required, then pass to annotator
        """

        with open(os.path.join("primers", self.filename)) as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                if row["Primer Sequences"].strip().rstrip() == "":
                    continue

                seq = row["Primer Sequences"].upper().strip()
                if row["Exon"] == "":
                    logging.warning("Primer Exon unspecified - please check input file")

                if row["Direction"] == "R":
                    seq = create_reverse_complement(seq)

                if row["Fragment Size"] == "":
                    logging.warning(
                        "Fragment Size unspecified - please check input file"
                    )

                batch = (
                    row["Primer Batch Numbers"]
                    if row["Primer Batch Numbers"]
                    else "Unknown"
                )

                frag_size = row["Fragment Size"] if row["Fragment Size"] else "Unknown"

                constructed_string = "Primer {}{}, Frag size = {}, Batch = {}".format(
                    row["Exon"], row["Direction"], frag_size, batch
                )
                self.search_for_seq(seq, constructed_string)

    def search_for_seq(self, seq, construct):
        """
        Given a query sequence, this component will attempt to find a match for the sequence within the gene sequence
        If a match is found, the naked sequence is substituted for a pdfcomment tag

        This retains the typsetting, but layers a tag over the top which reveals details on mouse-over
        Args:
            seq: the sequence to recognise and replace
            construct: the annotation to overlay
        """

        for transcript in self.dict["transcripts"]:
            for exon in self.dict["transcripts"][transcript]["exons"].keys():
                try:
                    match = re.search(
                        r"(?i){}".format(seq),
                        self.dict["transcripts"][transcript]["exons"][exon]["sequence"],
                    )
                    if match:
                        self.dict["transcripts"][transcript]["exons"][exon][
                            "sequence"
                        ] = re.sub(
                            r"(?i){}".format(seq),
                            "\\\\pdfcomment[date]{{{}}}\\\\hl{{{}}}".format(
                                construct, match.group()
                            ),
                            self.dict["transcripts"][transcript]["exons"][exon][
                                "sequence"
                            ],
                        )

                except MemoryError:
                    logging.error(
                        "MemError annotating {} with {}".format(exon, seq),
                        exc_info=True,
                    )

    def run(self):
        self.digest_input()
        return self.dict
