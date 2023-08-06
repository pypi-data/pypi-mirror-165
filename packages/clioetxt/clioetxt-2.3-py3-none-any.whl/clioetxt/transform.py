""" This module provide function to transform the data ie. sorted column (required data_header global variable), invert data, search item, convert dict to list and format columns

neat_print (d): print dictionary with tab between key and values
values_zip (*args): (helper function) the function zip values of the column in order of the data_header
sorted_column(d): function to rearrange the dictionary value as per data_header (global variable)
invert_dict_byindex(d, index=0): function that invert data by value index number
invert_dict_byindex_cc(d, index, cc=0): function that invert data by value index number with description
search_items(d, search_kv): function that search dictionary (param: d) by the value input (search_v)
dict_to_list(d): convert dictionary to list
format_columns(list_data): apply format to the list - (1) Title or (2) Uppercase or (3) Lowercase -
Additional Notes:
Sample data header for values_zip(*args) and sorted_column(d)
ie. data_header = ("key_column", "value_col1", "value_col2" ... "value_lastcol")
"""

data_header = []


def neat_print(d):
    """ Function print dictionary in the console with tab between key and values

    parameters:
    d (dictionary): The object to print
    """
    for key, value in d.items():
        print(key, "\t", value)


def values_zip(*args):
    """ zip the *args (lists) in order of the data_header (required as global variable)

    parameter:
    *args of list (excel column ie column1, column2 ...)

    returns:
    tuple: the zip value of the column in order of the data_header
    """
    if "data_header" not in globals() or len(data_header) == 0:
        return zip(*args)

    data_header_len = len(data_header)
    args_len = len(args)    # 3
    args_header = []
    args_order = []
    args_column_used = []
    args_left = []

    counter = 0
    while counter < args_len:
        args_header.append(args[counter][0])  # 1st data or the header
        counter += 1

    counter = 0
    while counter < data_header_len:
        if data_header[counter] in args_header:
            n = 0
            while n < args_len:
                if args_header[n] == data_header[counter]:
                    args_order.append(args[n])
                    args_column_used.append(n)
                n += 1
        else:
            header = data_header[counter],
            args_empty_h = header + tuple(" " * len(args[0]))
            args_order.append(args_empty_h)
        counter += 1

    n = 0
    while n < args_len:
        if n not in args_column_used:
            args_left.append(args[n])
        n += 1

    return zip(*args_order, *args_left)
    # ie('cus_name', 'cus_state'), ('Sandhurst Medical Practice', 'VIC')


def sorted_columns(d):
    """ Function to rearrange the dictionary value as per data_header (global variable)

    parameters:
    d (dictionary): The content of the text file as dictionary (original format)

    returns:
    dict: The content of the text file in certain order as per data_header (global variable) as dictionary
    """
    dict_key = tuple(d.keys())
    d_value = {}

    for value in d.values():
        counter = 0
        while counter < len(value):
            if counter not in d_value:
                d_value[counter] = [value[counter]]
            else:
                d_value[counter].append(value[counter])
            counter += 1

    list_d_value = list(d_value.values())  # list of value columns ..
    # use values_zip function to rearrange column in order
    dict_values = tuple(values_zip(*list_d_value))  # tuple of record 1, 2 ..
    data_sorted = dict(zip(dict_key, dict_values))
    return data_sorted


def invert_dict_byindex(d, index=0):
    """ Function that invert data by value index number

    parameters:
    d (dictionary): The content of the text file as dictionary
    index(int): The value index to be inverted

    returns:
    dict: Inverted data by value index number as dictionary
    """

    invert_data = dict()
    for key, value in d.items():
        if value[index].upper() not in invert_data:
            invert_data[value[index].upper()] = [key.upper()]
        else:
            invert_data[value[index].upper()].append(key.upper())
    return invert_data


def invert_dict_byindex_cc(d, index, cc=0):
    """ Function that invert data by value index number

    parameters:
    d (dictionary): The content of the text file as dictionary
    index (int): The value index to be inverted
    cc (int): The index value for key description (default = 0)

    returns:
    dict: Inverted data by value index number as dictionary
    """
    invert_data = dict()
    for key, value in d.items():
        val = value[index].upper()
        if val not in invert_data:
            invert_data[val] = [key.upper() + " - " + value[cc].title()]
        else:
            invert_data[val].append(key.upper() + " - " + value[cc].title())
    return invert_data


def search_items(d, search_kv):
    """ Function that search dictionary (param: d) by the value input (search_v)

    parameters:
    d (dictionary): The content of the text file as dictionary
    search_val (str): Search by dictionary's value

    returns:
    dict: Search result of param: search_v as dictionary
     """
    d_result = {}

    for key, value in d.items():  # search by key
        if key.upper() == search_kv.upper():
            d_result[key.upper()] = value

    for key, value in d.items():  # search by value
        x = 0
        while x < len(value):
            if value[x].lower() == search_kv.lower():
                d_result[key.upper()] = value
            x += 1
    return d_result


def dict_to_list(d):
    """ Convert dictionary to list

    parameters:
    d (dictionary)

    returns:
    list: list of data in columns format. (col 1, col 2 ... etc)
    """
    dict_key = list(d.keys())
    d_value = {}
    for value in d.values():
        counter = 0
        while counter < len(value):  # len(value) = 3
            if counter not in d_value:
                d_value[counter] = [value[counter]]
            else:
                d_value[counter].append(value[counter])
            counter += 1
    list_d_value = list(d_value.values())  # list of value columns ..
    return([dict_key] + list_d_value)


def format_columns(list_data):
    """ Apply format to the list - (1) Title or (2) Uppercase or (3) Lowercase -

    parameters:
    list_data (list)

    returns:
    dict: formatted data as per input entered
    """
    col_no = len(list_data)
    f_header = []
    formatted_columns = []

    counter = 0
    while counter < col_no:
        f_header.append(list_data[counter][0])  # 1st data or the header
        counter += 1    # # use values_zip function to rearrange column in order
    num = 0
    while num < col_no:
        format_no = input(
            "Column " + f_header[num] + " >> select 1-Title, 2-Upper, 3-Lower: ")
        if format_no == "1":
            res = [li.title() for li in list_data[num]]
            formatted_columns.append(res)
        elif format_no == "2":
            res = [li.upper() for li in list_data[num]]
            formatted_columns.append(res)
        elif format_no == "3":
            res = [li.lower() for li in list_data[num]]
            formatted_columns.append(res)
        else:
            print('Invalid Entry - Choose 1/2/3 // No format changes in "' +
                  f_header[num] + '" column.')
            formatted_columns.append(list_data[num])
        num += 1

    counter = 0
    while counter < col_no:  # new added 1/12/2019 10:33pm
        formatted_columns[counter][0] = (
            formatted_columns[counter][0]).title()  # 1st data or the header
        counter += 1    # Title format is proper

    dict_values = tuple(zip(*formatted_columns[1:]))  # tuple the values
    data_formatted = dict(zip(formatted_columns[0], dict_values))  # dict(k,v)
    return data_formatted
