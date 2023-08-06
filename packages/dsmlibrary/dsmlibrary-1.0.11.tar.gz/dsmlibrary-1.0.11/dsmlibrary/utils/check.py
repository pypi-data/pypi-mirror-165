from .requests import check_http_status_code

def check_lists_int(data=None, dataName="data"):
    if type(data) != list:
        raise Exception(f'expect {dataName} type `list`, but got ({type(data)})')
    _reject = []
    for i, d in enumerate(data):
        if type(d) != int:
            _reject.append({
                'data': d,
                'index': i
            })
    if _reject != []:
        raise Exception(f"expect {dataName} [<int>,<int>, ... , <int>] but got {_reject} ")