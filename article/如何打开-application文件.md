# 如何打开.application文件?

（经过大家的大量实践证明，这个方法不靠谱，这篇文章就当看着玩儿吧……）

.application后缀的文件是ClickOnce应用程序部署清单，在IE下点击后缀为.application的链接可以直接安装应用程序，其他浏览器下很可能会把这个.application文件下载下来，不过不用担心，下载下来的文件双击后一样能正常安装应用程序。

有极少数用户在点击我的豆瓣电台软件主页上的“立即使用”后下载下来一个文件名为doubanfm.application的文件，但却无法打开它，原因是缺少默认的打开方式（或者打开方式设置错误）。出现这个问题有两种可能，一种是没安装.NET Framework，解决方法就是安装一个.NET Framework。另一种情况很少有人遇到，就是已安装.NET Framework，但仍然无法打开，具体原因未知。

正常情况下安装.NET Framework后.application格式会自动关联到ClickOnce应用程序部署支持库上。如果安装.NET Framework后.application文件仍无法打开，可以尝试修复文件关联到“%WINDIR%\System32\dfshim.dll”这个文件上。

具体方法如下：

1、Shift+右键点击一个.application文件，选择“打开方式”或“打开方式——选择默认程序”。

[<img style="background-image: none; padding-top: 0px; padding-left: 0px; display: inline; padding-right: 0px; border-width: 0px;" title="无标题" alt="无标题" src="/attachment/up/blog/images/f9759a021aef_EC17/thumb.jpg" width="395" height="357" border="0" />](/attachment/up/blog/images/f9759a021aef_EC17/9408e2fc94c9.jpg)

2、勾选“所有.application文件都用这个应用打开”，然后选择“浏览”或“更多选项——在这台电脑上查找其他应用”。

[<img style="background-image: none; padding-top: 0px; padding-left: 0px; display: inline; padding-right: 0px; border: 0px;" title="无标题2" alt="无标题2" src="/attachment/up/blog/images/f9759a021aef_EC17/2_thumb_3.jpg" width="372" height="458" border="0" />](/attachment/up/blog/images/f9759a021aef_EC17/2_3.jpg)

3、在新出现的窗口中直接输入文件名“%WINDIR%\System32\dfshim.dll”，然后点击打开即可。

[<img style="background-image: none; padding-top: 0px; padding-left: 0px; display: inline; padding-right: 0px; border-width: 0px;" title="无标题3" alt="无标题3" src="/attachment/up/blog/images/f9759a021aef_EC17/3_thumb.jpg" width="504" height="316" border="0" />](/attachment/up/blog/images/f9759a021aef_EC17/3.jpg)

未经严格测试，请无法打开.application文件的用户试试看是否有效并留言。

# 评论

发布者 | 时间 | 内容
--- | --- | ---
Janice | 2012-12-30 21:34:11 | 我记得原来一点几的版本是可以有安装路径的貌似。现在确实不喜欢他默认安装C盘~
Lovages | 2012-12-24 17:02:01 | 我是Win 7 64，还是装成功了的，使用也没甚大问题，就是打开慢一点。
Lovages | 2012-12-24 17:00:44 | 安装了，也很好用，就是不知道软件装在哪个目录下，只能从开始菜单打开。。。。
cheng | 2012-11-22 13:32:46 | 关于这款软件<br/>win7 64位系统没装成功过<br/>win8 64位系统下体验是很不错的<br/>东西也都很好，但是有个问题<br/>经常会让我再装一遍，这很奇怪<br/>希望还是换回传统的方式<br/>或是建议可以投到微软WIN8 METRO界面去也行
飛了のXin | 2012-11-19 16:38:02 | 现在 还 停留在 2.0.5这个版本上
嗯哼~ | 2012-11-17 14:57:51 | WIn7 x64 .NET 4.5 打开时提示“不是有效的win32程序”
kii | 2012-11-10 18:33:14 | 我弱弱地想知道这个东西每次打开怎么打开？文章貌似说了安装的问题，但是我开机我根本找不到，如何去启动这个电台，真心急啊！！！还是得到网站来点一次下载它才奔出来
yuan | 2012-10-19 15:22:20 | 安装.NET Framework后直接双击doubanfm.application就可以安装了。
soloyu | 2012-10-05 19:09:53 | 还是不行的路过，同样提示不是有效的Win32应用程序的，郁闷啊
xinqing | 2012-09-30 23:24:56 | 同感。
Fs | 2012-09-24 18:28:50 | 博主能否提供个exe的版本啊? oc的都是安装到C盘的实在不喜欢啊...
xxx | 2012-09-17 19:20:52 | 不会啊，，这个平台其他的一些游戏什么的都有需要的，，应该是没问题的啊
K.F.Storm | 2012-09-16 21:41:34 | 会不会是你安装.NET时被360什么的阻止了文件关联？
K.F.Storm | 2012-09-16 21:38:31 | 看来这个方法还是不行了……
xxx | 2012-09-16 20:25:30 | 多谢啊，，文件倒是关联到了，，打开的时候提示doubanfm.application不是有效的Win32应用程序，下载的还是IE下载都是如此啊，，
