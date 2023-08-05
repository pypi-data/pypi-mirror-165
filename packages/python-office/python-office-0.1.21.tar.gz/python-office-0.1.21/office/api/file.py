#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: 文件.py
# Mail: 1957875073@qq.com
# Created Time:  2022-4-25 10:17:34
# Description: 有关 文件 的自动化操作
#############################################
from office.lib.utils.except_utils import except_dec

from office.core.FileType import MainFile
from office.core.SearchByContentType import MainSearchByContent

mainFile = MainFile()
mainSearchByContent = MainSearchByContent()


# todo：输入文件路径
@except_dec()
def replace4filename(path, del_content, replace_content=None):
    mainFile.replace4filename(path, del_content, replace_content)


# todo：输入文件路径
@except_dec()
def search_by_content(search_path, content):  # 定义 search() 函数，传入 "path" 文件路径， "target" 要查找的目标文件
    mainSearchByContent.search_by_content(search_path, content)


@except_dec()
def file_name_insert_content(file_path, insert_position: int, insert_content: str):
    mainFile.file_name_insert_content(file_path, insert_position, insert_content)


@except_dec()
def file_name_add_prefix(file_path, prefix_content):
    mainFile.file_name_add_prefix(file_path, prefix_content)


@except_dec
def file_name_add_postfix(file_path, postfix_content):
    mainFile.file_name_add_postfix(file_path, postfix_content)
