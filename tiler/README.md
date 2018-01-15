# Maptiles from GeoTiff

* This script creates white tiles from a GeoTiff using Floodfill in a height range with custom steps and zoom levels.
* MapTiler Pro and GDAL must be installed and set in the PATH variable in order for this script to execute.
* Executing this script might take several hours depending on zoom levels.

## General Usage (all parameters are mandatory, height in metres, output directory must be empty):

* tiler.py calc inputfile outputdirectory min_height max_height step min_zoom max_zoom

## Usage with docker-compose

* Download DEM Data from copernicus: https://land.copernicus.eu/pan-european/satellite-derived-products/eu-dem/eu-dem-v1.1?tab=mapview
  * only select your area of interest
* unzip the zip (inside the other zip)
* move the TIF to `data`
  * If you need to use multiple tif, either joine them to one big tiff, or alternatively use a `.vrt` file and use that one in the commands below.
* Download a Shapefile with the area (ie. Country) and rename it to `area.shp` (all files!) and move them to the data directory
* Example area.shp is Switzerland (from: https://opendata.swiss/en/dataset/swissboundaries3d-landesgrenzen1/resource/4aa8df61-7513-4b28-aacb-bb0e3632d8dd)

* Cut the tif along the boundary:

```bash
gdalwarp -cutline area.shp -crop_to_cutline -srcnodata 0 <infile.tif> <outfile.tif>
# eg. using eu_dem_v11_E40N20.TIF: gdalwarp -cutline area.shp -crop_to_cutline -srcnodata 0 eu_dem_v11_E40N20.TIF Switzerland.TIF
```
