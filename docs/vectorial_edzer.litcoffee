

## Reading and writing
Reading datasets from an external “data source” (file, web service, or even string) is done using st_read:

```{r}
library(sf)
(file <- system.file("gpkg/nc.gpkg", package = "sf"))
# [1] "/home/edzer/R/x86_64-pc-linux-gnu-library/4.4/sf/gpkg/nc.gpkg"
nc <- st_read(file)
# Reading layer `nc.gpkg' from data source 
#   `/home/edzer/R/x86_64-pc-linux-gnu-library/4.4/sf/gpkg/nc.gpkg' 
#   using driver `GPKG'
# Simple feature collection with 100 features and 14 fields
# Geometry type: MULTIPOLYGON
# Dimension:     XY
# Bounding box:  xmin: -84.3 ymin: 33.9 xmax: -75.5 ymax: 36.6
# Geodetic CRS:  NAD27
```

```{python}
import geopandas as gpd
nc = gpd.read_file("https://github.com/r-spatial/sf/raw/main/inst/gpkg/nc.gpkg")
```


Here, the file name and path file is read from the sf package, which has a different path on every machine, and hence is guaranteed to be present on every sf installation.

Command st_read has two arguments: the data source name (dsn) and the layer. In the example above, the geopackage (GPKG) file contains only a single layer that is being read. If it had contained multiple layers, then the first layer would have been read and a warning would have been emitted. The available layers of a dataset can be queried by


```{r}
st_layers(file)
# Driver: GPKG 
# Available layers:
#   layer_name geometry_type features fields crs_name
# 1    nc.gpkg Multi Polygon      100     14    NAD27
```

```{python}
...
```

```{r}

(file = tempfile(fileext = ".gpkg"))
# [1] "/tmp/RtmpMa6kYF/filebd1a17b06433.gpkg"
st_write(nc, file, layer = "layer_nc")
# Writing layer `layer_nc' to data source 
#   `/tmp/RtmpMa6kYF/filebd1a17b06433.gpkg' using driver `GPKG'
# Writing 100 features with 14 fields and geometry type Multi Polygon.
```

```{python}
...
```


where the file format (GPKG) is derived from the file name extension. Using argument append, st_write can either append records to an existing layer or replace it; if unset, it will err if a layer already exists. The tidyverse-style write_sf will replace silently if append has not been set. Layers can also be deleted using st_delete, which is convenient in particular when they are associated with tables in a database.

For file formats supporting a WKT-2 coordinate reference system, sf_read and sf_write will read and write it. For simple formats such as csv this will not work. The shapefile format supports only a very limited encoding of the CRS.


A very common operation is to subset objects; base R can use [ for this. The rules that apply to data.frame objects also apply to sf objects: records 2-5 and columns 3-7 are selected by

```{r}
nc[2:5, 3:7]
```

```{python}
...
```


but with a few additional features, in particular:

the drop argument is by default FALSE meaning that the geometry column is always selected, and an sf object is returned; when it is set to TRUE and the geometry column is not selected, it is dropped and a data.frame is returned
selection with a spatial (sf, sfc or sfg) object as first argument leads to selection of the features that spatially intersect with that object (see next section); other predicates than intersects can be chosen by setting parameter op to a function such as st_covers or any other binary predicate function listed in Section 3.2.2.


Binary predicates
Binary predicates like st_intersects, st_covers and such (Section 3.2.2) take two sets of features or feature geometries and return for all pairs whether the predicate is TRUE or FALSE. For large sets this would potentially result in a huge matrix, typically filled mostly with FALSE values and for that reason a sparse representation is returned by default:


```{r}
nc5 <- nc[1:5, ]
nc7 <- nc[1:7, ]
(i <- st_intersects(nc5, nc7))
# Sparse geometry binary predicate list of length 5, where the
# predicate was `intersects'
#  1: 1, 2
#  2: 1, 2, 3
#  3: 2, 3
#  4: 4, 7
#  5: 5, 6
```

```{python}
import geopandas as gpd

nc = gpd.read_file("https://github.com/r-spatial/sf/raw/main/inst/gpkg/nc.gpkg")

nc5 = nc[:5]
nc7 = nc[:7]

i = nc5.intersects(nc7)
# <string>:2: UserWarning: The indices of the left and right GeoSeries' are not equal, and therefore they will be aligned (reordering and/or introducing missing values) before executing the operation. If this alignment is the desired behaviour, you can silence this warning by passing 'align=True'. If you don't want alignment and protect yourself of accidentally aligning, you can pass 'align=False'.
i
# 0     True
# 1     True
# 2     True
# 3     True
# 4     True
# 5    False
# 6    False
# dtype: bool
```


```{r}
plot(st_geometry(nc7))
plot(st_geometry(nc5), add = TRUE, border = "brown")
cc = st_coordinates(st_centroid(st_geometry(nc7)))
text(cc, labels = 1:nrow(nc7), col = "blue")
```

```{python}
import matplotlib.pyplot as plt
import geopandas as gpd

nc = gpd.read_file("https://github.com/r-spatial/sf/raw/main/inst/gpkg/nc.gpkg")

nc5 = nc[:5]
nc7 = nc[:7]

i = nc5.intersects(nc7)
# <string>:2: UserWarning: The indices of the left and right GeoSeries' are not equal, and therefore they will be aligned (reordering and/or introducing missing values) before executing the operation. If this alignment is the desired behaviour, you can silence this warning by passing 'align=True'. If you don't want alignment and protect yourself of accidentally aligning, you can pass 'align=False'.

ax = nc7.plot()
nc5.plot(ax=ax, color='brown')

for x, y, label in zip(nc7.geometry.centroid.x, nc7.geometry.centroid.y, nc7.index):
    plt.text(x, y, label, fontsize=12)

plt.axis(False)    
# (np.float64(-82.03946952819824), np.float64(-75.47475929260254), np.float64(36.04697723388672), np.float64(36.61549072265625))
plt.show()
```
Figure 7.2 shows how the intersections of the first five with the first seven counties can be understood. We can transform the sparse logical matrix into a dense matrix by

```{r}
as.matrix(i)
#       [,1]  [,2]  [,3]  [,4]  [,5]  [,6]  [,7]
# [1,]  TRUE  TRUE FALSE FALSE FALSE FALSE FALSE
# [2,]  TRUE  TRUE  TRUE FALSE FALSE FALSE FALSE
# [3,] FALSE  TRUE  TRUE FALSE FALSE FALSE FALSE
# [4,] FALSE FALSE FALSE  TRUE FALSE FALSE  TRUE
# [5,] FALSE FALSE FALSE FALSE  TRUE  TRUE FALSE
```

```{python}
import numpy as np

matrix = np.matrix(i.values)
matrix
# matrix([[ True,  True,  True,  True,  True, False, False]])
```

The number of counties that each of nc5 intersects with is

```{r}
lengths(i)
# [1] 2 3 2 2 2
```

```{python}
...
```

and the other way around, the number of counties in nc5 that intersect with each of the counties in nc7 is

```{r}
lengths(t(i))
# [1] 2 3 2 1 1 1 1
```

The object i is of class sgbp (sparse geometrical binary predicate), and is a list of integer vectors, with each element representing a row in the logical predicate matrix holding the column indices of the TRUE values for that row. It further holds some metadata like the predicate used, and the total number of columns. Methods available for sgbp objects include

```{python}
methods(class = "sgbp")
#  [1] as.data.frame as.matrix     coerce        dim          
#  [5] initialize    Ops           print         show         
#  [9] slotsFromS3   t            
# see '?methods' for accessing help and source code
```

where the only Ops method available is !, the negation operation.


tidyverse

The tidyverse package loads a collection of data science packages that work well together (Wickham and Grolemund 2017; Wickham et al. 2019). Package sf has tidyverse-style read and write functions, read_sf and write_sf that

return a tibble rather than a data.frame,
do not print any output, and
overwrite existing data by default.
Further tidyverse generics with methods for sf objects include filter, select, group_by, ungroup, mutate, transmute, rowwise, rename, slice, summarise, distinct, gather, pivot_longer, spread, nest, unnest, unite, separate, separate_rows, sample_n, and sample_frac. Most of these methods simply manage the metadata of sf objects and make sure the geometry remains present. In case a user wants the geometry to be removed, one can use st_drop_geometry or simply coerce to a tibble or data.frame before selecting:


```{r}
library(tidyverse) |> suppressPackageStartupMessages()
nc |> as_tibble() |> select(BIR74) |> head(3)
# # A tibble: 3 × 1
#   BIR74
#   <dbl>
# 1  1091
# 2   487
# 3  3188
```

```{python}
nc[['BIR74']].head(3)
#     BIR74
# 0  1091.0
# 1   487.0
# 2  3188.0
```

The summarise method for sf objects has two special arguments:

do_union (default TRUE) determines whether grouped geometries are unioned on return, so that they form a valid geometry
is_coverage (default FALSE) in case the geometries grouped form a coverage (do not have overlaps), setting this to TRUE speeds up the unioning
The distinct method selects distinct records, where st_equals is used to evaluate distinctness of geometries.

filter can be used with the usual predicates; when one wants to use it with a spatial predicate, for instance to select all counties less than 50 km away from Orange County, one could use


```{r}
orange <- nc |> dplyr::filter(NAME == "Orange")
wd <- st_is_within_distance(nc, orange, 
                            units::set_units(50, km))
o50 <- nc |> dplyr::filter(lengths(wd) > 0)
nrow(o50)
# [1] 17
```

```{python}
...
```

(where we use dplyr::filter rather than filter to avoid confusion with filter from base R.)

Figure 7.3 shows the results of this analysis, and in addition a buffer around the county borders. Note that this buffer serves for illustration: it was not used to select the counties.

```{r}
og <- st_geometry(orange)
buf50 <- st_buffer(og, units::set_units(50, km))
all <- c(buf50, st_geometry(o50))
plot(st_geometry(o50), lwd = 2, extent = all)
plot(og, col = 'orange', add = TRUE)
plot(buf50, add = TRUE, col = NA, border = 'brown')
plot(st_geometry(nc), add = TRUE, border = 'grey')
```

```{python}
...
```

7.2 Spatial joins

In regular (left, right, or inner) joins, joined records from a pair of tables are reported when one or more selected attributes match (are identical) in both tables. A spatial join is similar, but the criterion to join records is not equality of attributes but a spatial predicate. This leaves a wide variety of options in order to define spatially matching records, using binary predicates listed in Section 3.2.2. The concepts of “left”, “right”, “inner”, or “full” joins remain identical to the non-spatial join as the options for handling records that have no spatial match.

When using spatial joins, each record may have several matched records, yielding a large result table. A way to reduce this complexity may be to select from the matching records the one with the largest overlap with the target geometry. An example of this is shown (visually) in Figure 7.4; this is done using st_join with argument largest = TRUE.

```{r}
# example of largest = TRUE:
system.file("gpkg/nc.gpkg", package="sf") |> 
    read_sf() |>
    st_transform('EPSG:2264') -> nc
gr <- st_sf(
         label = apply(expand.grid(1:10, LETTERS[10:1])[,2:1], 1, paste0, collapse = ""),
         geom = st_make_grid(nc))
gr$col <- sf.colors(10, categorical = TRUE, alpha = .3)
# cut, to verify that NA's work out:
gr <- gr[-(1:30),]
suppressWarnings(nc_j <- st_join(nc, gr, largest = TRUE))
par(mfrow = c(2,1), mar = rep(0,4))
plot(st_geometry(nc_j), border = 'grey')
plot(st_geometry(gr), add = TRUE, col = gr$col)
text(st_coordinates(st_centroid(st_geometry(gr))), labels = gr$label, cex = .85)
# the joined dataset:
plot(st_geometry(nc_j), border = 'grey', col = nc_j$col)
text(st_coordinates(st_centroid(st_geometry(nc_j))), labels = nc_j$label, cex = .7)
plot(st_geometry(gr), border = '#88ff88aa', add = TRUE)
```

```{python}
...
```

Sampling, gridding, interpolating
Several convenience functions are available in package sf, some of which will be discussed here. Function st_sample generates a sample of points randomly sampled from target geometries, where target geometries can be point, line, or polygon geometries. Sampling strategies can be (completely) random, regular, or (with polygons) triangular. Chapter 11 explains how spatial sampling (or point pattern simulation) methods available in package spatstat are interfaced through st_sample.

Function st_make_grid creates a square, rectangular, or hexagonal grid over a region, or points with the grid centres or corners. It was used to create the rectangular grid in Figure 7.4.

Function st_interpolate_aw “interpolates” area values to new areas, as explained in Section 5.3, both for intensive and extensive variables.


```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
```{r}

```

```{python}

```
































```{r}

```

```{python}

```
