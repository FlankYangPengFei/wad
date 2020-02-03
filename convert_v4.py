import arcpy
from arcpy.sa import *  #引入模块
outLoc = "E:/seaice/osisaf_conc/testtif_type"  #输出路径
inNetCDF = "E:/seaice/osisaf_conc/type/ice_type_nh_polstere-100_multi_201908021200.nc"  #输入路径
variable = 'ice_type'  #此处是.nc数据中的变量名（海冰类型）
x_dimension = "xc"
y_dimension = "yc"
band_dimension = ""
valueSelectionMethod = "BY_VALUE" #以上五个变量为第一个函数会用到的变量，提前定义好
nc_FP = arcpy.NetCDFFileProperties(inNetCDF)  #读取netCDF文件
nc_Dim = nc_FP.getDimensions()  #获取维度信息，返回一个维度列表 ['lon','lat','time']
	
'''
在一个.nc文件中有400个时间，每天有一个海冰密集度数据，所以导出有400个tiff图像
为了给导出图像方便命名，要使用 dimension_values ，每一个输出的变量值都是使用该维度的值
'''
	
for dimension in nc_Dim:
    
    if dimension == "time":  
         top = nc_FP.getDimensionSize(dimension)  #获取维度的大小
         for i in range(0, 1):
            dimension_values = nc_FP.getDimensionValue(dimension, i)
            nowFile =str(dimension_values[0:7])
            nowFile = nowFile.translate(None, '/')
            print('doing....'+str(i+1))
            dv1 = ["time", dimension_values]
            dimension_values = [dv1]
            #nowFile=str(i+1)  
            outpath= outLoc+"\\"+nowFile + ".tif"
            
            arcpy.MakeNetCDFRasterLayer_md(inNetCDF,variable,x_dimension,y_dimension,nowFile,band_dimension, dimension_values, valueSelectionMethod)
            arcpy.CopyRaster_management(nowFile, outpath, "", "", "", "NONE", "NONE", "")
            
print('success')