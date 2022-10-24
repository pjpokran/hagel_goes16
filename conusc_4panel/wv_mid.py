band="09"
filechar=['AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM',
          'AN','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX','AY','AZ',
          'BA','BB','BC','BD','BE','BF','BG','BH','BI','BJ','BK','BL','BM',
          'BN','BO','BP','BQ','BR','BS','BT','BU','BV','BW','BX','BY','BZ']


#f = netCDF4.Dataset("/weather/data/goes16/TIRC/"+band+"/"+dt+"_PAA.nc")
f = netCDF4.Dataset("/weather/data/goes16/"+prod_id+"/"+band+"/"+dt+"_PAA.nc")
a = np.zeros(shape=(f.product_rows,f.product_columns))
xa= np.zeros(shape=(f.product_columns))
ya= np.zeros(shape=(f.product_rows))


print(f)

data_var = f.variables['Sectorized_CMI']
a[0:f.product_tile_height,0:f.product_tile_width] = data_var[:]
#data_var2 = g.variables['Sectorized_CMI']

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
#
#print(np.average(a))
#if np.average(a) > 0.7:
#    quit()


proj_var = f.variables[data_var.grid_mapping]

import cartopy.crs as ccrs

# Create a Globe specifying a spherical earth with the correct radius
globe = ccrs.Globe(ellipse='sphere', semimajor_axis=proj_var.semi_major,
                   semiminor_axis=proj_var.semi_minor)

proj = ccrs.LambertConformal(central_longitude=proj_var.longitude_of_central_meridian,
                             central_latitude=proj_var.latitude_of_projection_origin,
                             standard_parallels=[proj_var.standard_parallel],
                             globe=globe)


image_rows=f.product_rows
image_columns=f.product_columns
wi_image_crop_top=365
wi_image_crop_bottom=-1750
wi_image_crop_left=1290
wi_image_crop_right=-1220

wi_image_size_y=(image_rows+wi_image_crop_bottom-wi_image_crop_top)
wi_image_size_x=(image_columns+wi_image_crop_right-wi_image_crop_left)

print("wi image size")
print(wi_image_size_x, wi_image_size_y)

#wi_image_size_x=float(wi_image_size_x)/120.
#wi_image_size_y=float(wi_image_size_y)/120.
wi_image_size_x=float(wi_image_size_x)/40.
wi_image_size_y=float(wi_image_size_y)/40.

mw_image_crop_top=295
mw_image_crop_bottom=-1430
mw_image_crop_left=875
mw_image_crop_right=-1075

mw_image_size_y=(image_rows+mw_image_crop_bottom-mw_image_crop_top)
mw_image_size_x=(image_columns+mw_image_crop_right-mw_image_crop_left)

print("mw image size")
print(mw_image_size_x, mw_image_size_y)

mw_image_size_x=float(mw_image_size_x)/75.
mw_image_size_y=float(mw_image_size_y)/75.

ne_image_crop_top=95
ne_image_crop_bottom=-1230
ne_image_crop_left=1475
ne_image_crop_right=-75

ne_image_size_y=(image_rows+ne_image_crop_bottom-ne_image_crop_top)
ne_image_size_x=(image_columns+ne_image_crop_right-ne_image_crop_left)

print("ne image size")
print(ne_image_size_x, ne_image_size_y)

ne_image_size_x=float(ne_image_size_x)/100.
ne_image_size_y=float(ne_image_size_y)/100.

conus_image_crop_top=220
conus_image_crop_bottom=-730
conus_image_crop_left=50
conus_image_crop_right=-225

conus_image_size_y=(image_rows+conus_image_crop_bottom-conus_image_crop_top)
conus_image_size_x=(image_columns+conus_image_crop_right-conus_image_crop_left)

print("conus image size")
print(conus_image_size_x, conus_image_size_y)

conus_image_size_x=float(conus_image_size_x)/150.
conus_image_size_y=float(conus_image_size_y)/150.

# Create a new figure with size 10" by 10"
fig = plt.figure(figsize=(wi_image_size_x,wi_image_size_y),dpi=80.)
fig2 = plt.figure(figsize=(mw_image_size_x,mw_image_size_y),dpi=160.)
fig3 = plt.figure(figsize=(conus_image_size_x,conus_image_size_y),dpi=160.)
fig4 = plt.figure(figsize=(ne_image_size_x,ne_image_size_y),dpi=160.)
#fig2 = plt.figure(figsize=(image_columns/200.,image_rows/200.))
#fig9 = plt.figure(figsize=(image_columns/80.,image_rows/80.))

# Put a single axes on this figure; set the projection for the axes to be our
# Lambert conformal projection
ax = fig.add_subplot(2, 2, 2, projection=proj)
ax2 = fig2.add_subplot(2, 2, 2, projection=proj)
ax3 = fig3.add_subplot(2, 2, 2, projection=proj)
ax4 = fig4.add_subplot(2, 2, 2, projection=proj)
#ax9 = fig9.add_subplot(1, 1, 1, projection=proj)


cdict = {'red': ((0.0, 1.0, 1.0),
                 (0.29, 1.00, 1.00),
                 (0.61, 0.0, 0.0),
                 (1.0, 0.0, 0.0)),
         'green': ((0.0, 1.0, 1.0),
                 (0.29, 1.00, 1.00),
                 (0.61, 0.0, 0.0),
                 (1.0, 0.0, 0.0)),
         'blue': ((0.0, 1.0, 1.0),
                 (0.29, 1.00, 1.00),
                 (0.61, 0.0, 0.0),
                 (1.0, 0.0, 0.0))}

import matplotlib as mpl

my_cmap = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,2048)

cdict2 = {'red': ((0.0, 0.0, 0.0),
                 (0.208, 0.0, 0.0),
                 (0.379, 1.0, 1.0),
                 (0.483, 0.0, 0.0),
                 (0.572, 1.0, 1.0),
                 (0.667, 0.0, 0.0),
                 (1.0, 0.0, 0.0)),
         'green': ((0.0, 1.0, 1.0),
                   (0.208, .423, .423),
                   (0.379, 1.0, 1.0),
                   (0.483, 0.0, 0.0),
                   (0.572, 1.0, 1.0),
                   (0.667, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),
         'blue': ((0.0, 1.0, 1.0),
                  (0.208, 0.0, 0.0),
                  (0.379, 1.0, 1.0),
                  (0.483,0.651, 0.651),
                  (0.572, 0.0, 0.0),
                  (0.667, 0.0, 0.0),
                  (1.0, 0.0, 0.0))}

my_cmap2 = mpl.colors.LinearSegmentedColormap('my_colormap2',cdict2,2048)

# Plot the data using a simple greyscale colormap (with black for low values);
# set the colormap to extend over a range of values from 140 to 255.
# Note, we save the image returned by imshow for later...
#im = ax.imshow(data_var[:], extent=(x[0], x[-1], y[0], y[-1]), origin='upper',
#               cmap='Greys_r', norm=plt.Normalize(0, 256))
#im = ax.imshow(data_var[:], extent=(x[0], x[-1], y[0], y[-1]), origin='upper',
#im = ax.imshow(a[:], extent=(xa[0], xa[-1], ya[-1], ya[0]), origin='upper',
#               cmap='Greys_r')
#im = ax.imshow(a[250:-3000,2000:-2000], extent=(xa[2000],xa[-2000],ya[-3000],ya[250]), origin='upper',cmap='Greys_r')
#im = ax.imshow(a[250:-3500,2500:-2200], extent=(xa[2500],xa[-2200],ya[-3500],ya[250]), origin='upper',cmap='Greys_r')
#im = ax.imshow(data_var[:], extent=(x[0], x[-1], y[0], y[-1]), origin='upper')
#im = ax2.imshow(a[:], extent=(xa[1],xa[-1],ya[-1],ya[1]), origin='upper', cmap='Greys_r')

im = ax.imshow(a[wi_image_crop_top:wi_image_crop_bottom,wi_image_crop_left:wi_image_crop_right], extent=(xa[wi_image_crop_left],xa[wi_image_crop_right],ya[wi_image_crop_bottom],ya[wi_image_crop_top]), origin='upper',cmap=my_cmap2, vmin=162., vmax=330.0)
im = ax2.imshow(a[mw_image_crop_top:mw_image_crop_bottom,mw_image_crop_left:mw_image_crop_right], extent=(xa[mw_image_crop_left],xa[mw_image_crop_right],ya[mw_image_crop_bottom],ya[mw_image_crop_top]), origin='upper',cmap=my_cmap2, vmin=162., vmax=330.0)
im = ax3.imshow(a[conus_image_crop_top:conus_image_crop_bottom,conus_image_crop_left:conus_image_crop_right], extent=(xa[conus_image_crop_left],xa[conus_image_crop_right],ya[conus_image_crop_bottom],ya[conus_image_crop_top]), origin='upper',cmap=my_cmap2, vmin=162., vmax=330.0)
im = ax4.imshow(a[ne_image_crop_top:ne_image_crop_bottom,ne_image_crop_left:ne_image_crop_right], extent=(xa[ne_image_crop_left],xa[ne_image_crop_right],ya[ne_image_crop_bottom],ya[ne_image_crop_top]), origin='upper',cmap=my_cmap2, vmin=162., vmax=330.0)
#im = ax9.imshow(a[:], extent=(xa[1],xa[-1],ya[-1],ya[1]), origin='upper', cmap=my_cmap2, vmin=162., vmax=330.0)

import cartopy.feature as cfeat

# Add country borders with a thick line.
ax.add_feature(cfeat.BORDERS, linewidth='1', edgecolor='green')
ax2.add_feature(cfeat.BORDERS, linewidth='1', edgecolor='green')
ax3.add_feature(cfeat.BORDERS, linewidth='1', edgecolor='green')
ax4.add_feature(cfeat.BORDERS, linewidth='1', edgecolor='green')
#ax9.add_feature(cfeat.BORDERS, linewidth='1', edgecolor='green')

# Set up a feature for the state/province lines. Tell cartopy not to fill in the polygons
state_boundaries = cfeat.NaturalEarthFeature(category='cultural',
                                             name='admin_1_states_provinces_lakes',
                                             scale='50m', facecolor='none', edgecolor='red')

# Add the feature with dotted lines, denoted by ':'
ax.add_feature(state_boundaries, linestyle=':')
ax2.add_feature(state_boundaries, linestyle=':')
ax3.add_feature(state_boundaries, linestyle=':')
ax4.add_feature(state_boundaries, linestyle=':')
#ax9.add_feature(state_boundaries, linestyle=':')

# axes for wi
cbaxes1 = fig.add_axes([0.135,0.12,0.755,0.02])
cbar1 = fig.colorbar(im, cax=cbaxes1, orientation='horizontal')
font_size = 14
#cbar1.set_label('Brightness Temperature (K)',size=18)
cbar1.ax.tick_params(labelsize=font_size)
cbar1.ax.xaxis.set_ticks_position('top')
cbar1.ax.xaxis.set_label_position('top')

# axes for mw
cbaxes2 = fig2.add_axes([0.135,0.12,0.755,0.02])
cbar2 = fig2.colorbar(im, cax=cbaxes2, orientation='horizontal')
font_size = 14
#cbar2.set_label('Brightness Temperature (K)',size=18)
cbar2.ax.tick_params(labelsize=font_size)
cbar2.ax.xaxis.set_ticks_position('top')
cbar2.ax.xaxis.set_label_position('top')

# axes for conus
cbaxes3 = fig3.add_axes([0.135,0.12,0.755,0.02])
cbar3 = fig3.colorbar(im, cax=cbaxes3, orientation='horizontal')
font_size = 14
#cbar3.set_label('Brightness Temperature (K)',size=18)
cbar3.ax.tick_params(labelsize=font_size)
cbar3.ax.xaxis.set_ticks_position('top')
cbar3.ax.xaxis.set_label_position('top')

# axes for ne
cbaxes4 = fig4.add_axes([0.135,0.12,0.755,0.02])
cbar4 = fig4.colorbar(im, cax=cbaxes4, orientation='horizontal')
font_size = 14
#cbar4.set_label('Brightness Temperature (K)',size=18)
cbar4.ax.tick_params(labelsize=font_size)
cbar4.ax.xaxis.set_ticks_position('top')
cbar4.ax.xaxis.set_label_position('top')

## axes for full
#cbaxes9 = fig9.add_axes([0.135,0.15,0.755,0.02])
#cbar9 = fig9.colorbar(im, cax=cbaxes9, orientation='horizontal')
#font_size = 18
##cbar9.set_label('Brightness Temperature (K)',size=18)
#cbar9.ax.tick_params(labelsize=font_size)
#cbar9.ax.xaxis.set_ticks_position('top')
#cbar9.ax.xaxis.set_label_position('top')
