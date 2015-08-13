# toolkits
just toolkits

## extractor.py
网页信息抽取工具，只需修改模板配置文件即可对指定站点信息进行抽取

输入文件格式： 每行一个URL

输出格式： 对应输入文件每行URL的网页抽取结果

###使用说明 
(1) 在配置文件template.conf配置模板
以bing.com的搜索结果页抽取为例
```
pattern:http://cn.bing.com/dict/search?q=.*
[\#text]:span'class@def'

```
 pattern为网页的URL pattern，程序通过网页的URL和pattern来选取对应的抽取模板 

[\#text]:span[class@def] 表示抽取的字段名为text， 该字段的值为html中span标签的文本，且该标签的class属性为def。

*高级语法*

(1) group 型字段

```
[people] : div'class@people'
[people#name] : div'class@name' 
[people#gender] : div'class@gender'
```
如果抽取的字段由多个属性构成，那么可以指定这些属性的公共节点，以保持抽取的属性字段位于同一个公共节点中。(没有#的字段名不会输出）

(2) 节点顺序指定
```
[people#name] : div'class@name'/p[3] 

```
如果字段无法通过节点的属性进行区分,可以指定节点在其父节点下的顺序来进行匹配, 如上的例子表示抽取class属性为name的div节点下的第3个p节点文本为name字段的值

(3) 文本前缀指定
```
[people#name] : div'class@name'/p'prefix@名字' 

```
对于动态生成的网页，字段对应的路径不是固定的，可以通过指定节点文本的前缀来进行区分, 上面的例子只会匹配文本前缀为“名字”的p节点



## mtranslator.py
支持湘雅医学词典和Bing在线翻译

输入文件格式: ID,ENGLISH_TERM

数据文件格式：ID \tab ENGLISH_TERM \tab 字典名 \tab 中文解释 

##calc_str_sim.cpp
计算中文字符串相似度，支持设置不同匹配部分权重（代码中已设置中文疾病名相似权重）




