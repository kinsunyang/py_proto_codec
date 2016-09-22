# py_proto_codec
- 本代码主要是将python dict序列化为binary数据，并生成相应的协议模板。
- 主要应用场景是用python写的网络服务在发固定协议的包时，简化操作，压缩数据量。

## 目的
- 作为本人的github练手项目
- python网络收发包时，有以下几种常用的方式
    1. 直接用struct.pack/unpack压解包。该方法实用于简单协议，对dict/list等复合数据处理起来稍显繁琐。
    2. 用protobuffer。该方法需要先定义好协议文件，然后用protobuffer生成相应的编解码程序。对于开发初期，协议变化较快时，需要经常修改协议文件。
    3. 直接用bson库序列化，不需要协议，反序列化之后就是一个可用的dict数据，灵活，扩展性好。缺点是数量量会较大，因为包含了所有数据的key。
- 本文的实现要点
    1. 根据dict数据自动生成协议文件。开发初期协议变动，只要重新跑一遍就有新的协议
    2. 底层仍是采用struct编解码
    3. 目前支持int/float/string/list/dict这些基本类型，list中的元素==只支持相同类型==
    4. 生成的协议保存为python tuple，可直接加载。每个field生成为(key, type, sub_field)，其中sub_field只对list/dict这种复活数据类型有效。

## Example
输入数据为  
```
data = {  
    'a' : 1,   
    'b' : 1.5,   
    'c' : 'hello world',  
    'd' : {  
            'level1' : False,   
            'x' : {   
                'level2' : {  
                    'ok' : 'ok'  
                },   
                'y' : [1, -2, 3]  
            }   
    },   
    'ccc' : None,   
    'userid' : 100010000032  
}    
```

则生成的协议为    
```
proto = [
    ('a', 16, None), 
    ('c', 2, None), 
    ('b', 1, None), 
    ('d', 3, (
                ('level1', 8, None), 
                ('x', 3, (
                            ('y', 4, (None, 16, None)), 
                            ('level2', 3, (
                                ('ok', 2, None),)
                            )
                        )
                )
            )
    ), 
    ('ccc', 10, None), 
    ('userid', 18, None)
]
```  
其中类型定义与bson基本保持一致

## TODO
- 如何在不强制升级的情况下，兼容旧的协议
- 
