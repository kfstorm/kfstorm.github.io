# 在WPF程序中获取图像的像素

很早以前我就想知道怎样在WPF程序中获取图片和各个像素的信息，当然在网上搜索了一下之后很快就解决了，那就是用WinForm下的System.Drawing.Bitmap类来做处理，虽然这样做也能达到目的，但我总在想WPF不应该不支持这种功能的啊。今天终于让我研究出来了。

System.Windows.Media.Imaging.BitmapSource类有一个CopyPixels方法，并有几个重载方法，这个方法能将图像的像素数据复制到指定的数组里，然后访问数组的内容就能获得像素信息了。要注意的是BitmapSource的Format属性可能不同，也就是说不同的图片可能像素的存放格式不同，所以复制时指定的数组大小可能不同，复制出来后读取像素的方式也不同。

可以将BitmapSource转换为FormatConvertedBitmap类，FormatConvertedBitmap类继承自BitmapSource，所以也具有CopyPixels方法。FormatConvertedBitmap类的构造方法中可以指定转换时采用的PixelFormat，如Rgb24、Bgra32、Gray4、Cmyk32等，想要什么像素存放格式就可以指定相应的PixelFormat，PixelFormats类中有很多定义好的PixelFormat。

下面是一个封装好的类，可以获取任一点的Color，并可计算图片的平均色。

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Threading;

namespace BitmapPixelTest
{
	/// <summary>
	/// 用于获取位图像素的类
	/// </summary>
	public class BitmapPixelHelper
	{
		/// <summary>
		/// 位图宽度
		/// </summary>
		public int Width { get; protected set; }
		/// <summary>
		/// 位图高度
		/// </summary>
		public int Height { get; protected set; }
		/// <summary>
		/// 像素
		/// </summary>
		public Color[][] Pixels { get; protected set; }

		/// <summary>
		/// 根据指定的位图生成BitmapPixelHelper类的新实例。
		/// </summary>
		/// <param name="bitmap">指定的位图</param>
		public BitmapPixelHelper(BitmapSource bitmap)
		{
			FormatConvertedBitmap newBitmap = new FormatConvertedBitmap(bitmap, PixelFormats.Bgra32, BitmapPalettes.WebPaletteTransparent, 0);
			const int bytesPerPixel = 4;
			Height = newBitmap.PixelHeight;
			Width = newBitmap.PixelWidth;
			byte[] data = new byte[Height * Width * bytesPerPixel];
			newBitmap.CopyPixels(data, Width * bytesPerPixel, 0);

			Pixels = new Color[Height][];
			for (int i = 0; i < Height; ++i)
			{
				Pixels[i] = new Color[Width];
				for (int j = 0; j < Width; ++j)
				{
					Pixels[i][j] = Color.FromArgb(
						data[(i * Width + j) * bytesPerPixel + 3],
						data[(i * Width + j) * bytesPerPixel + 2],
						data[(i * Width + j) * bytesPerPixel + 1],
						data[(i * Width + j) * bytesPerPixel + 0]);
				}
			}
		}

		/// <summary>
		/// 获取图片的平均色
		/// </summary>
		public Color GetAverageColor()
		{
			int a = 0, r = 0, g = 0, b = 0;
			for (int i = 0; i < Height; ++i)
			{
				for (int j = 0; j < Width; ++j)
				{
					a += Pixels[i][j].A;
					r += Pixels[i][j].R;
					g += Pixels[i][j].G;
					b += Pixels[i][j].B;
				}
			}
			a = a / Height / Width;
			r = r / Height / Width;
			g = g / Height / Width;
			b = b / Height / Width;
			return Color.FromArgb((byte)a, (byte)r, (byte)g, (byte)b);
		}
	}
}
```

效果如下（选择图片按钮下方为图片，窗口背景为图片的平均色）：

[<img style="background-image: none; border-bottom: 0px; border-left: 0px; padding-left: 0px; padding-right: 0px; display: inline; border-top: 0px; border-right: 0px; padding-top: 0px" title="image38" border="0" alt="image38" src="/attachment/up/blog/images/60e1c5ea7974_134B9/image38_thumb.jpg" width="500" height="333">](/attachment/up/blog/images/60e1c5ea7974_134B9/image38.jpg)

[<img style="background-image: none; border-bottom: 0px; border-left: 0px; padding-left: 0px; padding-right: 0px; display: inline; border-top: 0px; border-right: 0px; padding-top: 0px" title="image39" border="0" alt="image39" src="/attachment/up/blog/images/60e1c5ea7974_134B9/image39_thumb.jpg" width="500" height="333">](/attachment/up/blog/images/60e1c5ea7974_134B9/image39.jpg)

[<img style="background-image: none; border-bottom: 0px; border-left: 0px; padding-left: 0px; padding-right: 0px; display: inline; border-top: 0px; border-right: 0px; padding-top: 0px" title="image40" border="0" alt="image40" src="/attachment/up/blog/images/60e1c5ea7974_134B9/image40_thumb.jpg" width="500" height="333">](/attachment/up/blog/images/60e1c5ea7974_134B9/image40.jpg)

# 评论

发布者 | 时间 | 内容
--- | --- | ---
韩总 | 2012-02-24 11:17:22 | 不错，不错，哈哈哈。。。
