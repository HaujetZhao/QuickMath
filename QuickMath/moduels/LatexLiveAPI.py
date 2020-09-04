#!/usr/bin/env python3

import os
import base64
import requests
import json

service = 'https://www.latexlive.com:5001/api/mathpix/posttomathpix'

def recognizePixmap(pixmap):

    with open(pixmap, 'rb') as f:
        img = base64.b64encode(f.read())
    args = {
        'src': 'data:image/png;base64,' + str(img, encoding = "utf-8"),
    }

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-type": "application/json",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    result = requests.post(service, data=json.dumps(args), headers=headers, timeout=30).text
    # print(result)
    # print(json.dumps(result, indent=4, sort_keys=True))
    return result
