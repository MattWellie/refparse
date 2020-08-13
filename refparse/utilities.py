import time


def create_reverse_complement(string):
    new_list = []
    for x in string:
        if x == 'A':
            new_list.append('T')
        if x == 'C':
            new_list.append('G')
        if x == 'G':
            new_list.append('C')
        if x == 'T':
            new_list.append('A')
    new_string = ''.join(new_list)
    return new_string[::-1]


def check_file_type(file_name):
    """
    identifies LGR (.xml) and GenBank (.gk/gbk) files
    will print an error message and exit the application if other files are specified
    """
    if file_name.endswith('.xml'):
        return 'lrg'
    elif file_name.endswith('.gb') or file_name.endswith('.gbk'):
        return 'gbk'
    else:
        raise Exception('This program only works for GenBank and LRG files')


def get_date_string():
    return time.strftime("%d-%m-%Y_%H-%M-%S")
