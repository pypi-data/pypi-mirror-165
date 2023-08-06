""" This module provide function to import data (or load text file) and export data (or upload dict to text file)
and add data or create a new text file 
"""
import os


def import_txt(file_name, split_by="\t"):
    """ Import text file into console with default split ="\t"

    parameters:
    file_name (str): The path to a text file (string or raw string)
    split_by (str): The text file delimiter

    returns:
    dict: The content of the text file as dictionary
    """
    read_line = []
    data = {}
    with open(file_name, "r") as fin:
        for line in fin:
            line = line.strip()
            split_line = line.split(split_by)
            read_line.append(split_line)
    for record in read_line:
        val = []
        x = 1
        while x < len(record):
            val.append(record[x])
            x += 1
        data[record[0]] = tuple(val)
    return data


def import_txt_add_index(file_name, split_by="\t"):  # add index number
    """ Import text file and add index number into console with default split ="\t"

    parameters:
    file_name (str): The path to a text file (string or raw string)
    split_by (str): The text file delimiter

    returns:
    dict: The content of the text file as dictionary
    """
    read_line = []
    data = {}
    no = 0
    with open(file_name, "r") as fin:
        for line in fin:
            line = str(no) + " " + line.strip()
            split_line = line.split(split_by)
            read_line.append(split_line)
            no += 1
    for record in read_line:
        val = []
        x = 1
        while x < len(record):
            val.append(record[x])
            x += 1
        data[record[0]] = tuple(val)
    return data


def add_data(txt_file):
    """ Function to add data to existing file or create text file data with delimiter = "\t"

    parameters:
    txt_file (str): The path to a text file (string or raw string), the function will create a new file if the file is not exist

    returns:
    text file: update the text file (.txt) or create a new file (.txt) if the file does not exist
    """
    if os.path.exists(txt_file):
        # intentionally read txt_file without closing it
        # the purpose so when we add a new record it continue from the last record
        fin = open(txt_file, "r")
        header_line = fin.readline()
        f_header = header_line.strip().split("\t")  # return list of header column
        col_no = len(f_header)
        fin.read()
    else:
        with open(txt_file, "w") as wr:  # create new file
            col_no = input(
                "Created a new file, please advise how many columns? ")
            new_header = input("Please enter header column 1: ").title()
            n = 1
            while n < int(col_no):
                header_name = input(
                    " Please enter header column {}: ".format(str(n+1)))
                new_header = new_header + "\t" + header_name
                n += 1
            wr.write(new_header + "\n")
        add_data(txt_file)  # recursive

    new_entry = input("Do you want to continue adding a new record (Y/N)? ")
    while new_entry.upper() == "Y":
        with open(txt_file, "a") as wr:
            new_line = input("Please enter " + f_header[0] + ": ").upper()
            n = 1
            while n < col_no:
                value = input("Please enter " + f_header[n] + ": ")
                new_line = new_line + "\t" + value
                n += 1
            wr.write(new_line + "\n")
        new_entry = input(
            "Do you want to continue adding a new record (Y/N)? ")


def export_txt(d, file_name, split_by="\t"):
    """ Upload data (dict) to text file with default split ="\t"

    parameters:
    d (dictionary): data to be exported
    file_name (str): The path to a text file (string or raw string)
    split_by (str): The text file delimiter

    returns:
    text file: dict data uploaded as text file format
    """
    with open(file_name, "w") as fin:
        for key, value in d.items():
            fin.write(key + split_by)
            x = 0
            while x < len(value)-1:
                fin.write(value[x] + split_by)
                x += 1
            fin.write(value[len(value)-1] + "\n")


def export_dict_remove_index(d, file, split_by="\t"):  # remove the index number
    """ Upload data (dict) and remove the leading index number to text file with default split ="\t"

    parameters:
    d (dictionary): data to be exported
    file_name (str): The path to a text file (string or raw string)
    split_by (str): The text file delimiter

    returns:
    text file: dict data uploaded as text file format
    """
    with open(file, "w") as fin:
        for key, val in d.items():
            fin.write(key[key.find(" "):] + split_by)
            x = 0
            while x < len(val) - 1:
                fin.write(val[x] + split_by)
                x += 1
            fin.write(val[len(val)-1] + "\n")
