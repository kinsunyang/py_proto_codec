# -*- coding: utf-8 -*- 

import os.path

RUN_TEST = True 
PROTO_PATH = './'

from type_def import TYPE_DEFINE
from field import create_field_by_value, load_field
# ------------------------------
'''
	加载协议py文件
'''

class ProtoDefine(object) :
	def __init__(self, proto_name) :
		self._data = []	
		self._proto_name = proto_name
		filename = self.get_file_name() 
		if os.path.exists(filename) :
			self.load_from_file(filename)

	def get_file_name(self) :
		return PROTO_PATH + self._proto_name + '.py'

	def load_from_file(self, filename) :
		import importlib
		#m = importlib.import_module(self._proto_name)
		m = __import__(self._proto_name)
		data = getattr(m, 'proto', [])
		for one in data :
			self._data.append(load_field(one[0], one[1], one[2]))

	def save_to_file(self) :
		filename = self.get_file_name()
		f = file(filename, 'wb')
		s = []
		for field in self._data :
			s.append(field.get_field())
		f.write('proto = %s'%(str(s)))
		f.close()


	def has_field(self, key, value) :
		for field in self._data :
			if field.get_key() == key :
				assert( TYPE_DEFINE.getType(value) == field.get_type())
				return True

		return False


	def update_field(self, key, value) :
		self._data.append(create_field_by_value(key, value))

	# TODO 二分查找
	def get_field(self, key) :
		for field in self._data :
			if field.get_key() == key :
				return field
	def update(self, data) :
		for k, v in data.iteritems() :
			if not self.has_field(k, v) :
				self.update_field(k, v)		

		if RUN_TEST :
			self.save_to_file()

	def encode(self, data) :
		ret = ''
		for field in self._data :
			v = data.get(field.get_key(), TYPE_DEFINE.getTypeDefaultValue(field.get_type()))
			
			ret += field.encode(v)
		return ret
			
	def decode(self, bin) :
		ret = {}

		offset = 0

		for field in self._data :
			value, len = field.decode(bin[offset:])
			offset += len
			ret[field.get_key()] = value

		return ret

class ProtoMgr(object) :
	def __init__(self) :
		self._proto_dict = {}

	def load_proto(self, proto) :
		if self._proto_dict.has_key(proto) :
			return self._proto_dict[proto]

		self._proto_dict[proto] = ProtoDefine(proto) 
		return self._proto_dict[proto]

	def encode(self, data, proto) :
		p = self.load_proto(proto)
		
		# 先更新协议
		p.update(data)
		# 再编码
		return p.encode(data)
		
	def decode(self, data, proto) :
		p = self.load_proto(proto)
		return p.decode(data)

