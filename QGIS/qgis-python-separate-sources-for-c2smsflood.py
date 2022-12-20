
from qgis.core import QgsProject
import os
import processing

print("Start")

sar_list = list()
sar_epsg_list = list()

dem30_list = list()
dem30_epsg_list = list()

# get and check epsg
for layer in QgsProject.instance().mapLayers().values():
    file_ext = os.path.splitext(layer.source())
    epsg = layer.crs().authid()
    
    if(file_ext[1] == '.tif'): # layer names of SAR Image
        sar_epsg_list.append(epsg)
        
    elif (file_ext[1] == '.hgt'): # layer names of DEM
        dem30_epsg_list.append(epsg)

sar_epsg_list = list(set(sar_epsg_list))
dem30_epsg_list = list(set(dem30_epsg_list))

print(sar_epsg_list)
print(dem30_epsg_list)

assert len(sar_epsg_list) == 1, "There are files with different EPSG within tif files"
assert len(dem30_epsg_list) == 1, "There are files with different EPSG within hgt files"

# transfrom .hgt crs
for layer in QgsProject.instance().mapLayers().values():
    file_ext = os.path.splitext(layer.source())
    
    if (file_ext[1] == '.hgt'): # layer names of DEM
        params = {'INPUT':layer.source(),
        'SOURCE_CRS':QgsCoordinateReferenceSystem(dem30_epsg_list[0]),
        'TARGET_CRS':QgsCoordinateReferenceSystem(sar_epsg_list[0]),
        'RESAMPLING':1,
        'NODATA':None,
        'TARGET_RESOLUTION':None,
        'OPTIONS':'',
        'DATA_TYPE':0,
        'TARGET_EXTENT':None,
        'TARGET_EXTENT_CRS':None,
        'MULTITHREADING':False,
        'EXTRA':'',
        'OUTPUT':'TEMPORARY_OUTPUT'}
        result = processing.run("gdal:warpreproject", params)
        rlayer = iface.addRasterLayer(result['OUTPUT'], layer.name() + "_reprojected","gdal")
        QgsProject.instance().removeMapLayers([layer.id()])
print("Done: Generating reprojected DEM")

# Separate DEM(temporary file) and SAR files

for layer in QgsProject.instance().mapLayers().values():
    filename = os.path.basename(layer.source())
    if(filename == 'OUTPUT.tif'): # layer names of temporary file
        dem30_list.append(layer)
        
    else: # layer names of DEM
        sar_list.append(layer)
        
print("Done: separating SAR and DEM layers")
#print(dem30_list)
#print(sar_list)

# Extracting 30m DEM layers from SAR image extent with buffer

mapped_dem10 = list()

for sar in sar_list:
    overlap_id = ""
    overlap_cnt = 0
    temp_dem30 = list()
    
    # clipping
    for dem in dem30_list:
        
        #print(sar.extent())
        #print(dem.extent())
        if(sar.extent().intersects(dem.extent())):
            #print(sar.name())
            #print(dem.name())

            extent = sar.extent()
            xmin = extent.xMinimum()
            xmax = extent.xMaximum()
            ymin = extent.yMinimum()
            ymax = extent.yMaximum()
            xbuf = abs(xmax-xmin) * 0.1
            ybuf = abs(ymax-ymin) * 0.1
            new_extent = "%f,%f,%f,%f" %(xmin-xbuf, xmax+xbuf, 
                                        ymin-ybuf, ymax+ybuf)
            
            params = {
            'INPUT':dem.source(),
            'PROJWIN':new_extent,
            'OVERCRS':False,
            'NODATA':None,
            'OPTIONS':'',
            'DATA_TYPE':0,
            'EXTRA':'',
            'OUTPUT':'TEMPORARY_OUTPUT'}
            result = processing.run("gdal:cliprasterbyextent", params)
            
            if(overlap_cnt == 0):
                overlap_id = ""
            else:
                overlap_id = str(overlap_cnt)
            overlap_cnt = overlap_cnt + 1    
            
            #rlayer = iface.addRasterLayer(result['OUTPUT'],sar.name() + "mapped" + overlap_id,"gdal")
            temp_dem30.append(result['OUTPUT'])
    print(temp_dem30)        
    if len(temp_dem30) == 1 :
        dem30_source = temp_dem30[0]
       
    # merge all intersections
    elif len(temp_dem30) > 1 :
        # merge
        merge_list = [temp for temp in temp_dem30]
            
        params = {
        'INPUT':merge_list,
        'PCT':False,
        'SEPARATE':False,
        'NODATA_INPUT':None,
        'NODATA_OUTPUT':-9999,
        'OPTIONS':'',
        'EXTRA':'',
        'DATA_TYPE':6,
        'OUTPUT':'TEMPORARY_OUTPUT'}
        result = processing.run("gdal:merge", params)
        dem30_source = result['OUTPUT']
        #rlayer = iface.addRasterLayer(result['OUTPUT'], sar.name() + "mapped_merge","gdal")
        
    # resample DEM files as 10m resolution
    
    params = {
    'input':dem30_source,
    'method':1,
    'output':'TEMPORARY_OUTPUT',
    'GRASS_REGION_PARAMETER':None,
    'GRASS_REGION_CELLSIZE_PARAMETER':10,
    'GRASS_RASTER_FORMAT_OPT':'',
    'GRASS_RASTER_FORMAT_META':''}
    
    result = processing.run("grass7:r.resamp.interp", params)

    # clipping without buffer
    params = {
    'INPUT':result['output'],
    'PROJWIN':sar.extent(),
    'OVERCRS':False,
    'NODATA':None,
    'OPTIONS':'',
    'DATA_TYPE':0,
    'EXTRA':'',
    'OUTPUT':'TEMPORARY_OUTPUT'}
    result = processing.run("gdal:cliprasterbyextent", params)
    name = sar.name()
    rlayer = iface.addRasterLayer(result['OUTPUT'],"DEM_" + name[6:],"gdal")
    mapped_dem10.append(rlayer)
            
print('Done: Extracting 10m DEM layers from SAR image extent')

# Save result as a file
dir = "C:\\GMSDL\\C2SMSFLOOD\\data\\DEM\\"
#C:\GMSDL\C2SMSFLOOD\data\DEM
for dem in mapped_dem10:
    file_name = dir + dem.name() + '.hgt'
    print(dem.width(), dem.height())
    file_writer = QgsRasterFileWriter(file_name)
    pipe = QgsRasterPipe()
    provider = dem.dataProvider()
    
    if not pipe.set(provider.clone()):
        print ("Cannot set pipe provider")
        continue

    file_writer.writeRaster(
        pipe,
        provider.xSize(),
        provider.ySize(),
        provider.extent(),
        provider.crs())
        
print('Complete: Saving 10m DEM layers mapped each SAR images')

'''
        #r.fill.stats - treat no-data on the boarder
        params = {
        'input':result['OUTPUT'],
        '-k':True,
        'mode':0,
        '-m':False,
        'distance':3,
        'minimum':None,
        'maximum':None,
        'power':2,
        'cells':8,
        'output':'TEMPORARY_OUTPUT',
        'uncertainty':'TEMPORARY_OUTPUT',
        'GRASS_REGION_PARAMETER':None,
        'GRASS_REGION_CELLSIZE_PARAMETER':0,
        'GRASS_RASTER_FORMAT_OPT':'',
        'GRASS_RASTER_FORMAT_META':''}
        result = processing.run("grass7:r.fill.stats", params)
        rlayer = iface.addRasterLayer(result['output'],"dem10_mapped_" + sar.name() + "_MFI","gdal")
        '''