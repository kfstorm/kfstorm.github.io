# 在.NET中利用内存映射实现进程间通信

### 一、为什么要用进程间通信？

在我写的豆瓣电台里，有一个利用Win7任务栏中的跳转列表实现频道切换的功能，截图如下：

[<img style="background-image: none; border-bottom: 0px; border-left: 0px; padding-left: 0px; padding-right: 0px; display: inline; border-top: 0px; border-right: 0px; padding-top: 0px" title="image5" border="0" alt="image5" src="http://up.kfstorm.com/blog/images/d0dc2d75cb07.NET_13ADA/image5_thumb.jpg" width="230" height="498" />](http://up.kfstorm.com/blog/images/d0dc2d75cb07.NET_13ADA/image5.jpg)

当点击列表中的频道时，豆瓣电台就能够切换到相应的频道。

这和进程间通信有什么关系呢？原来跳转列表中的一个个频道其实是一个个任务，每个任务都是一个命令行，有执行文件的路径，也有参数。

<!--more--><pre class="brush:csharp">/// &lt;summary&gt;

/// 将频道添加到跳转列表

/// &lt;/summary&gt;

private void AddChannelToJumpList(Channel channel)

{

JumpList jumpList = JumpList.GetJumpList(App.Current);

if (jumpList == null) jumpList = new JumpList();

jumpList.ShowRecentCategory = true;

jumpList.ShowFrequentCategory = true;

foreach (JumpTask jumpItem in jumpList.JumpItems)

{

if (jumpItem.Title == channel.Name) return;

}

JumpTask jumpTask = new JumpTask();

jumpTask.Title = channel.Name;

jumpTask.Description = jumpTask.Title;

jumpTask.Arguments = channel.ToCommandLineArgs();

JumpList.AddToRecentCategory(jumpTask);

JumpList.SetJumpList(App.Current, jumpList);

}</pre>

每次点击一个跳转列表里的项目，实际上都是启动了一个代参数的豆瓣电台的实例，如果不加任何处理，就会打开另外一个豆瓣电台，这与切换频道的初衷不符，我们希望的是始终只运行一个豆瓣电台。于是我们就可以这样做：启动代参数的豆瓣电台时，立即告诉正在运行的豆瓣电台，让它更换频道，然后新打开的豆瓣电台在还没有显示界面时就立即退出。这就涉及到进程间通信了。

### 二、进程间通信要点一：找到要与之通信的进程

以豆瓣电台为例，只有当已经有一个豆瓣电台在运行时，才需要进程间通信，如果当前没有运行，那么点击跳转列表中的频道时应当启动一个新实例。如何判断豆瓣电台是否已经在运行呢？有如下几种方法：

##### 1、查找窗口

利用Win32 API函数FindWindow，可以方便地找到特定的窗口的句柄，如果能够找到豆瓣电台的窗口，那就说明豆瓣电台已经在运行了。FindWindow接受两个参数，一个是窗口标题，另一个是窗口类别名。

##### 2、获取进程列表

利用System.Diagnostics.Process类，可以方便地判断一个程序的另一个实例是否已经在运行：

/// 检测是否有另一个实例正在运行

/// &lt;/summary&gt;

bool HasAnotherInstance()

{

string fileName = Process.GetCurrentProcess().MainModule.FileName;

Process[] processes = Process.GetProcessesByName(fileName);

int count = 0;

foreach (var process in processes)

{

if (process.MainModule.FileName == fileName) ++count;

if (count &gt; 1) return true;

}

return false;

}</pre>

##### 3、使用互斥量、管道等基于内存映射的方法

具体方法在网上搜一搜就有，因为我没有试过，所以就不具体说了。

##### 4、直接使用内存映射

后面会详细说明。

### 三、进程间通信要点二：与进程通信

与进程通信也有几种方法：

##### 1、不太理想的方法：向窗口发送WM_COPYDATA消息

具体代码如下：

/// 使用COPYDATA，WM_USER只能用于应用程序内部的通讯，跨进程用COPYDATA

/// &lt;/summary&gt;

public const int WM_COPYDATA = 0x004A;

/// &lt;summary&gt;

/// 正确的窗口标题

/// &lt;/summary&gt;

public const string CorrectTitle = &quot;InteropWindow {CB66A0B0-DC2A-4F8C-BDA7-C2E1202D35AB}&quot;;

public InteropWindow()

{

InitializeComponent();

Title = CorrectTitle;

}

/// &lt;summary&gt;

/// 查找目标发送窗体

/// &lt;/summary&gt;

[DllImport(&quot;User32.dll&quot;, EntryPoint = &quot;FindWindow&quot;)]

public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);

[StructLayout(LayoutKind.Sequential)]

public struct CopyDataStruct

{

public IntPtr dwData;

public int cbData;//字符串长度

[MarshalAs(UnmanagedType.LPStr)]

public string lpData;//字符串

}

/// &lt;summary&gt;

/// 发送消息方法

/// &lt;/summary&gt;

[DllImport(&quot;User32.dll&quot;, EntryPoint = &quot;SendMessage&quot;)]

private static extern int SendMessage

(

IntPtr hWnd,                   //目标窗体句柄

int Msg,                       //WM_COPYDATA

int wParam,                                             //自定义数值

ref  CopyDataStruct lParam             //结构体

);

/// &lt;summary&gt;

/// SendMessage To Window

/// &lt;/summary&gt;

/// &lt;param name=&quot;windowName&quot;&gt;window的title，建议加上GUID，不会重复&lt;/param&gt;

/// &lt;param name=&quot;strMsg&quot;&gt;要发送的字符串&lt;/param&gt;

public static void SendMessage(string windowName, string strMsg)

{

if (strMsg == null) return;

IntPtr hwnd = FindWindow(null, windowName);

if (hwnd != IntPtr.Zero)

{

CopyDataStruct cds;

cds.dwData = IntPtr.Zero;

cds.lpData = strMsg;

//注意：长度为字节数

cds.cbData = System.Text.Encoding.Default.GetBytes(strMsg).Length + 1;

// 消息来源窗体

int fromWindowHandler = 0;

SendMessage(hwnd, WM_COPYDATA, fromWindowHandler, ref  cds);

}

}

private void Window_Loaded(object sender, RoutedEventArgs e)

{

(PresentationSource.FromVisual(this) as HwndSource).AddHook(new HwndSourceHook(this.WndProc));

}

/// &lt;summary&gt;

/// 接收消息

/// &lt;/summary&gt;

IntPtr WndProc(IntPtr hwnd, int msg, IntPtr wParam, IntPtr lParam, ref bool handled)

{

if (msg == WM_COPYDATA)

{

CopyDataStruct cds = (CopyDataStruct)System.Runtime.InteropServices.Marshal.PtrToStructure(lParam, typeof(CopyDataStruct));

List&lt;string&gt; commandLineArgs = new List&lt;string&gt;();

bool haveQuote = false;

StringBuilder sb = new StringBuilder();

foreach (char c in cds.lpData)

{

if (char.IsWhiteSpace(c) &amp;&amp; haveQuote == false)

{

if (sb.Length &gt; 0)

{

commandLineArgs.Add(sb.ToString());

sb.Clear();

}

}

else if (c == '\&quot;')

if (haveQuote)

{

commandLineArgs.Add(sb.ToString());

sb.Clear();

haveQuote = false;

}

else haveQuote = true;

else sb.Append(c);

}

if (sb.Length &gt; 0)

commandLineArgs.Add(sb.ToString());

Channel channel = Channel.FromCommandLineArgs(commandLineArgs);

if (channel != null)

(App.Current.MainWindow as DoubanFMWindow).InteropChangeChannel(channel);

}

return hwnd;

}</pre>

每次程序启动时，先用下面的代码检查豆瓣电台是否已经运行：



/// 检测是否有另一个实例正在运行

/// &lt;/summary&gt;

bool HasAnotherInstance()

{

IntPtr hwnd = InteropWindow.FindWindow(null, InteropWindow.CorrectTitle);

return hwnd != IntPtr.Zero;

}</pre>



如果已经运行，则用InteropWindow.SendMessage(InteropWindow.CorrectTitle, message)向窗口发送消息，然后立即退出。

WM_COPYDATA的不足：

### 

(1) WPF窗口的窗口类别每次启动都是随机的，这个可以通过Spy++看到，而豆瓣电台的窗口标题是随着当前播放的歌曲的变化而变化的，于是FindWindow无法找到豆瓣电台的主窗口，只好另外创建一个用户看不见的隐藏窗口（即上面的InteropWindow），并设置窗口标题为InteropWindow.CorrectTitle，程序不查找豆瓣电台的主窗口，而是查找隐藏窗口，并向隐藏窗口发送消息。是不是感觉有点非主流啊？

(2) 从Vista开始，微软出于安全性考虑，让以管理员权限运行的程序无法接收到以普通权限运行的程序的某些消息，WM_COPYDATA就是其中一个。你可能会问了，豆瓣电台怎么会用到管理员权限呢？还真用到了，一个典型的例子就是豆瓣电台的安装程序安装完成后，可以自动启动豆瓣电台，因为安装程序是以管理员权限启动的，所以豆瓣电台也自然有管理员权限了，这时通过跳转列表切换频道就失效了，只能关掉程序再重新打开一次。由于这个原因，使我最终放弃了WM_COPYDATA。对了，我也尝试过用获取进程列表的方法判断豆瓣电台是否在运行，最后也因为权限的问题而失败了。在执行下面这句时，如果process有管理员权限，就会抛出异常。

2、非主流方法：利用临时文件传递信息

新启动的程序如果检测到已经有豆瓣电台在运行，就会把要切换的频道写入一个临时文件，然后退出。而已经启动的豆瓣电台会定时检查是否那个临时文件存在，如果有，则读取频道信息，切换频道，然后删除临时文件。是不是感觉也有点非主流啊？

##### 3、今天的主角：内存映射

百度百科上对内存映射文件的解释：

<blockquote>

> </p>
内存映射文件，是由一个文件到一块内存的映射。Win32提供了允许应用程序把文件映射到一个进程的函数 (CreateFileMapping)。内存映射文件与虚拟内存有些类似，通过内存映射文件可以保留一个地址空间的区域，同时将物理存储器提交给此区域，内存文件映射的物理存储器来自一个已经存在于磁盘上的文件，而且在对该文件进行操作之前必须首先对文件进行映射。使用内存映射文件处理存储于磁盘上的文件时，将不必再对文件执行I/O操作，使得内存映射文件在处理大数据量的文件时能起到相当重要的作用。
<p>

</blockquote>

其时这个和写临时文件的方法很像，只不过写临时文件是在硬盘上写，而这个是在内存里写罢了，不过感觉没那么非主流了。

.NET Framework 4新增加了MemoryMappedFile类，利用MemoryMappedFile类，可以方便地进行内存映射。

要用到的成员方法：

string mapName,

long capacity

)</pre>


<p><br />或者

<br />

string mapName,

long capacity

)</pre>


<p><br />还有

<br />

string mapName

)</pre>

&#160;

CreateNew和CreateOrOpen用于创建（或打开）一个内存映射文件，选一个用就行了，OpenExisting用于打开一个已经存在的内存映射文件，CreateViewStream用于打开流，这样就可以像读写普通文件一样读写内存映射文件了。

创建的内存映射文件是在系统内存内的，不会因为创建文件的进程退出而销毁（除非显示指示销毁），而是当所有使用该文件的进程都退出后，系统自动回收内存。

具体实现：

主窗口有两个私有成员：



/// 用于进程间更换频道的内存映射文件

/// &lt;/summary&gt;

private MemoryMappedFile _mappedFile;

/// &lt;summary&gt;

/// 内存映射文件的文件名

/// &lt;/summary&gt;

private string _mappedFileName = &quot;{04EFCEB4-F10A-403D-9824-1E685C4B7961}&quot;;</pre>



主窗口的成员方法：

/// 检测是否有另一个实例正在运行

/// &lt;/summary&gt;

bool HasAnotherInstance()

{

try

{

MemoryMappedFile mappedFile = MemoryMappedFile.OpenExisting(_mappedFileName);

return mappedFile != null;

}

catch

{

return false;

}

}

/// &lt;summary&gt;

/// 将频道写入内存映射文件

/// &lt;/summary&gt;

void WriteChannelToMappedFile(Channel channel)

{

if (channel != null)

try

{

using (MemoryMappedFile mappedFile = MemoryMappedFile.OpenExisting(_mappedFileName))using (Stream stream = mappedFile.CreateViewStream())

{

BinaryFormatter formatter = new BinaryFormatter();

formatter.Serialize(stream, channel);

}

}

catch { }

}

/// &lt;summary&gt;

/// 从内存映射文件加载频道

/// &lt;/summary&gt;

Channel LoadChannelFromMappedFile()

{

try

{

using (Stream stream = _mappedFile.CreateViewStream())

{

BinaryFormatter formatter = new BinaryFormatter();

return (Channel)formatter.Deserialize(stream);

}

}

catch

{

return null;

}

}

/// &lt;summary&gt;

/// 清除内存映射文件的内容

/// &lt;/summary&gt;

void ClearMappedFile()

{

try

{

using (Stream stream = _mappedFile.CreateViewStream())

{

BinaryFormatter formatter = new BinaryFormatter();

formatter.Serialize(stream, 0);

}

}

catch { }

}</pre>


<p><br />这里在ClearMappedFile方法里将0序列化到文件里，以达到清除文件中的频道信息的目的。

<br />在主窗口的构造函数中这样写：

<br />

{

Channel channel = Channel.FromCommandLineArgs(System.Environment.GetCommandLineArgs().ToList());

//只允许运行一个实例

if (HasAnotherInstance())

{

if (channel != null) WriteChannelToMappedFile(channel);

App.Current.Shutdown(0);

return;

}

InitializeComponent();

//其他操作

//定时检查内存映射文件，看是否需要更换频道

ThreadPool.QueueUserWorkItem(new WaitCallback(o =&gt;

{

_mappedFile = MemoryMappedFile.CreateOrOpen(_mappedFileName, 10240);

while (true)

{

Thread.Sleep(50);

Channel ch = LoadChannelFromMappedFile();

if (ch != null)

{

ClearMappedFile();

//执行特定操作

}

}

}));

}</pre>

大功告成！

通过检查内存映射文件是否已经存在，可以知道程序的另一个实例是否在运行，再也不用通过查找窗口来检测了。

参考链接：.NET中内存映射文件的详细说明：[http://msdn.microsoft.com/zh-cn/library/dd997372.aspx](http://msdn.microsoft.com/zh-cn/library/dd997372.aspx)
