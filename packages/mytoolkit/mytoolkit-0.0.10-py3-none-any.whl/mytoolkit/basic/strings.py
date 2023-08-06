def snake_to_camel(s: str):
    temp = s.split('_')
    res = temp[0] + ''.join(ele.title() for ele in temp[1:])
    return res
