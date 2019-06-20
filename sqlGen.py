import sys


def Convert(data):
    arr = SplitData(data)

    sql = []
    for a in arr:
        sql.append(CreateSQL(a))

    return sql


def CreateSQL(pair):
    sql = pair['sql']

    for p in pair['params']:
        sql = sql.replace('@{}'.format(p['num']), Normalize(p), 1)

    return sql


def Normalize(param):
    data = param['data']
    t = param['type']

    arr_str = ['Guid', 'AnsiString', 'DateTime2']

    if t.startswith('Double'):
        data = data.replace(',', '.')
    elif t.startswith('AnsiString'):
        data = data.replace("'", "''")

    for a in arr_str:
        if t.startswith(a):
            data = "'{}'".format(data)

    return data


def SplitData(data):
    result = []

    sql_delimeter = '\n\n\n\n'
    param_delimeter = '\n\n-- '
    type_delimeter = ' (Type = '

    arr_data = data.split(sql_delimeter)

    for a in arr_data:
        arr_str = a.split(param_delimeter)

        params = []
        arr_par = arr_str[1: -2]

        for p in arr_par:
            num = p[1: p.find(':')]
            t = p[p.find(type_delimeter) + len(type_delimeter): -1]

            data = p[p.find("'") + 1: p.rfind("'")]

            params.append({
                'num': num,
                'data': data,
                'type': t
            })

        result.append({'sql':  arr_str[0], 'params': params})

    return result


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        sql_path = sys.argv[1]
    else:
        sql_path = input("input file path: ")

    if len(sys.argv) == 3:
        res_path = sys.argv[2]
    else:
        res_path = 'result.sql'

    try:
        with open(sql_path, 'r') as file:
            data = file.read()

        if not data:
            raise Exception('Data is None')

        sql = Convert(data)

        with open(res_path, 'w') as outfile:
            for s in sql:
                outfile.write(s)
                outfile.write('\n\n')

    except Exception as ex:
        print(str(ex))
