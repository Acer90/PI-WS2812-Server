import sys

def StringToDict(data):
        arr = dict()
        if '&' in data:
            splitdata = data.split('&')
            for single in splitdata:
                if '=' in single:
                    para = single.split('=')
                    arr[para[0]] = para[1]
                else:
                    arr[single] = ""
        elif '=' in data:
            para = data.split('=')
            arr[para[0]] = para[1]
        else:
            arr[data] = ""
        return arr