# SCP-CN Backup Tool SCP-CN备份工具

在四月一日的事件之后，为了避免中分失去更多文章，我做了这个本地备份工具，用于批量下载文章到本地。

## 特性和注意事项
* 这是一天以内写的代码，有可能会有bug，如果有的话请开个Issue告诉我。
* 本工具会下载网站的HTML源码，**而非纯文字或Wikidot源码**。这是为了最大限度地保留原文风格所考虑，也是因为Wikidot源码的API需要一个目前无法获取到的页面ID。
* 本工具需要`python`及其`requests`和`BeautifulSoup4`库，下载方式见下

## 使用方法

### 安装必要的库
* 如果你是有经验的用户：
    * `Python`版本是3.7.9
    * `requests` 2.25.1
    * `beautifulsoup4` 4.9.3
* 否则请看这里：
    * 在[这里](https://www.python.org/downloads/release/python-379/#Files)下载你需要的操作系统安装包
    * 运行安装包，一路点继续完成安装
    * 按`Ctrl+R`（Mac用户请打开Terminal）打开命令行，输入`pip install requests`
    * 在它停止蹦出新的提示后，输入`pip install beautifulsoup4`
    * 完成

### 修改变量
考虑到时间问题，我没有实现命令行参数。因此，如果需要自定义拉取主页和存储目录，你需要直接修改源代码——不用担心，这很简单。

* 下载本目录中的`scp_cn_mirror.py`文件
* 用记事本或者你喜欢的编辑器打开这个文件
* 有以下几个内容可以自定义：
    * 第六行 **`mirror_dir`**：存储html文件的目录，将两个单引号之间的内容修改至目录的绝对路径。如：`F://scp-wiki-cn/mirror/`，`C://mirror/`
    * 第九行 **home_page**：页面链接来源，目前只支持[标签搜索](http://scp-wiki-cn.wikidot.com/tag-search)生成的链接。将两个双引号之间的内容修改至链接，以`/`字符结尾。
        * **如何获取`home_page`？**
