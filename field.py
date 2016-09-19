# -*- coding: utf-8 -*- 

from type_def import TYPE_DEFINE
import struct

# (key, type, sub_proto)
class ProtoField(object) :
	def __init__(self, key, sub = None) :
		self._key = key
		self._sub = sub 

	def get_field(self) :
		return (self._key, self.get_type(), self.get_sub_proto())

	def get_type(self) :
		pass
	
	def get_key(self) :
		return self._key

	def get_sub_proto(self) :
		if not self._sub :
			return None
		else :
			return self._sub.get_field()

	def decode(self, buff) :
		pass

	def encode(self, value) :
		pass

class Int64Field(ProtoField) :
	def __init__(self, key, sub = None) :
		super(Int64Field, self).__init__(key, sub)

	def get_type(self) :
		return TYPE_DEFINE.VALUE_TYPE_INT64

	def decode(self, buff) :
		return struct.unpack('!q', buff[0:8])[0], 8
	def encode(self, value) :
		return struct.pack('!q', value)

class Int32Field(ProtoField) :
	def __init__(self, key, sub = None) :
		super(Int32Field, self).__init__(key, sub)

	def get_type(self) :
		return TYPE_DEFINE.VALUE_TYPE_INT32

	def decode(self, buff) :
		return struct.unpack('!i', buff[0:4])[0], 4
	def encode(self, value) :
		return struct.pack('!i', value)

class BoolField(ProtoField) :
	def __init__(self, key, sub = None) :
		super(BoolField, self).__init__(key, sub)
	
	def get_type(self) :
		return TYPE_DEFINE.VALUE_TYPE_BOOL

	def decode(self, buff) :
		return struct.unpack('!B', buff[0:1])[0] > 0, 1

	def encode(self, value) :
		return struct.pack('!B', value and 1 or 0)

class NoneField(ProtoField) :
	def __init__(self, key, sub = None) :
		super(NoneField, self).__init__(key, sub)
	
	def get_type(self) :
		return TYPE_DEFINE.VALUE_TYPE_NULL

	def decode(self, buff) :
		return None, 0

	def encode(self, value) :
		return ''

class FloatField(ProtoField) :
	def __init__(self, key, sub = None) :
		super(FloatField, self).__init__(key, sub)

	def get_type(self) :
		return TYPE_DEFINE.VALUE_TYPE_FLOAT32

	def decode(self, buff) :
		return struct.unpack('!f', buff[0:4])[0], 4
	def encode(self, value) :
		return struct.pack('!f', value)

class StringField(ProtoField) :
	def __init__(self, key, sub = None) :
		super(StringField, self).__init__(key, sub)

	def get_type(self) :
		return TYPE_DEFINE.VALUE_TYPE_STRING

	def decode(self, buff) :
		len = struct.unpack('!H', buff[0:2])[0]
		s = struct.unpack('%ds'%(len), buff[2:2+len])[0]
		return s, len + 2
	def encode(self, value) :
		return struct.pack('!H%ds'%(len(value)), len(value), value)

class ListField(ProtoField) :
	def __init__(self, key, sub) :
		super(ListField, self).__init__(key, sub)
	
	def get_type(self) :
		return TYPE_DEFINE.VALUE_TYPE_LIST

	def decode(self, buff) :
		ret = []
		len = 2
		offset = 2
		count = struct.unpack('!H', buff[0:2])[0]
		for i in xrange(count) :
			v, l = self._sub.decode(buff[offset:])
			ret.append(v)
			offset += l
			len += l

		return ret, len

	def encode(self, value) :
		count = len(value)
		ret = ''
		ret += struct.pack('!H', count)
		for one in value :
			ret += self._sub.encode(one)

		return ret

class DictField(ProtoField) :
	def __init__(self, key, sub) :
		super(DictField, self).__init__(key, sub)
	
	def get_type(self) :
		return TYPE_DEFINE.VALUE_TYPE_DICT

	def get_field(self) :
		return (self.get_key(), self.get_type(), tuple([f.get_field() for f in self._sub]))


	def encode(self, value) :
		ret = ''
		for f in self._sub :
			v = value.get(f.get_key(), TYPE_DEFINE.getTypeDefaultValue(f.get_type()))
			ret += f.encode(v)
		
		return ret

	def decode(self, buff) :
		ret = {}
		offset = 0
		for f in self._sub :
			value, len = f.decode(buff[offset :])
			offset += len
			ret[f.get_key()] = value

		return ret, offset


def load_field(key, type, sub = None) :
	if type == TYPE_DEFINE.VALUE_TYPE_INT64 :
		return Int64Field(key)
	elif type == TYPE_DEFINE.VALUE_TYPE_INT32 :
		return Int32Field(key)
	elif type == TYPE_DEFINE.VALUE_TYPE_BOOL :
		return BoolField(key)
	elif type == TYPE_DEFINE.VALUE_TYPE_NULL :
		return NoneField(key)
	elif type == TYPE_DEFINE.VALUE_TYPE_FLOAT32 :
		return FloatField(key)
	elif type == TYPE_DEFINE.VALUE_TYPE_STRING :
		return StringField(key)
	elif type == TYPE_DEFINE.VALUE_TYPE_LIST :
		return ListField(key, load_field(sub[0], sub[1], sub[2]))
	elif type == TYPE_DEFINE.VALUE_TYPE_DICT:
		p = []
		for one in sub :
			p.append(load_field(one[0], one[1], one[2]))
		return DictField(key, p)

def create_field_by_value(key, value) :
	type = TYPE_DEFINE.getType(value)
	if type == TYPE_DEFINE.VALUE_TYPE_INT64 :
		return Int64Field(key)
	elif type == TYPE_DEFINE.VALUE_TYPE_INT32 :
		return Int32Field(key)
	elif type == TYPE_DEFINE.VALUE_TYPE_BOOL :
		return BoolField(key)
	elif type == TYPE_DEFINE.VALUE_TYPE_NULL :
		return NoneField(key)
	elif type == TYPE_DEFINE.VALUE_TYPE_FLOAT32 :
		return FloatField(key)
	elif type == TYPE_DEFINE.VALUE_TYPE_STRING :
		return StringField(key)
	elif type == TYPE_DEFINE.VALUE_TYPE_LIST :
		sub = create_field_by_value(None, value[0])
		return ListField(key, sub)
	elif type == TYPE_DEFINE.VALUE_TYPE_DICT :
		sub = []
		for k,v in value.iteritems() :
			sub.append(create_field_by_value(k, v))
		return DictField(key, sub)


