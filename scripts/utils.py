@staticmethod
def lines_of(string, sep='\n'):
    return string.split(sep)

@staticmethod
def line_to_list(line, columns_types, field_sep=None):
    spl = line.split(field_sep)
    ncolum=len(columns_types)
    if len(spl) != ncolum:
        print(f'Line:{line} has {len(spl)} fields.\nExpected {len(columns_types)}')
        return []
    ret = [columns_types[i](spl[i]) for i in range(ncolum)]
    return ret

@staticmethod
def text_table_to_data(str_table, colum_types, header=True, field_sep=None):
    lines = lines_of(str_table)
    if header:
        del lines[0]
    data = [line_to_list(l,columns_types=colum_types,field_sep=field_sep) for l in lines if l!='']
    return data

@staticmethod
def mean(lst):
    if len(lst) > 0:
        return sum(lst)/len(lst)
    return 0