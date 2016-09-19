# -*- coding: utf-8 -*- 
import bson
import sys
from codec import encode, decode

if __name__ == '__main__' :
	data = {'a' : 1, 'b' : 1.5, 'c' : 'hello world', 'd' : {'level1' : False, 'x' : { 'level2' : {'ok' : 'ok'}, 'y' : [1, -2, 3]} }, 'ccc' : None, 'userid' : 100010000032} 
	#data = {'b' : 1.5, 'c' : 'hello world'}
	#data = { 'a' : 1, 'b' : 1.5, 'c' : 'hello world', 'd' : [1, 2, 3, 4, 5], 'e' : {'x' : 1, 'y' : 2}}

	bs = bson.BSON.encode(data)
	size1 = len(bs)

	bin = encode(data, 'proto1')
	size2 = len(bin)

	print 'cmp size', 'bson = %d, encode = %d' %(size1, size2)
	print 'cmp data', 'bson =   ' ,list(bs)
	print 'cmp data', 'encode = ' ,list(bin)

	print 'decode result : ', decode(bin, 'proto1')
