import os
from osgeo import gdal

# os.environ['PROJ_LIB'] = r'E:\ProgramData\Anaconda3\envs\qt39exe\Lib\site-packages\osgeo\data\proj'
# 影像分块
def split(tifDir, outPath, size):
    """

    Args:
        tifDir:分块影像(tif)所在文件夹，不能有中文
        outPath:输出的文件夹，不能有中文，如果文件夹不存在则会被创建
        size:定义切图的大小（矩形框）

    Returns:是否成功

    """
    if not os.path.exists(outPath):
        os.makedirs(outPath)
    tifs = [i for i in os.listdir(tifDir) if i.endswith(".tif")]
    print("有 %s 个tif文件" % len(tifs))
    print("tifs", tifs)
    tiflist1 = []
    for i in tifs:
        tiflist1.append(i[:-4])
    tiflist = list(set(tiflist1))
    tiflist.sort(key=tiflist1.index)
    print("有 %s 个文件" % len(tiflist))
    print("datelist", tiflist)
    # 定义切图的大小（矩形框）
    # len(datelist)

    for img in range(len(tifs)):
        print("正在分割：", tifs[img])
        in_ds = gdal.Open(tifDir + "\\" + tifs[img])  # 读取要切的原图

        width = in_ds.RasterXSize  # 获取数据宽度
        height = in_ds.RasterYSize  # 获取数据高度
        outbandsize = in_ds.RasterCount  # 获取数据波段数
        im_geotrans = in_ds.GetGeoTransform()  # 获取仿射矩阵信息
        im_proj = in_ds.GetProjection()  # 获取投影信息
        datatype = in_ds.GetRasterBand(1).DataType
        im_data = in_ds.ReadAsArray()  # 获取数据

        col_num = int(width / size)  # 宽度可以分成几块
        row_num = int(height / size)  # 高度可以分成几块
        if (width % size != 0):
            col_num += 1
        if (height % size != 0):
            row_num += 1

        # print("row_num:%d   col_num:%d" % (row_num, col_num))
        for i in range(row_num):  # 从高度下手！！！ 可以分成几块！
            for j in range(col_num):
                offset_x = i * size
                offset_y = j * size
                ## 从每个波段中切需要的矩形框内的数据(注意读取的矩形框不能超过原图大小)
                b_ysize = min(width - offset_y, size)
                b_xsize = min(height - offset_x, size)
                out_allband = im_data[:, offset_x:offset_x + b_xsize, offset_y:offset_y + b_ysize]
                # print(out_allband.shape)

                # 获取Tif的驱动，为创建切出来的图文件做准备
                gtif_driver = gdal.GetDriverByName("GTiff")
                file = outPath + "\\" + tifs[img][:-4] + "-" + str(offset_x).zfill(10) + "-" + str(offset_y).zfill(
                    10) + ".tif"

                # 创建切出来的要存的文件
                out_ds = gtif_driver.Create(file, b_ysize, b_xsize, outbandsize, datatype)
                # print("create new tif file succeed")

                # 获取原图的原点坐标信息
                ori_transform = in_ds.GetGeoTransform()
                # if ori_transform:
                # print(ori_transform)
                # print("Origin = ({}, {})".format(ori_transform[0], ori_transform[3]))
                # print("Pixel Size = ({}, {})".format(ori_transform[1], ori_transform[5]))

                # 读取原图仿射变换参数值
                top_left_x = ori_transform[0]  # 左上角x坐标
                w_e_pixel_resolution = ori_transform[1]  # 东西方向像素分辨率
                top_left_y = ori_transform[3]  # 左上角y坐标
                n_s_pixel_resolution = ori_transform[5]  # 南北方向像素分辨率

                # 根据反射变换参数计算新图的原点坐标
                top_left_x = top_left_x + offset_y * w_e_pixel_resolution
                top_left_y = top_left_y + offset_x * n_s_pixel_resolution

                # 将计算后的值组装为一个元组，以方便设置
                dst_transform = (
                    top_left_x, ori_transform[1], ori_transform[2], top_left_y, ori_transform[4], ori_transform[5])

                # 设置裁剪出来图的原点坐标
                out_ds.SetGeoTransform(dst_transform)

                # 设置SRS属性（投影信息）
                out_ds.SetProjection(in_ds.GetProjection())

                # 写入目标文件
                for ii in range(outbandsize):
                    out_ds.GetRasterBand(ii + 1).WriteArray(out_allband[ii])

                # 将缓存写入磁盘
                out_ds.FlushCache()
                # print("FlushCache succeed")
                del out_ds
            # print(i/row_num)
            # self.progressBar.setValue(int(100*(i+1)/row_num))
            # self._signal.emit(int(100*(i+1)/row_num))  # 注意这里与_signal = pyqtSignal(str)中的类型相同
            # self._signal.emit(int(100 * (img / 3 + (i + 1) / (row_num * 3))))  # 注意这里与_signal = pyqtSignal(str)中的类型相同

    return True
