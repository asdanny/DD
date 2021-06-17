
def get_sk(data):
    data_val = [val for val in data['data'].values()]
    n, o, p, q, r, s = data_val[0], data_val[1], data_val[2], data_val[3], data_val[4], data_val[5]
    sk_val = ''
    if n == 'cca':
        sk_val = p[14:19].lower() + o[5:15].upper()
    if n == 'ab':  # check ok
        sk_val = r[10:18] + s[2:13].lower()
    if n == 'ch':
        sk_val = q.upper() + r[6:10].upper()
    if n == 'cbc':  # check ok
        sk_val = q[3:13].upper() + p[10:19].lower()
    if n == 'by':
        sk_val = o[5:8] + p.replace('a', 'c')
    if n == 'xa':
        sk_val = o[1:16] + s[4:10]
    if n == 'cza':
        sk_val = q[6:19].lower() + s[5:11]
    if n == 'cb':
        sk_val = s[5:14] + p[2:13].upper()

    return sk_val


if __name__ == '__main__':
    data = {
        "code": "000000",
        "message": "success",
        "data": {
            "@t": "ab",
            "WnB": "GYKlHpXKNaGfwUJVcTC5",
            "Tcm": "ghQjFHWiuMYg5gBJ72jj",
            "g": "b6Qh7mrWjBCeRkS7BPMV",
            "Ha": "NiUW64hVm1XlmOwfSUwp",
            "RR": "luWc7izQV9t1NU1Hm4Rq"
        }}

    # python 重写
    sk_val2 = get_sk(data=data)
    print(sk_val2)
