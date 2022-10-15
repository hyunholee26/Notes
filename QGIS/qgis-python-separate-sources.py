
from qgis.core import QgsProject
import os

print("Start")

tif_list = list()
hgt_list = list()

# separate hgt and tiff files

for layer in QgsProject.instance().mapLayers().values():
    file_ext = os.path.splitext(layer.source())
    if(file_ext[1] == '.tif'): # layer names of SAR Image
        tif_list.append(layer)
    elif (file_ext[1] == '.hgt'): # layer names of DEM
        hgt_list.append(layer)
        
print("Done: separating SAR and DEM layers")

import processing

# resample DEM files as 10m resolution

cell_size = 8.983152841195214829e-05

for dem in hgt_list:
    params = {
    'input':dem.source(),
    'method':1,
    'output':'TEMPORARY_OUTPUT',
    'GRASS_REGION_PARAMETER':None,
    'GRASS_REGION_CELLSIZE_PARAMETER':cell_size,
    'GRASS_RASTER_FORMAT_OPT':'',
    'GRASS_RASTER_FORMAT_META':''}
    
    result = processing.run("grass7:r.resamp.interp", params)
    rlayer = iface.addRasterLayer(result['output'],"10m_" + dem.name(),"gdal")

    if rlayer.isValid() == False:
        print("This raster layer is invalid!")
        
print('Done: Resampling to 10m DEM files')

# generate 10m_dem layers list and remove 30m_dem layers

resampled_dem = list()

for layer in QgsProject.instance().mapLayers().values():
    if(layer.name().startswith("10m_")):
        resampled_dem.append(layer)
    
for layer in hgt_list:
    QgsProject.instance().removeMapLayer(layer)

print('Done: Remove 30m DEM layers')

# Extracting 10m DEM layers from SAR image extent

mapped_10m_dem = list()

for sar in tif_list:
    
    overlap_id = ""
    overlap_cnt = 0
    temp_10m_dem = list()
    
    for dem in resampled_dem:
        if(sar.extent().intersects(dem.extent())):
            #print(sar.name())
            #print(dem.name())
            params = {
            'INPUT':dem.source(),
            'PROJWIN':sar.extent(),
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
            
            rlayer = iface.addRasterLayer(result['OUTPUT'],"dem10_mapped_" + sar.name() + overlap_id,"gdal")
            temp_10m_dem.append(rlayer)
            
    if len(temp_10m_dem) == 1 :
        rlayer = temp_10m_dem[0]
        
    elif len(temp_10m_dem) > 1 :
        merge_list = [temp.source() for temp in temp_10m_dem]
            
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

        for temp in temp_10m_dem:
            QgsProject.instance().removeMapLayer(temp)
    
    mapped_10m_dem.append(rlayer)
            
print('Done: Extracting 10m DEM layers from SAR image extent')

# Save result as a file
dir = "C:\\gmsdl\\SRTM_DEM_10m\\"

for dem in mapped_10m_dem:
    file_name = dir + dem.name() + '.hgt'
    #print(file_name)
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
