# A Simple Python Toolbox for Generating Latex from Markdown txt

### Installation:

```python
pip install pydbeamer -i https://www.pypi.org/simple/
```

There are three ways to generating latex files
1. write the like-markdown file for generating a document, which is simpler
2. write the objects for building a document, which is more flexible
3. combine the obove two methods


V0.3.9

## 1. write the like-markdown file for generating a document, which is simpler
### 结果示例
http://python2022.cloud:8501

### 参考md文件
```python
# 标题1, 副标题1
# 标题2, 副标题2

## Section1

--- 当前Section第一页幻灯片

```teal
title: 这是颜色为teal的一个Box
1. # title为可选项, 一个井号表示最大号字体
2. ##b 注意开始和结束的标识, 两个井号表示次大号字体, b表示蓝色, 有b, r, k, p四种颜色可选
```

--- 当前Section第二页幻灯片

```bgreen
title: 这是一段代码
```python
def sum(a, b):
    return a + b
```
```

## Section2
--- 第一页幻灯片
||
lratio: 0.48
```teal
title: 这是一个分栏显示
para: 表示一个段落, 与其他的区分
- 表示列表项1
- 表示接下来的列表项
```
|

```teal
title: 这是右边栏
- 列表项1
- 列表项2
```
||
```

```python
filename = "demo.md" # 上面的markdown语句对应的文件
f = open(filename)
txt = f.read()
LatexFile(txt)
```

## 2. write the objects for building a document, which is more flexible

```python
from pydbeamer.pydbeamer import *
title0 = TitlePage("标题1", "副标题1")
title1 = TitlePage("标题2", "副标题2")
#一般可以在各个字符串里输入需要的latex语句

doc = Beamer(title0, title1) #可以有一个标题页或多个标题页
s = Section("Section1", parent = doc)
f = Frame("当前Section第一页幻灯片", parent = s)
b = tealBox('这是颜色为teal的一个Box', parent = f)
l1 = "第一行示例"
l2 = "第二行示例"
nl = NumList(*l(2), parent = b)

f = Frame("当前Section第二页幻灯片", parent = s)

b = bgreenBox('这是一段代码', parent = f)
code = '''
def sum(a, b):
    return a + b
'''
pb = PythonBlock(code, "demo", head = False, parent = b)
#####################################################
s = Section("Section2", parent = doc)
f = Frame("第一页幻灯片", parent = s)
cols = Columns(parent = f, no = 2)

b = tealBox('这是一个分栏显示', parent = cols.left)
Para("表示一个段落, 与其他的区分", parent = b)
l1 = '表示列表项1'
l2 = '表示接下来的列表项'
nl = ItemList(*l(2), parent = b)

b = tealBox('这是右边栏', parent = cols.right)
i1 = "列表项1"
i2 = "列表项2"
il = ItemList(*i(2), parent = b)

doc.build() #生成文档

```
### 查看详细的函数和类的说明
```python
import pydbeamer.pydbeamer as P
help(P) 
```


