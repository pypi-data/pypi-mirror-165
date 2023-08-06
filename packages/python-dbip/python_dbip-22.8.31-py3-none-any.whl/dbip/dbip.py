#!/usr/bin/env python


"""
-------------------------------------------------------------

File name: __init__.py
File function: IP database that supports IPv6 and IPv4 dual-stack protocols.
File Description: Add, delete, verify IP information
File author: mxlbb(cute baby fox)
File Date: August 22, 2022
File function:  __read__(path)
				__write__(path, text)
				__ip__(ip)
				__recursion__update__(ip, text)
				__recursion__remove__(ip, text)
				__add__(ip)
				__update__(ip)
				__remove__(ip)
				__verify__(ip)
				__system__call__(__system__call__number__,
				__system__call__parameters__)

文件名称：__init__.py
文件作用：支持Ipv6和IPv4双栈协议的IP数据库。
文件说明：添加、删除、验证IP信息
文件作者：萌小狸宝宝
文件日期：2022年8月22日
文件函数：	__read__(path)
			__write__(path, text)
			__ip__(ip)
			__recursion__update__(ip, text)
			__recursion__remove__(ip, text)
			__add__(ip)
			__update__(ip)
			__remove__(ip)
			__verify__(ip)
			__system__call__(__system__call__number__,
							 __system__call__parameters__)

-------------------------------------------------------------
"""


def __read__(path):
	"""
	---------------------------------------------------------

	Function name: __read__(path)
	Function parameters: path -> path
	Function: Read file text data and convert dictionary type
	Function preparation: mxlbb(cute baby fox)
	Function time: August 22, 2022

	函数名称：__read__(path)
	函数参数：path -> 路径
	函数作用：读取文件文本数据并转换字典类型
	函数编写：萌小狸宝宝
	函数时间：2022年8月22日

	---------------------------------------------------------
	"""
	import json
	import pathlib
	paths = "DatabaseIP"
	if not pathlib.Path(paths).is_dir() and not pathlib.Path(F"./{paths}/{str(path)}.db").is_file():
		return dict()
	textData = str()
	with open(F"./{paths}/{str(path)}.db", "r", encoding="utf-8") as path:
		for fd in path.readlines():
			if fd.strip().startswith("//"):
				continue
			else:
				textData += fd
	if len(textData) != 0:
		return json.loads(textData)
	else:
		return dict()


def __write__(path, text):
	"""
	---------------------------------------------------------

	Function name: __ip__(ip)
	Function parameters: ip -> IP address
	Function: Parse IP version type
	Function preparation: mxlbb(cute baby fox)
	Function time: August 22, 2022

	函数名称：__write__(path, text)
	函数参数：path -> 路径，text -> 文本内容
	函数作用：字典类型并转换文本数据写入文件
	函数编写：萌小狸宝宝
	函数时间：2022年8月22日

	---------------------------------------------------------
	"""
	from pathlib import Path
	import json
	import os
	paths = "DatabaseIP"
	if not Path(paths).is_dir():
		os.mkdir(paths)
	with open(F"./{paths}/{str(path)}.db", "w", encoding="utf-8") as path:
		json.dump(text,
				  path,
				  ensure_ascii=False,
				  indent=4,
				  skipkeys=True)
		return True
	return False


def __ip__(ip):
	"""
	---------------------------------------------------------

	Function name: __ip__(ip)
	Function parameters: ip -> IP address
	Function role: Parse IP type
	Function preparation: mxlbb(cute baby fox)
	Function time: August 22, 2022

	函数名称：__ip__(ip)
	函数参数：ip -> IP地址
	函数作用：解析IP类型
	函数编写：萌小狸宝宝
	函数时间：2022年8月22日

	---------------------------------------------------------
	"""
	import datetime
	if ip.count(".") == 3:
		ip = ("IPv4", ip.split("."), ip)
	if ip.count(":") >= 2:
		ip = ("IPv6", ip.split(":"), ip)
	ipd = ip[2]
	for f1 in range(len(ip[1]), 0, -1):
		ipd = {ip[1][f1 - 1]: ipd}
	ip = {ip[0]: ipd}
	return ip


def __recursion__update__(ip, text):
	"""
	---------------------------------------------------------

	Function name: __recursion__update__(ip, text)
	Function parameters: ip -> IP dataset, text -> IP address
	Function: add IP address
	Function preparation: mxlbb(cute baby fox)
	Function time: August 22, 2022

	函数名称：__recursion__update__(ip, text)
	函数参数：ip -> IP数据集，text -> IP地址
	函数作用：添加IP地址
	函数编写：萌小狸宝宝
	函数时间：2022年8月22日

	---------------------------------------------------------
	"""
	if text == dict():
		text.update(ip)
	else:
		try:
			for f1 in zip(ip, text):
				if f1[0] == f1[1]:
					__recursion__update__(ip[f1[0]], text[f1[1]])
				else:
					text.update(ip)
					return text
		except Exception as e:
			# 开始记录错误
			import json
			import datetime
			ed = {
				"time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
				"write": ip,
				"read": json.dumps(text),
				"error": str(e),
				"message": "An exception occurred while reading the file. Overwrite all data when writing."
			}
			with open("[error]__ip__data__recursion__update__.log", "a", encoding="utf-8") as fp:
				json.dump(ed,
						  fp,
						  ensure_ascii=False,
						  skipkeys=True)
				fp.write("\n")
			# 结束记录错误
			text = ip
	return text


def __recursion__remove__(ip, text):
	"""
	---------------------------------------------------------

	Function name: __recursion__remove__(ip, text)
	Function parameters: ip -> IP dataset, text -> IP address
	Function: delete IP address
	Function preparation: mxlbb(cute baby fox)
	Function time: August 22, 2022

	函数名称：__recursion__remove__(ip, text)
	函数参数：ip -> IP数据集，text -> IP地址
	函数作用：删除IP地址
	函数编写：萌小狸宝宝
	函数时间：2022年8月22日

	---------------------------------------------------------
	"""
	if type(ip) == dict and type(text) == dict:
		for f1k, f1v in text.items():
			if f1k in ip.keys() and ip[f1k] == f1v:
				del ip[f1k]
				return ip
			if f1k in ip.keys() and ip[f1k] != f1v:
				__recursion__remove__(ip[f1k], f1v)
	return ip


def __recursion__verify__(ip, text):
	"""
	---------------------------------------------------------

	Function name: __recursion__verify__(ip, text)
	Function parameters: ip -> IP dataset, text -> IP address
	Function: Verify IP address
	Function preparation: mxlbb(cute baby fox)
	Function time: August 22, 2022

	函数名称：__recursion__verify__(ip, text)
	函数参数：ip -> IP数据集，text -> IP地址
	函数作用：验证IP地址
	函数编写：萌小狸宝宝
	函数时间：2022年8月22日

	---------------------------------------------------------
	"""
	if type(ip) == dict and type(text) == dict:
		for f2tk, f2tv in text.items():
			if f2tk in ip.keys():
				if ip[f2tk] == text[f2tk] and type(ip[f2tk]) == str and type(text[f2tk]) == str:
					return True
				else:
					return __recursion__verify__(ip[f2tk], text[f2tk])
	return False


def __add__(ip):
	"""
	---------------------------------------------------------

	Function name: __add__(ip)
	Function parameters: ip -> IP address
	Function role: call the __update__(ip) function
	Function preparation: mxlbb(cute baby fox)
	Function time: August 22, 2022

	函数名称：__add__(ip)
	函数参数：ip -> IP地址
	函数作用：调用__update__(ip)函数
	函数编写：萌小狸宝宝
	函数时间：2022年8月22日

	---------------------------------------------------------
	"""
	return __update__(ip)


def __update__(ip):
	"""
	---------------------------------------------------------

	Function name: __update__(ip)
	Function parameters: ip -> IP address
	Function: add or update IP data set address
	Function preparation: mxlbb(cute baby fox)
	Function time: August 22, 2022

	函数名称：__update__(ip)
	函数参数：ip -> IP地址
	函数作用：添加或者更新IP数据集地址
	函数编写：萌小狸宝宝
	函数时间：2022年8月22日

	---------------------------------------------------------
	"""
	ip = __ip__(ip)
	if "IPv4" in ip.keys():
		ip = {"IPv4": __recursion__update__(ip["IPv4"], __read__("IPv4"))}
	if "IPv6" in ip.keys():
		ip = {"IPv6": __recursion__update__(ip["IPv6"], __read__("IPv6"))}
	for f1k, f1v in ip.items():
		__write__(f1k, f1v)
	return ip


def __remove__(ip):
	"""
	---------------------------------------------------------

	Function name: __remove__(ip)
	Function parameters: ip -> IP address
	Function: delete and update IP data set address
	Function preparation: mxlbb(cute baby fox)
	Function time: August 22, 2022

	函数名称：__remove__(ip)
	函数参数：ip -> IP地址
	函数作用：删除更新IP数据集地址
	函数编写：萌小狸宝宝
	函数时间：2022年8月22日

	---------------------------------------------------------
	"""
	data = __ip__(ip)
	for f1k, f1v in data.items():
		data = {f1k: __recursion__remove__(__read__(f1k), f1v)}
	for f1k, f1v in data.items():
		__write__(f1k, f1v)
	return False if ip == data else True


def __verify__(ip):
	"""
	---------------------------------------------------------

	Function name: __verify__(ip)
	Function parameters: ip -> IP address
	Function: Check whether the IP data set address exists
	Function preparation: mxlbb(cute baby fox)
	Function time: August 22, 2022

	函数名称：__verify__(ip)
	函数参数：ip -> IP地址
	函数作用：校验IP数据集地址是否存在
	函数编写：萌小狸宝宝
	函数时间：2022年8月22日

	---------------------------------------------------------
	"""
	for f1k, f1v in __ip__(ip).items():
		return __recursion__verify__(__read__(f1k), f1v)


def __system__call__(__system__call__number__,
					 __system__call__parameters__):
	"""

	---------------------------------------------------------

	Function name: __system__call__(__system__call__number__,
																	__system__call__parameters__)

	Function parameters: __system__call__number__ 		-> call number
											 __system__call__parameters__ 	-> call parameters

											call number	->	__add__
																			__update__
																			__remove__
																			__verify__

											Call parameters -> IP address

	Function role: function call table
	Function preparation: mxlbb(cute baby fox)
	Function time: August 22, 2022

	函数名称：__system__call__(__system__call__number__,
													  __system__call__parameters__)

	函数参数：__system__call__number__		-> 调用号
					 __system__call__parameters__	-> 调用参数

					调用号	->	__add__
											__update__
											__remove__
											__verify__

					调用参数	->	IP地址

	函数作用：函数调用表
	函数编写：萌小狸宝宝
	函数时间：2022年8月22日
	---------------------------------------------------------
	"""
	__system__call__table__ = {
		"__add__": __add__,
		"__update__": __update__,
		"__remove__": __remove__,
		"__verify__": __verify__
	}
	return __system__call__table__[__system__call__number__](__system__call__parameters__)


__system__call__("__add__","192.168.9.9")