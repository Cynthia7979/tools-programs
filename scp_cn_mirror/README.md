# SCP-CN Backup Tool SCP-CN备份工具

在四月一日的事件之后，为了避免中分失去更多文章，我做了这个本地备份工具，用于批量下载文章到本地。

## 特性和注意事项
* 这是一天以内写的代码，有可能会有bug，如果有的话请开个Issue告诉我。
* 本工具会下载网站的HTML源码，**而非纯文字或Wikidot源码**。这是为了最大限度地保留原文风格所考虑，也是因为Wikidot源码的API需要一个目前无法获取到的页面ID。
* 如果你的作品引用了任何外部代码或图片，请手动备份这些文件。本工具只会备份文本和（写在module里的）CSS。
* 如果目标目录不存在，本工具会自动创建该目录
* 如果已有同名的文件，工具会**跳过**该页面，并继续备份其他页面
* 本工具需要`python`及其`requests`和`BeautifulSoup4`库，下载方式见下

## 使用方法

### 安装必要的库
* 如果你是有经验的用户：
    * `Python`版本是3.7.9
    * `requests` 2.25.1
    * `beautifulsoup4` 4.9.3
* 否则请看这里：
    * 在[这里](https://www.python.org/downloads/release/python-379/#Files)下载你的操作系统的Python安装包
    * 运行安装包，一路点继续完成安装
    * 按`Ctrl+R`（Mac用户请打开Terminal）打开命令行，输入`pip install requests`
    * 在它停止蹦出新的提示后，输入`pip install beautifulsoup4`
    * 完成

### 修改变量
考虑到时间问题，我没有实现命令行参数。因此，如果需要自定义拉取主页和存储目录，你需要直接修改源代码——不用担心，这很简单。

* 下载本目录中的`scp_cn_mirror.py`文件
* 用记事本 或 你喜欢的编辑器 或 “运行程序”中提到的IDLE 打开这个文件
* 有以下几个内容可以自定义：
    * 第六行 **`mirror_dir`**：存储html文件的目录，将两个单引号之间的内容修改至目录的绝对路径。如：`F://scp-wiki-cn/mirror/`，`C://mirror/`
    * 第九行 **`home_page`**：[标签搜索](http://scp-wiki-cn.wikidot.com/tag-search)结果页链接。将两个双引号之间的内容修改至链接，以`/`字符结尾。代码里已经给出了几个可用的链接，可以注释掉（在前面加“#”）不需要的链接并留下要用的。如果需要进一步自定义链接，请见下方“如何获取`home_page`？”
    * 第十五和十六行 **`start_page`**和**`end_page`**：起始和结束页码，对应标签搜索结果页面的分页，最低为1。

#### 如何获取`home_page`？
1. 打开[标签搜索](http://scp-wiki-cn.wikidot.com/tag-search)页面
2. 按照页面提示输入你需要的条件
3. 点击“在新标签页打开检索结果”
4. 拷贝新页面的链接
5. 粘贴到第九行的双引号中间，在链接的最后添加一个`/`（如果没有的话）
6. 恭喜你，你得到了你的自定义`home_page`

### 运行程序
* 如果你是有经验的用户：
   * 使用你的环境直接运行`scp_cn_mirror.py`即可
* 否则请看这里：
   * 为了看到所有log信息，请在搜索中查找"IDLE (Python GUI)"并运行
   * 在打开的窗口的顶端栏里，选择“File”-“Open...”-找到修改好的`scp_cn_mirror.py`并打开
   * 在新窗口的顶端栏里，点击“Run”-“Run Module”
   * 程序现在在运行了，具体进度会显示在Shell窗口中（如果看不懂日志消息，可以问下我（）

## 这好像……不怎么符合预期？
如果你遇到了任何bug或者有想要改进的地方，请[创建一个Issue](https://github.com/Cynthia7979/tools-programs/issues/new)或[Pull request](https://github.com/Cynthia7979/tools-programs/compare)来报告问题或贡献。
