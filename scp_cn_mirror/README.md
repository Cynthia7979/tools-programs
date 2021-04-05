# SCP-CN Backup Tool SCP-CN备份工具

在四月一日的事件之后，为了避免中分失去更多文章，我做了这个本地备份工具，用于批量下载文章到本地。

## 特性和注意事项
* 这是一天以内写的代码，有可能会有bug，如果有的话请开个Issue告诉我。
* 本工具会下载网站的**HTML源码** 和 **（可选）Wikidot源码**
* 关于Wikidot源码：
    * 抓取代码来自[CSharperMantle](https://github.com/CSharperMantle)写的[scp_fetcher_bs4](https://github.com/CSharperMantle/scp_fetcher_bs4/)
    * 程序会先打开中分主页，在提示“`请在打开的窗口中登录，完成后按回车键>`”后，请登陆自己的WikiDot帐号，登录完成后请在命令行按回车
    * 如果主页显示不正确，可以刷新页面
    * 此后的抓取会自动进行，将打开的浏览器窗口最小化即可。
    * 如果嫌太慢，可以在页面大概加载完毕时手动停止加载——但请注意不要太早停止加载，这有可能会导致js代码不完全，从而无法抓取源码
    * 目前仅支持单线程备份，可能会花较长时间，且不是很稳定，备份大量页面时建议关掉（见“修改变量”）
    * **注意：** `deleted:`分类不会显示源码，因此本工具会**自动跳过**备份源码的步骤
* 如果你的作品引用了任何外部代码或图片，请手动备份这些文件。本工具只会备份文本和（写在module里的）CSS。
* 如果目标目录不存在，本工具会自动创建该目录
* 如果已有同名的文件，工具会**跳过**该页面，并继续备份其他页面
* 由于Windows不允许文件名出现冒号，我把**所有":"都统一替换成了";"**，如果找不到文件还请注意
* 本工具需要`python`及其`requests`, `selenium` 和`BeautifulSoup4`库，以及浏览器驱动，下载方式见下

## 使用方法

### 安装必要的库
* 如果你是有经验的用户：
    * `Python`版本是3.7.9
    * `requests` 2.25.1
    * `beautifulsoup4` 4.9.3
    * `selenium` 3.141.0
    * `geckodriver`、`operachromiumdriver`和`chromedriver`需要其一，且需要在`PATH`中
* 否则请看这里：
    * 在[这里](https://www.python.org/downloads/release/python-379/#Files)下载你的操作系统的Python安装包
    * 运行安装包，一路点继续完成安装
    * 按`Ctrl+R`（Mac用户请打开Terminal）打开命令行，输入`pip install requests`
    * 在它停止蹦出新的提示后，输入`pip install beautifulsoup4`
    * 在它又一次停止蹦出新的提示后，输入`pip install selenium`
    * 如果你不需要备份源码，可以跳过下列步骤
        * 如果你安装了火狐浏览器（Firefox），请：
            * 参考[这个教程](https://blog.csdn.net/rhx_qiuzhi/article/details/80296801)安装Windows或Ubuntu的`geckodriver`
            * 如果你是Mac用户，参考[这篇文章](https://blog.csdn.net/vulnerableyears/article/details/92016645)安装
        * 如果你安装了Google Chrome浏览器，请：
            * 参考[这个教程](https://www.jianshu.com/p/dc0336a0bf50)安装`chromedriver`
        * 如果你安装了Opera浏览器，请：
            * 先将Opera升级到最新版本
            * 在[这里](https://github.com/operasoftware/operachromiumdriver/releases)下载`operachromiumdriver`
            * 将压缩包最内部的`operadriver.exe`和`sha512_sum`拷贝到Opera的安装目录下，版本号最高的文件夹中（即你现在使用的版本）
            * 将版本号的目录路径添加到环境变量（PATH）中——如果你不知道怎么做，请百度对应操作系统的环境变量编辑方法，或者参考上面的两篇文章
        * 如果哪个都没装的话，就随便选一个浏览器从头安装吧……
    * 完成

### 修改变量
考虑到时间问题，我没有实现命令行参数。因此，如果需要自定义拉取主页和存储目录，你需要直接修改源代码——不用担心，这很简单。

* 下载本目录中的`scp_cn_mirror.py`文件
* 用记事本 或 你喜欢的编辑器 或 “运行程序”中提到的IDLE 打开这个文件
* 有以下几个内容可以自定义：
    * 第8行 **`mirror_dir`**：存储html文件的目录，将两个单引号之间的内容修改至目录的绝对路径。如：`F://scp-wiki-cn/mirror/`，`C://mirror/`
    * 第9行 **`source_dir`**：存储wikidot源码的目录，同上
    * 第11行 **`fetch_source`**：是否备份源码，`True`为是，`False`为否
    * 第13行 **`driver`**：使用哪个浏览器驱动获取源码，可以填`'firefox'`（火狐浏览器）、`'opera'`、或`'chrome'`（Google Chrome浏览器）
        * 上面下载了哪个驱动就填哪个
        * 不用备份源码就不用改
    * 第16行 **`home_page`**：[标签搜索](http://scp-wiki-cn.wikidot.com/tag-search)结果页链接。将两个双引号之间的内容修改至链接，以`/`字符结尾。代码里已经给出了几个可用的链接，可以注释掉（在前面加“#”）不需要的链接并留下要用的。如果需要进一步自定义链接，请见下方“如何获取`home_page`？”
    * 第26行 **`overwrite`**：如果同名文件存在，是否覆盖。`True`为是，`False`为否，如果你希望更新文件，请设为`True`
    * 第27和28行 **`start_page`**和**`end_page`**：起始和结束页码，对应标签搜索结果页面的分页，最低为1。
        * 提示：如果备份中断，可以将`start_page`更改为上一次停止的页码（在日志中寻找Iter字样，后面的数字就是）来加快速度

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
