# -*- coding: utf-8 -*- 

#---------------------------------
from proto_manager import ProtoMgr

mgr = ProtoMgr()
def encode(data, proto) :
	return mgr.encode(data, proto)

def decode(bin, proto) :
	return mgr.decode(bin, proto) 
