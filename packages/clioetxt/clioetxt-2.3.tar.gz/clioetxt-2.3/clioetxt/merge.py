def read_book(filename:str, k_idx:int, split_by=','):
    """ Read csv or txt file as dict

    Params:
    filename(str): filename to read
    k_idx(int): index column for key

    Return dict
    """
    d = {}
    with open(filename) as f:
        for line in f:
            line = line.strip().split(',')
            d[line[k_idx]]=line
    return d


def merge(bk1:str, k1_idx:int, bk2:str, k2_idx:int, merge_type:str, out_filename:str='output.csv'):
    """ Operand Or | And | Symetric difference update keep the shape of bk1 if items in both

    Params:
    bk1(str): filename 1 to read
    k1_idx(int): index column for key
    bk2(str): filename 1 to read
    k2_idx(int): index column for key
    merge_type(str): can be | or & or ^ or -

    ie.merge('Book1.csv',1,'Book2.csv',1,"^")

    return file with default out filename: 'output.csv'
    """
    bk1 = read_book(bk1,k1_idx)
    bk2 = read_book(bk2,k2_idx)

    setbk1=set(list(bk1.keys())[1:]) # chop head
    setbk2=set(list(bk2.keys())[1:]) # chop head

    if(merge_type=="&" or merge_type=="|" or merge_type=="^" ):
        bk1 = {**bk2,**bk1}

    if(merge_type=="&"):
        num_in_both = list(setbk1 & setbk2) # set operation
        num_in_both.sort()

    if(merge_type=="|"):
        num_in_both = list(setbk1 | setbk2) # set operation
        num_in_both.sort()
    
    if(merge_type=="-"):
        num_in_both = list(setbk1 - setbk2) # set operation
        num_in_both.sort()  

    if(merge_type=="^"):
        num_in_both = list(setbk1 ^ setbk2) # either but not both
        num_in_both.sort()  

    output_data = '\n'.join([','.join(bk1[line]) for line in num_in_both])

    with open(out_filename,'w') as fw:
        fw.write(','.join(list(bk1.values())[0])+'\n')
        fw.writelines(output_data)

