from osgeo import gdal,ogr
import struct

def extractvalues(pathImage, pathAddresses, fieldName):
    
    src_filename = pathImage
    shp_filename = pathAddresses


    src_ds=gdal.Open(src_filename) 
    gt=src_ds.GetGeoTransform()
    rb=src_ds.GetRasterBand(1)
    # in order to write to a shapefile we need to add 1
    ds=ogr.Open(shp_filename,1)
    lyr=ds.GetLayer()    
    # create a new field >> ogr.OFTReal (Double Precision floating point)
    lyr.CreateField(ogr.FieldDefn(fieldName, ogr.OFTReal))
    for feat in lyr:
        geom = feat.GetGeometryRef()
        mx,my=geom.GetX(), geom.GetY()  #coord in map units

        #Convert from map to pixel coordinates.
        #Only works for geotransforms with no rotation.
        px = int((mx - gt[0]) / gt[1]) #x pixel
        py = int((my - gt[3]) / gt[5]) #y pixel
        lyr.SetFeature(feat)
        intval=rb.ReadAsArray(px,py,1,1)
        print intval[0][0] #intval is a numpy array, length=1 as we only asked for 1 pixel value
        
        feat.SetField(fieldName, float(intval[0][0]))
        lyr.SetFeature(feat)
    

if __name__ == '__main__':
    # extract elevation
    extractvalues(r'C:/Temp/ele.tif',r'C:\gis\p2017\pmnewengland\data\step02.shp', 'elevation')
    # STEP 07-08 >> extract dvhi_1km values
    extractvalues(r'C:/Temp/dvhi.tif',r'C:\gis\p2017\pmnewengland\data\step02.shp', 'dvhi')
    # STEP 09 >> extract dvlo_1km values
    extractvalues(r'C:/Temp/dvlo.tif',r'C:\gis\p2017\pmnewengland\data\step02.shp', 'dvlo')
    # STEP 10 >> extract imp_1km values
    extractvalues(r'C:/Temp/imp.tif',r'C:\gis\p2017\pmnewengland\data\step02.shp', 'imp')