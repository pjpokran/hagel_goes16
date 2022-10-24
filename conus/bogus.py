#!/home/poker/miniconda3/bin/python
import netCDF4
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
#import os.rename
#import os.remove
import shutil
import sys

import cartopy
ccrs = cartopy.crs

band="02"
filechar=['AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM',
          'AN','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX','AY','AZ',
          'BA','BB','BC','BD','BE','BF','BG','BH','BI','BJ','BK','BL','BM',
          'BN','BO','BP','BQ','BR','BS','BT','BU','BV','BW','BX','BY','BZ',
          'CA','CB','CC','CD','CE','CF','CG','CH','CI','CJ','CK','CL','CM',
          'CN','CO','CP','CQ','CR','CS','CT','CU','CV','CW','CX','CY','CZ',
          'DA','DB','DC','DD','DE','DF','DG','DH','DI','DJ','DK','DL','DM',
          'DN','DO','DP','DQ','DR','DS','DT','DU','DV','DW','DX','DY','DZ',
          'EA','EB','EC','ED','EE','EF','EG','EH','EI','EJ','EK','EL','EM',
          'EN','EO','EP','EQ','ER','ES','ET','EU','EV','EW','EX','EY','EZ']

#print(filechar[1])

prod_id = "TIRC"
#dt="201703051957"
dt = sys.argv[1]

#f = netCDF4.Dataset("/weather/data/goes16/TIRC/"+band+"/"+dt+"_PAA.nc")
f = netCDF4.Dataset("/weather/data/goes16/"+prod_id+"/"+band+"/"+dt+"_PAA.nc")
a = np.zeros(shape=(f.product_rows,f.product_columns))
xa= np.zeros(shape=(f.product_columns))
ya= np.zeros(shape=(f.product_rows))


print(f)

data_var = f.variables['Sectorized_CMI']
a[0:f.product_tile_height,0:f.product_tile_width] = data_var[:]

print(data_var)

x = f.variables['x'][:]
y = f.variables['y'][:]
xa[f.tile_column_offset:f.tile_column_offset+f.product_tile_width] = x[:]
ya[f.tile_row_offset:f.tile_row_offset+f.product_tile_height] = y[:]

if f.number_product_tiles > 1:
# this goes from 1 to number of tiles - 1
    for i in range(1,f.number_product_tiles):
#    print(filechar[i])
        if os.path.isfile("/weather/data/goes16/TIRC/"+band+"/"+dt+"_P"+filechar[i]+".nc"):
            g = netCDF4.Dataset("/weather/data/goes16/TIRC/"+band+"/"+dt+"_P"+filechar[i]+".nc")
#        print(g)
            data_var2 = g.variables['Sectorized_CMI']
            a[g.tile_row_offset:g.tile_row_offset+g.product_tile_height,g.tile_column_offset:g.tile_column_offset+g.product_tile_width]=data_var2[:]
            x = g.variables['x'][:]
            y = g.variables['y'][:]
            xa[g.tile_column_offset:g.tile_column_offset+g.product_tile_width] = x[:]
            ya[g.tile_row_offset:g.tile_row_offset+g.product_tile_height] = y[:]
            g.close


#a[g.tile_column_offset:g.tile_column_offset+g.product_tile_width,g.tile_row_offset:g.tile_row_offset+g.product_tile_height]=data_var[:]
    a[g.tile_row_offset:g.tile_row_offset+g.product_tile_height,g.tile_column_offset:g.tile_column_offset+g.product_tile_width]=data_var2[:]
#print(a)

# swap zeros for ones
a[a==0.] = 1.

print(np.average(a))
if np.average(a) > 0.7:
    quit()


proj_var = f.variables[data_var.grid_mapping]
globe = ccrs.Globe(ellipse='sphere', semimajor_axis=proj_var.semi_major,
                   semiminor_axis=proj_var.semi_minor)

proj = ccrs.LambertConformal(central_longitude=proj_var.longitude_of_central_meridian,
                             central_latitude=proj_var.latitude_of_projection_origin,
                             standard_parallels=[proj_var.standard_parallel],
                             globe=globe)


image_rows=f.product_rows
image_columns=f.product_columns


# Fullres Southern WI sector

swi_image_crop_top=1900
swi_image_crop_bottom=-6400
swi_image_crop_left=5860
swi_image_crop_right=-5280

swi_image_size_y=(image_rows+swi_image_crop_bottom-swi_image_crop_top)
swi_image_size_x=(image_columns+swi_image_crop_right-swi_image_crop_left)

swi_image_size_x=float(swi_image_size_x)/65.
swi_image_size_y=float(swi_image_size_y)/65.

#fig = plt.figure(figsize=(10, 8))
fig = plt.figure(figsize=(swi_image_size_x,swi_image_size_y),dpi=83.)
#proj = ccrs.LambertConformal(central_latitude=40,
#                             central_longitude=-105)
#proj = ccrs.PlateCarree()


#ax = fig.add_subplot(1, 1, 1, projection=proj)
ax = fig.add_subplot(1, 1, 1, projection=proj)


# Open counties shapefile and plot geometry
counties = cartopy.io.shapereader.Reader('/home/poker/resources/counties.shp')
#ax.add_geometries(counties.geometries(), ccrs.PlateCarree(),
#                  edgecolor='grey', facecolor='None')
ax.add_geometries(counties.geometries(), ccrs.PlateCarree(),
                  edgecolor='grey', facecolor='None')

# Find Boulder county and plot
boulder = [county.geometry for county in counties.records()
           if county.attributes['NAME'] == 'Boulder']
ax.add_geometries(boulder, ccrs.PlateCarree(),
                  edgecolor='blue', facecolor='lightblue')

state_borders = cartopy.feature.NaturalEarthFeature(
    category='cultural', name='admin_1_states_provinces_lakes',
    scale='50m', facecolor='none') 

# Re-use state borders from above
ax.add_feature(state_borders, edgecolor='black', linewidth=2)

# Add topo
#im = plt.imread('/home/poker/resources/colorado_blue_marble.jpg')
#ax.imshow(im, interpolation='None', extent=(-110, -101, 36, 42),
#          transform=ccrs.PlateCarree())

# Set limits in lat/lon space
#ax.set_extent([-110, -101, 36, 42])

fig.savefig('/whirlwind/goes16/test/t.jpg', bbox_inches='tight')
