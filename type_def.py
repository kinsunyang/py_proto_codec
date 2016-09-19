# -*- coding: utf-8 -*- 

class TYPE_DEFINE(object) :
	# 类型定义, 与bson一致
	VALUE_TYPE_FLOAT32 = 0x01
	VALUE_TYPE_STRING = 0x02	# utf-8
	VALUE_TYPE_DICT = 0x03
	VALUE_TYPE_LIST = 0x04	# 数组元素类型必须一致
	VALUE_TYPE_BINARY = 0x05
	VALUE_TYPE_BOOL = 0x08

	VALUE_TYPE_NULL = 0x0A

	VALUE_TYPE_INT32 = 0x10
	VALUE_TYPE_INT64 = 0x12

	@classmethod
	def getType(cls, value) :
		if type(value) == type(1L) :
			return cls.VALUE_TYPE_INT64
		elif type(value) == type(1) :
			return cls.VALUE_TYPE_INT32
		elif type(value) == type(1.0) :
			return cls.VALUE_TYPE_FLOAT32
		elif type(value) == type('') :
			return cls.VALUE_TYPE_STRING
		elif type(value) == type({}):
			return cls.VALUE_TYPE_DICT
		elif type(value) == type([]) :
			return cls.VALUE_TYPE_LIST
		elif type(value) == type(True) :
			return cls.VALUE_TYPE_BOOL
		elif type(value) == type(None):
			return cls.VALUE_TYPE_NULL

		assert(False)
	
	@classmethod
	def getTypeDefaultValue(cls, type) :
		if cls.VALUE_TYPE_INT64 == type :
			return 0
		elif cls.VALUE_TYPE_INT32 == type :
			return 0
		elif cls.VALUE_TYPE_FLOAT32 == type :
			return 0.0
		elif cls.VALUE_TYPE_STRING == type :
			return ''
		elif cls.VALUE_TYPE_DICT == type :
			return {}
		elif cls.VALUE_TYPE_LIST == type :
			return []
		elif cls.VALUE_TYPE_BOOL == type :
			return False
		elif cls.VALUE_TYPE_NULL == type :
			return None

		assert(False)
