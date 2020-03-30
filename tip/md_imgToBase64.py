#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
__author__ = 'zachary'
"""
File Name: md_imgToBase64.py
Created Time: 2020-03-30 22:04:01
Last Modified: 
"""
import sys
import os
import base64
"""
accept only one image address parameter.
convert the image to base64 format, then copy it to clipboard.
"""

if __name__ == '__main__':
    if len(sys.argv) > 2:
        print('too many params')
        exit(1)
    try:
        image_path = sys.argv[1]
        f = open(image_path, 'rb')
    except IndexError as ex:
        print("please give image path param")
    except FileNotFoundError as ex:
        print("invalid image path")
    else:
        img = f.read()
        img_base64 = str(base64.b64encode(img), encoding='utf-8')
        code_str = 'data:image/png\;base64,' + img_base64
        flag = input("don't you need to print? (yes/no):")
        if flag == 'n' or flag == 'no':
            print(code_str)
        mk_command = 'touch ~/temp.txt'
        os.system(mk_command)
        w_command = 'echo ' + code_str + ' >> ~/temp.txt '
        os.system(w_command)
        # should install xsel, like 'apt-get install xsel'.
        cp_to_clipboard_command = 'cat ~/temp.txt | xsel --clipboard'
        os.system(cp_to_clipboard_command)
        rm_command = 'rm ~/temp.txt'
        os.system(rm_command)
        print("finished, contents stored on clipboadr.")
        f.close()
