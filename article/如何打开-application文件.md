# 如何打开.application文件?

（经过大家的大量实践证明，这个方法不靠谱，这篇文章就当看着玩儿吧……）

.application后缀的文件是ClickOnce应用程序部署清单，在IE下点击后缀为.application的链接可以直接安装应用程序，其他浏览器下很可能会把这个.application文件下载下来，不过不用担心，下载下来的文件双击后一样能正常安装应用程序。

有极少数用户在点击我的豆瓣电台软件主页上的“立即使用”后下载下来一个文件名为doubanfm.application的文件，但却无法打开它，原因是缺少默认的打开方式（或者打开方式设置错误）。出现这个问题有两种可能，一种是没安装.NET Framework，解决方法就是安装一个.NET Framework。另一种情况很少有人遇到，就是已安装.NET Framework，但仍然无法打开，具体原因未知。

<!--more-->

正常情况下安装.NET Framework后.application格式会自动关联到ClickOnce应用程序部署支持库上。如果安装.NET Framework后.application文件仍无法打开，可以尝试修复文件关联到“%WINDIR%\System32\dfshim.dll”这个文件上。

具体方法如下：

1、Shift+右键点击一个.application文件，选择“打开方式”或“打开方式——选择默认程序”。

[<img style="background-image: none; padding-top: 0px; padding-left: 0px; display: inline; padding-right: 0px; border-width: 0px;" title="无标题" alt="无标题" src="/attachment/up/blog/images/f9759a021aef_EC17/thumb.jpg" width="395" height="357" border="0" />](/attachment/up/blog/images/f9759a021aef_EC17/9408e2fc94c9.jpg)

2、勾选“所有.application文件都用这个应用打开”，然后选择“浏览”或“更多选项——在这台电脑上查找其他应用”。

[<img style="background-image: none; padding-top: 0px; padding-left: 0px; display: inline; padding-right: 0px; border: 0px;" title="无标题2" alt="无标题2" src="/attachment/up/blog/images/f9759a021aef_EC17/2_thumb_3.jpg" width="372" height="458" border="0" />](/attachment/up/blog/images/f9759a021aef_EC17/2_3.jpg)

3、在新出现的窗口中直接输入文件名“%WINDIR%\System32\dfshim.dll”，然后点击打开即可。

[<img style="background-image: none; padding-top: 0px; padding-left: 0px; display: inline; padding-right: 0px; border-width: 0px;" title="无标题3" alt="无标题3" src="/attachment/up/blog/images/f9759a021aef_EC17/3_thumb.jpg" width="504" height="316" border="0" />](/attachment/up/blog/images/f9759a021aef_EC17/3.jpg)

未经严格测试，请无法打开.application文件的用户试试看是否有效并留言。
