# .NET下使用全局Shell Hook

今天我解决了一个长期困扰我的问题，那就是如何在.NET程序中使用全局Shell Hook。

豆瓣电台需要响应用户按下键盘上的“播放/暂停”键与“下一首”键，无论豆瓣电台的窗口是否处于活动状态。

响应多媒体指令的最佳方法就是处理[WM_APPCOMMAND消息](http://msdn.microsoft.com/en-us/library/windows/desktop/ms646275.aspx)，但WM_APPCOMMAND消息只在窗口处于活动状态时才会触发，当窗口处于非活动状态时，WM_APPCOMMAND是不会触发的。从某种角度上来说，WM_APPCOMMAND消息不是全局广播的。另一个办法是使用全局Shell Hook，使用[SetWindowsHookEx函数](http://msdn.microsoft.com/ZH-CN/library/windows/desktop/ms644990.aspx)添加一个类型为WH_SHELL的全局钩子，并在[Shell钩子的回调函数](http://msdn.microsoft.com/ZH-CN/library/windows/desktop/ms644991.aspx)中处理wParam参数为HSHELL_APPCOMMAND的消息。一切看起来很美好，不是吗？别急，下面才是重点。豆瓣电台使用C#编写，生成的代码当然为托管代码，而包含全局钩子的代码必须编译为本机DLL，所以单纯使用托管代码是无法安装全局钩子的（见[此文](http://support.microsoft.com/kb/318804)的“在 .NET 框架中不支持全局挂钩”一节）。难道要逼我用C++写个DLL？注册热键的方法也不太好，因为热键有唯一性，可能会出现热键冲突。

虽然说.NET程序号称无法安装全局钩子，但是实际上还是可以安装WH_KEYBOARD_LL和WH_MOUSE_LL类型的全局钩子的，这个并不需要将钩子写到DLL里面。所以可以通过监控键盘输入来知晓用户是否按下了多媒体按键。之前我就是这样干的，具体的代码请看[这里](http://doubanfm.codeplex.com/SourceControl/changeset/view/17477#182754)。这个方法的缺点是什么呢？到现在为止我已经数不清有多少用户反映360安全卫士提示我的豆瓣电台监控键盘输入了……

今天又有人向我反映豆瓣电台监控键盘输入，于是我又Google了一番，终于，看到了[这篇文章](http://blog.csdn.net/kimoli/article/details/1601503)，才发现有[RegisterShellHookWindow](http://msdn.microsoft.com/ZH-CN/library/windows/desktop/ms644989.aspx)这样的函数。简单来说，RegisterShellHookWindow函数的作用就是将一般Shell Hook采用的回调函数改为窗口消息发送给指定的窗口。它的好处是可以在全局范围内使用，也不用写在DLL里。调用RegisterShellHookWindow后，指定的窗口就会收到WM_SHELLHOOKMESSAGE消息（值得注意的是，WM_SHELLHOOKMESSAGE不是一个常数，需要用RegisterWindowMessage(TEXT("SHELLHOOK"))获取），消息的wParam参数即代表hook code，包括HSHELL_APPCOMMAND。当不再需要使用钩子时调用[DeregisterShellHookWindow](http://msdn.microsoft.com/ZH-CN/library/windows/desktop/ms644979.aspx)函数就可以了。

下面是我用C#的实现：

```csharp
using System;
using System.ComponentModel;
using System.Runtime.InteropServices;
using System.Windows;
using System.Windows.Interop;

namespace DoubanFM
{
    public class AppCommand : IDisposable
    {
        public class AppCommandEventArgs : EventArgs
        {
            public Command Command { get; private set; }
            public Device Device { get; private set; }
            public Keys Keys { get; private set; }
            public bool Handled { get; set; }

            public AppCommandEventArgs(Command command, Device device, Keys keys)
            {
                Command = command;
                Device = device;
                Keys = keys;
            }
        }

        public delegate void AppCommndEventhandler(object sender, AppCommandEventArgs e);

        public event AppCommndEventhandler Fire;

        protected virtual void OnFire(AppCommandEventArgs e)
        {
            AppCommndEventhandler handler = Fire;
            if (handler != null) handler(this, e);
        }

        [DllImport("user32.dll", SetLastError = true)]
        private static extern bool RegisterShellHookWindow(IntPtr hWnd);

        [DllImport("user32.dll", SetLastError = true)]
        private static extern bool DeregisterShellHookWindow(IntPtr hWnd);

        [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
        private static extern uint RegisterWindowMessage(string lpString);

        private static int WM_SHELLHOOKMESSAGE;
        private static readonly IntPtr HSHELL_APPCOMMAND = new IntPtr(12);
        private const uint FAPPCOMMAND_MASK = 0xF000;

        private IntPtr hWnd;
        private HwndSource source;
        private bool disposed = false;

        public AppCommand(IntPtr hWnd)
        {
            this.hWnd = hWnd;
        }

        public AppCommand(Window window)
            : this(new WindowInteropHelper(window).EnsureHandle())
        {
        }

        public void Dispose()
        {
            Dispose(true);
            GC.SuppressFinalize(this);
        }

        protected virtual void Dispose(bool disposing)
        {
            if (!disposed)
            {
                if (disposing)
                {
                }

                Stop();
                hWnd = IntPtr.Zero;

                disposed = true;

            }
        }

        ~AppCommand()
        {
            Dispose(false);
        }

        public void Start()
        {
            if (disposed)
            {
                throw new ObjectDisposedException(null);
            }

            if (source == null)
            {
                source = HwndSource.FromHwnd(hWnd);
                if (source == null)
                {
                    throw new InvalidOperationException("hWnd is invalid.");
                }
                source.AddHook(WndProc);
                WM_SHELLHOOKMESSAGE = (int) RegisterWindowMessage("SHELLHOOK");
                if (WM_SHELLHOOKMESSAGE == 0)
                {
                    int error = Marshal.GetLastWin32Error();
                    throw new Win32Exception(error, "Register window message 'SHELLHOOK' failed.");
                }
                if (!RegisterShellHookWindow(hWnd))
                {
                    int error = Marshal.GetLastWin32Error();
                    throw new Win32Exception(error, "Call RegisterShellHookWindow failed.");
                }
            }
        }

        private IntPtr WndProc(IntPtr hwnd, int msg, IntPtr wParam, IntPtr lParam, ref bool handled)
        {
            if (msg == WM_SHELLHOOKMESSAGE && wParam == HSHELL_APPCOMMAND)
            {
                var command = GetAppCommandLParam(lParam);
                var device = GetDeviceLParam(lParam);
                var keys = GetKeyStateLParam(lParam);

                var e = new AppCommandEventArgs(command, device, keys);
                OnFire(e);
                handled = e.Handled;
            }
            return IntPtr.Zero;
        }

        protected static Command GetAppCommandLParam(IntPtr lParam)
        {
            return (Command) ((short) (((ushort) ((((uint) lParam.ToInt64()) >> 16) & 0xffff)) & ~FAPPCOMMAND_MASK));
        }

        protected static Device GetDeviceLParam(IntPtr lParam)
        {
            return (Device) ((ushort) (((ushort) ((((uint) lParam.ToInt64()) >> 16) & 0xffff)) & FAPPCOMMAND_MASK));
        }

        protected static Keys GetKeyStateLParam(IntPtr lParam)
        {
            return (Keys) ((ushort) (((uint) lParam.ToInt64()) & 0xffff));
        }

        public void Stop()
        {
            if (disposed)
            {
                throw new ObjectDisposedException(null);
            }

            if (source != null)
            {
                source.RemoveHook(WndProc);
                if (!source.IsDisposed)
                {
                    if (!DeregisterShellHookWindow(hWnd))
                    {
                        int error = Marshal.GetLastWin32Error();
                        throw new Win32Exception(error, "Call DeregisterShellHookWindow failed.");
                    }
                    source.Dispose();
                }
                source = null;
            }
        }

        public enum Command
        {
            APPCOMMAND_BASS_BOOST = 20,
            APPCOMMAND_BASS_DOWN = 19,
            APPCOMMAND_BASS_UP = 21,
            APPCOMMAND_BROWSER_BACKWARD = 1,
            APPCOMMAND_BROWSER_FAVORITES = 6,
            APPCOMMAND_BROWSER_FORWARD = 2,
            APPCOMMAND_BROWSER_HOME = 7,
            APPCOMMAND_BROWSER_REFRESH = 3,
            APPCOMMAND_BROWSER_SEARCH = 5,
            APPCOMMAND_BROWSER_STOP = 4,
            APPCOMMAND_CLOSE = 31,
            APPCOMMAND_COPY = 36,
            APPCOMMAND_CORRECTION_LIST = 45,
            APPCOMMAND_CUT = 37,
            APPCOMMAND_DICTATE_OR_COMMAND_CONTROL_TOGGLE = 43,
            APPCOMMAND_FIND = 28,
            APPCOMMAND_FORWARD_MAIL = 40,
            APPCOMMAND_HELP = 27,
            APPCOMMAND_LAUNCH_APP1 = 17,
            APPCOMMAND_LAUNCH_APP2 = 18,
            APPCOMMAND_LAUNCH_MAIL = 15,
            APPCOMMAND_LAUNCH_MEDIA_SELECT = 16,
            APPCOMMAND_MEDIA_CHANNEL_DOWN = 52,
            APPCOMMAND_MEDIA_CHANNEL_UP = 51,
            APPCOMMAND_MEDIA_FAST_FORWARD = 49,
            APPCOMMAND_MEDIA_NEXTTRACK = 11,
            APPCOMMAND_MEDIA_PAUSE = 47,
            APPCOMMAND_MEDIA_PLAY = 46,
            APPCOMMAND_MEDIA_PLAY_PAUSE = 14,
            APPCOMMAND_MEDIA_PREVIOUSTRACK = 12,
            APPCOMMAND_MEDIA_RECORD = 48,
            APPCOMMAND_MEDIA_REWIND = 50,
            APPCOMMAND_MEDIA_STOP = 13,
            APPCOMMAND_MIC_ON_OFF_TOGGLE = 44,
            APPCOMMAND_MICROPHONE_VOLUME_DOWN = 25,
            APPCOMMAND_MICROPHONE_VOLUME_MUTE = 24,
            APPCOMMAND_MICROPHONE_VOLUME_UP = 26,
            APPCOMMAND_NEW = 29,
            APPCOMMAND_OPEN = 30,
            APPCOMMAND_PASTE = 38,
            APPCOMMAND_PRINT = 33,
            APPCOMMAND_REDO = 35,
            APPCOMMAND_REPLY_TO_MAIL = 39,
            APPCOMMAND_SAVE = 32,
            APPCOMMAND_SEND_MAIL = 41,
            APPCOMMAND_SPELL_CHECK = 42,
            APPCOMMAND_TREBLE_DOWN = 22,
            APPCOMMAND_TREBLE_UP = 23,
            APPCOMMAND_UNDO = 34,
            APPCOMMAND_VOLUME_DOWN = 9,
            APPCOMMAND_VOLUME_MUTE = 8,
            APPCOMMAND_VOLUME_UP = 10
        }

        public enum Device
        {
            FAPPCOMMAND_KEY = 0,
            FAPPCOMMAND_MOUSE = 0x8000,
            FAPPCOMMAND_OEM = 0x1000
        }

        [Flags]
        public enum Keys
        {
            MK_CONTROL = 0x0008,
            MK_LBUTTON = 0x0001,
            MK_MBUTTON = 0x0010,
            MK_RBUTTON = 0x0002,
            MK_SHIFT = 0x0004,
            MK_XBUTTON1 = 0x0020,
            MK_XBUTTON2 = 0x0040
        }
    }
}
```

Update at 2013.01.04: 修复了上面贴的代码中在64位系统下可能算术溢出的bug。

# 评论

发布者 | 时间 | 内容
--- | --- | ---
K.F.Storm | 2014-06-17 22:38:24 | Windows Azure
tewuapple | 2014-06-16 07:54:11 | 楼主用的是什么主机搭建的wordpress？
jiong-lin | 2013-08-01 13:12:26 | 哥们儿，加油。
wintrue | 2013-02-19 13:53:37 | 强烈支持楼主！！！！！！
K.F.Storm | 2013-02-02 14:14:20 | hook不会提示的。注册快捷键也可以，不过快捷键是独占的，如果同时开启了多个播放器，可能会有意料之外的结果。
vincent | 2013-02-01 09:39:06 | 注册全局快捷键不就可以了？用得着Hook？如果win7下UAC没关的话，Hook会提示的，我觉得不如注册全局快捷键 API- RegisterHotKey
Zasz | 2013-01-30 20:32:30 | 啊，似乎是因为我用了autohotkey把常用那几个键映射成了豆瓣FM官方的那几个，所以怎么也设不了……<br/>捂脸退下了，thx……
K.F.Storm | 2013-01-30 19:41:11 | 你可以用Ctrl+Shift+....，Ctrl+Alt+....等
Zasz | 2013-01-30 00:32:04 | 吓我一跳，没有注册也有自定义头像……是gravatar.com识别邮箱吗？
Zasz | 2013-01-30 00:29:13 | 方便的话，拜托加上三个键的全局快捷键~两个的话，太容易和复制粘贴那一群冲突了……
licdream | 2013-01-14 11:55:48 | 努力学习，很佩服和欣赏楼主！
南 | 2013-01-06 17:23:29 | 支持！！！
lxwlxc | 2013-01-03 21:43:58 | 很喜欢你的杰作，即使看不懂，我也默默的支持
小心 | 2013-01-03 09:18:16 | 祝软件越来越完美
TianLi520 | 2013-01-03 00:14:50 | 看不懂，不过只要好用就支持
