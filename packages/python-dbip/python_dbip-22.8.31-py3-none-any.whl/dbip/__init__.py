#!/usr/bin/env python


"""
---------------------------------------------------------------------------

File name: SafeIp
File function: IP database that supports IPv6 and IPv4 dual-stack protocols.
File Description: Add, delete, verify IP information
File author: mxlbb(cute baby fox)
File Date: August 22, 2022
File function: 	add(ip)
				update(ip)
				remove(ip)
				verify(ip)
				printf()

文件名称：SafeIp
文件作用：支持Ipv6和IPv4双栈协议的IP数据库。
文件说明：添加、删除、验证IP信息
文件作者：萌小狸宝宝
文件日期：2022年8月22日
文件函数：	add(ip)
			update(ip)
			remove(ip)
			verify(ip)
			printf()

---------------------------------------------------------------------------
"""


from .DatabaseIP import __system__call__ as system_call


def add(ip):
	"""
	------------------------------------------------------------

	Function name: add(ip)
	Function parameters: ip -> IP address
	Function role: call the __update__(ip) function
	Function preparation: mxlbb(cute baby fox)
	Function time: August 21, 2022

	函数名称：add(ip)
	函数参数：ip -> IP地址
	函数作用：调用__update__(ip)函数
	函数编写：萌小狸宝宝
	函数时间：2022年8月21日

	------------------------------------------------------------
	"""
	return system_call("__add__", ip)


def update(ip):
	"""
	------------------------------------------------------------

	Function name: update(ip)
	Function parameters: ip -> IP address
	Function: add or update IP data set address
	Function preparation: mxlbb(cute baby fox)
	Function time: August 21, 2022

	函数名称：update(ip)
	函数参数：ip -> IP地址
	函数作用：添加或者更新IP数据集地址
	函数编写：萌小狸宝宝
	函数时间：2022年8月21日

	------------------------------------------------------------
	"""
	return system_call("__update__", ip)


def remove(ip):
	"""
	------------------------------------------------------------

	Function name: remove(ip)
	Function parameters: ip -> IP address
	Function: delete and update IP data set address
	Function preparation: mxlbb(cute baby fox)
	Function time: August 21, 2022

	函数名称：remove(ip)
	函数参数：ip -> IP地址
	函数作用：删除更新IP数据集地址
	函数编写：萌小狸宝宝
	函数时间：2022年8月21日

	------------------------------------------------------------
	"""
	return system_call("__remove__", ip)


def verify(ip):
	"""
	------------------------------------------------------------

	Function name: verify(ip)
	Function parameters: ip -> IP address
	Function: Check whether the IP data set address exists
	Function preparation: mxlbb(cute baby fox)
	Function time: August 21, 2022

	函数名称：verify(ip)
	函数参数：ip -> IP地址
	函数作用：校验IP数据集地址是否存在
	函数编写：萌小狸宝宝
	函数时间：2022年8月21日

	------------------------------------------------------------
	"""
	return system_call("__verify__", ip)


def printf():
	"""
	------------------------------------------------------------

	Function name: printf()
	Function parameters: none
	Function: print module function
	Function preparation: mxlbb(cute baby fox)
	Function time: August 21, 2022

	函数名称：printf()
	函数参数：无
	函数作用：打印模块功能
	函数编写：萌小狸宝宝
	函数时间：2022年8月21日

	------------------------------------------------------------
	"""
	print(__doc__)
	print(add.__doc__)
	print(update.__doc__)
	print(remove.__doc__)
	print(verify.__doc__)
	print(printf.__doc__)
	import sys
	print(sys.argv)
