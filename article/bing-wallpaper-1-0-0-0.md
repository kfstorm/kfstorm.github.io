# Bing Wallpaper 1.0.0.0

[去年](http://www.kfstorm.com/blog/2012/05/19/bingwallpaper/)我发布了一个自动更换桌面背景为当日的Bing首页图片的小软件，在之后的使用过程中我一直设置了开机启动，但总觉得托盘上的图标很碍眼。于是这两天写了个新版本。新版本没有托盘图标，双击运行会打开一个窗口，里面包含版本信息、设置、当日图片的链接等。这个窗口可以关闭，Bing Wallpaper仍然会在后台运行。关闭窗口后如果想再次打开这个窗口，或者想退出Bing Wallpaper，请再次双击运行程序的exe文件。开机启动是不会显示这个窗口的（仍然可以之后双击exe以显示窗口），比较清静。

[<img style="background-image: none; padding-top: 0px; padding-left: 0px; display: inline; padding-right: 0px; border: 0px;" title="" src="/attachment/upblog/images/Bing-Wallpaper-1.0.0.0_13083/_thumb.png" alt="" width="504" height="316" border="0" />](/attachment/upblog/images/Bing-Wallpaper-1.0.0.0_13083/5bb006fc3b9e.png)

<!--more-->

本应用需要.NET Framework 3.5以上版本的支持。

各Windows版本自带的.NET Framework版本列表：

Windows XP或更早的系统：无

Windows Vista：.NET Framework 3.0

Windows 7：.NET Framework 3.5

Windows 8：.NET Framework 4.5

[完整列表请看这里](http://jianyun.org/archives/667.html)

由于Windows 8自带的是.NET 4.5，而.NET 3.5向下兼容至.NET 2.0，.NET 4.5向下兼容至.NET 4.0，所以全新安装的Windows 8系统是运行不了.NET 3.5应用的。为了免去Win8用户下载庞大的.NET 3.5安装程序的烦恼，Bing Wallpaper发布了.NET 3.5版和.NET 4.0版，包含在同一个压缩包中，大家按需使用。（电脑内同时安装了.NET 3.5和.NET 4.0/4.5的童鞋就不要纠结了，随便选一个用就是。）

[下载地址](/attachment/upBingWallpaper_1.0.0.0.zip)

博主一向无私，所以Bing Wallpaper也开源了。[去GitHub看看](https://github.com/kfstorm/BingWallpaper)。
