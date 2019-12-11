# Bing Wallpaper 1.0.0.0

[去年](/article/bingwallpaper)我发布了一个自动更换桌面背景为当日的Bing首页图片的小软件，在之后的使用过程中我一直设置了开机启动，但总觉得托盘上的图标很碍眼。于是这两天写了个新版本。新版本没有托盘图标，双击运行会打开一个窗口，里面包含版本信息、设置、当日图片的链接等。这个窗口可以关闭，Bing Wallpaper仍然会在后台运行。关闭窗口后如果想再次打开这个窗口，或者想退出Bing Wallpaper，请再次双击运行程序的exe文件。开机启动是不会显示这个窗口的（仍然可以之后双击exe以显示窗口），比较清静。

[<img style="background-image: none; padding-top: 0px; padding-left: 0px; display: inline; padding-right: 0px; border: 0px;" title="" src="/attachment/up/blog/images/Bing-Wallpaper-1.0.0.0_13083/thumb.png" alt="" width="504" height="316" border="0" />](/attachment/up/blog/images/Bing-Wallpaper-1.0.0.0_13083/5bb006fc3b9e.png)

本应用需要.NET Framework 3.5以上版本的支持。

各Windows版本自带的.NET Framework版本列表：

Windows XP或更早的系统：无

Windows Vista：.NET Framework 3.0

Windows 7：.NET Framework 3.5

Windows 8：.NET Framework 4.5

[完整列表请看这里](http://jianyun.org/archives/667.html)

由于Windows 8自带的是.NET 4.5，而.NET 3.5向下兼容至.NET 2.0，.NET 4.5向下兼容至.NET 4.0，所以全新安装的Windows 8系统是运行不了.NET 3.5应用的。为了免去Win8用户下载庞大的.NET 3.5安装程序的烦恼，Bing Wallpaper发布了.NET 3.5版和.NET 4.0版，包含在同一个压缩包中，大家按需使用。（电脑内同时安装了.NET 3.5和.NET 4.0/4.5的童鞋就不要纠结了，随便选一个用就是。）

[下载地址](/attachment/up/bingwallpaper/BingWallpaper_1.0.0.0.zip)

博主一向无私，所以Bing Wallpaper也开源了。[去GitHub看看](https://github.com/kfstorm/BingWallpaper)。

# 评论

发布者 | 时间 | 内容
--- | --- | ---
华 | 2013-08-01 09:34:01 | 我一直在找个中文版的，一直没找到bing 出了一个缤纷桌面是国际版的，所以不爽
泉 | 2013-07-11 11:41:06 | 能更新个1.01版本，保存7天内的图片，第二天自动删除最旧的一张。这样就可以使用win8的幻灯片桌面功能，几分钟换个桌面。<br/>谢谢！
lmq | 2013-07-05 11:40:45 | 希望能设置为拉伸，而不是平铺，可以做一个设置项。
Sail | 2013-05-31 21:09:04 | 很棒！！<br/>希望改成中文bing，更迎合中国人的偏好。非常感谢作者的努力
彼时我心 | 2013-05-31 20:37:24 | 改一下路径
彼时我心 | 2013-05-31 20:36:47 | set "Ymd=%date:~,4%%date:~5,2%%date:~8,2%"<br/>copy C:\Users\wangkai\AppData\Roaming\K.F.Storm\BingWallpaper\image.jpg E:\wallpaper\%Ymd%.jpg
fans | 2013-04-05 16:43:27 | 确实是小巧精湛的软件，不过还是希望能加上保存图片到指导文件夹，并按照图片名或者日期命名<br/>ps：这个貌似会更新图片后自动退出么？
K.F.Storm | 2013-03-26 13:52:19 | 由于图片来源是国际版的Bing，所以壁纸的更新时间大概是北京时间每天下午3点左右。
Thanks | 2013-03-25 17:23:33 | 哇，太好用了~~找半天终于找到这款软件，喜欢，感谢作者的无私奉献~~网上有找到你的0.9版本的，但是总不放心，后来顺蔓摸瓜找到原作者的博客下载，安全又是最新的~总之，谢谢
sixfancy | 2013-03-25 11:24:41 | 为什么只能同步美国的图片?  时区设置是正确的.
张奕 | 2013-02-13 17:43:49 | 请教下<br/>我想做个bat<br/>可以把<br/>[C:\Users\Administrator\AppData\Roaming\K.F.Storm\BingWallpaper\image.jpg]<br/>复制到<br/>[F:\wallpaper]<br/>并更名为当天日期yyyymmdd<br/><br/>怎么写....
yoyodadada | 2013-02-07 11:52:09 | 果断下载，看看效果如何
