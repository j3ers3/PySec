#!/usr/bin/env python3
# encoding:utf8

import requests
import sys

def get_img(url):
    r = requests.get(url)
    img = r.content

    with open('1.jpg', 'wb') as f:
        f.write(img)

    return img


def main():
    if len(sys.argv) !=2:
        print("python3 {0} kaptcha_url".format(sys.argv[0]))
        exit(1)
    import muggle_ocr
    img = get_img(sys.argv[1])
    sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
    text = sdk.predict(image_bytes=img)

    print(text)

if __name__ == '__main__':
    main()

