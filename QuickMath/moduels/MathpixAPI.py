#!/usr/bin/env python3

import os
import base64
import requests
import json

#
# Common module for calling Mathpix OCR service from Python.
#
# N.B.: Set your credentials in environment variables APP_ID and APP_KEY,
# either once via setenv or on the command line as in
# APP_ID=my-id APP_KEY=my-key python3 simple.py
#

env = os.environ

service = 'https://api.mathpix.com/v3/latex'


# Return the base64 encoding of an image with the given filename.
#
#
# Call the Mathpix service with the given arguments, headers, and timeout.
#
def latex(args, appid, appkey, timeout=30):
    headers = {
        'app_id': env.get('APP_ID', appid),
        'app_key': env.get('APP_KEY', appkey),
        'Content-type': 'application/json'
    }
    r = requests.post(service,
        data=json.dumps(args), headers=headers, timeout=timeout)
    return json.loads(r.text)




#
# Example using Mathpix OCR with multiple result formats. We want to recognize
# both math and text in the image, so we pass the ocr parameter set to
# ['math', 'text']. This example returns the LaTeX text format, which
# starts in text mode instead of math mode, the latex_styled format,
# the asciimath format, and the mathml format. We define custom
# math delimiters for the text result so that the math is surrounded
# by dollar signs ("$").
#

def recognizePixmap(pixmap, appid, appkey):

    # im = Image.open(pixmap)
    # output_buffer = BytesIO()
    # im.save(output_buffer,  'PNG')
    # binara_data = output_buffer.getvalue()
    with open(pixmap, 'rb') as f:
        img = base64.b64encode(f.read())


    r = latex({
        'src': 'data:image/png;base64,' + str(img, encoding = "utf-8"),
        'ocr': ['math', 'text'],
        'skip_recrop': True,
        'formats': ['text', 'latex_simplified'],
         # 'formats': ['text', 'latex_styled', 'asciimath', 'mathml', 'latex_simplified'],
        'format_options': {
            'text': {
                'transforms': ['rm_spaces', 'rm_newlines'],
                'math_delims': ['$', '$']
            },
            'latex_styled': {'transforms': ['rm_spaces']}
        }
    }, appid, appkey)

    #
    # Note the actual results might be slighly different in LaTeX spacing or
    # MathML attributes.
    #

    # print('Expected for r["text"]: "$-10 x^{2}+5 x-3$ and $-7 x+4$"')
    # print('Expected for r["latex_styled"]: "-10 x^{2}+5 x-3 \\text { and }-7 x+4"')
    # print('Expected for r["asciimath"]: "-10x^(2)+5x-3\\" and \\"-7x+4"')
    # print('Expected for r["mathml"]: "<math><mo>\u2212</mo><mn>10</mn><msup><mi>x</mi><mn>2</mn></msup><mo>+</mo><mn>5</mn><mi>x</mi><mo>\u2212</mo><mn>3</mn><mtext>\u00a0and\u00a0</mtext><mo>\u2212</mo><mn>7</mn><mi>x</mi><mo>+</mo><mn>4</mn></math>"')

    return json.dumps(r, indent=4, sort_keys=True)
    # 这里就得到了识别的结果, 大概长这样:
    # {
    #     "detection_list": [],
    #     "detection_map": {
    #         "contains_chart": 0,
    #         "contains_diagram": 0.0001,
    #         "contains_graph": 0.0002,
    #         "contains_table": 0,
    #         "is_blank": 0.0005,
    #         "is_inverted": 0,
    #         "is_not_math": 0.0005,
    #         "is_printed": 0.0008
    #     },
    #     "latex_confidence": 0.7462203502655029,
    #     "latex_confidence_rate": 0.9728515625,
    #     "latex_simplified": "\\sqrt { 2 } \\times 6 = y",
    #     "latex_styled": "\\sqrt{2} \\times 6=y",
    #     "position": {
    #         "height": 335,
    #         "top_left_x": 0,
    #         "top_left_y": 0,
    #         "width": 545
    #     },
    #     "request_id": "71645984d2e2d742c4a24a834b0e6f29",
    #     "text": "$\\sqrt{2} \\times 6=y$"
    # }
