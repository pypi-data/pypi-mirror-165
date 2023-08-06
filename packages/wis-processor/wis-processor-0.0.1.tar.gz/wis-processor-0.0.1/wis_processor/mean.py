#!/usr/bin/env python
# coding: utf-8

'''
该模块用于计算流域平均

- `mean_over_basin` - 计算流域平均

'''


import geopandas as gpd
from shapely.geometry import Point,Polygon,shape


def mean_over_basin(basin,basin_id,dataset,data_name,lon='lon',lat='lat',time='time',time_index=0):
    '''
    计算流域平均
    
    Todo: 
        - 根据grid数据生成网格
        - 网格与流域相交
        - 以流域为单位计算流域内加权值


    Args:
        basin (GeoDataframe): 必选，流域的矢量数据，通过geopandas读取
        basin_id (str): 必选，表示流域编号的字段名称
        dataset (Dataset): 必选，表示grid数据集，通过xarray读取
        data_name (str): 必选，表示grid数据集中需要参与计算的变量名称
        lon (bool): 可选，grid数据集中经度坐标名称
        lat (str): 可选，grid数据集中纬度坐标名称
        time (str): 可选，grid数据集中时间坐标名称
        time_index (int): 可选，grid数据集中的时间序列
    
    Returns
        data (Dataframe): 流域编号和对应的平均值

    '''

    grid=grid_to_gdf(dataset,data_name,lon,lat,time,time_index)
    
    intersects=gpd.overlay(grid,basin,how='intersection')
    intersects=intersects.to_crs(epsg=3857)
    intersects['Area']=intersects.area
    intersects=intersects.to_crs(epsg=4326)

    mean_over_basin=intersects.groupby(basin_id).apply(wavg,data_name,'Area')

    return mean_over_basin
    

def wavg(group,avg_name,weight_name):
    d=group[avg_name]
    w=group[weight_name]
    try:
        return (d*w).sum()/w.sum()
    except ZeroDivisionError:
        return d.mean()


def grid_to_gdf(dataset,data_name,lon='lon',lat='lat',time='time',time_index=0):

    lons=dataset[lon].values
    lats=dataset[lat].values
    delta=lons[1]-lons[0]
    
    geometry=[]
    values=[]
    HBlons=[]
    HBlats=[]

    delta_lon=lons.size
    delta_lat=lats.size

    for i in range(delta_lon):
        for j in range(delta_lat):
            HBLON=lons[i]
            HBLAT=lats[j]

            HBlons.append(HBLON)
            HBlats.append(HBLAT)
            
            geometry.append(Polygon([
                (HBLON-delta/2,HBLAT+delta/2),
                (HBLON+delta/2,HBLAT+delta/2),
                (HBLON+delta/2,HBLAT-delta/2),
                (HBLON-delta/2,HBLAT-delta/2)
            ]))

            values.append(float(dataset[data_name].isel(lon=i,lat=j,time=time_index).data))

    data = gpd.GeoDataFrame(crs='EPSG:4326',geometry=geometry)
    data['HBlon']=HBlons
    data['HBlat']=HBlats
    data[data_name]=values
    # data['geometry']=geometry

    return data