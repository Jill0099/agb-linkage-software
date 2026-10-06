# Latitude-dependent historical window dimensions

The companion CSV uses hypothetical raster-cell centres at longitude 112° and latitudes 20°, 30°, 40° and 50°N. These are illustrative coordinates, not company observations.

For each nominal radius label, the recovered rule is `half=max(1, round(radius_m/111000/resolution_degrees))`. The complete square side is `(2*half+1)*resolution_degrees`. The actual raster step is 0.00026949458523585647°, giving 35, 67 and 335 cells per side.

Distances were calculated with the WGS84 ellipsoid using `pyproj.Geod.inv` (pyproj 3.7.2) between the midpoints of opposite outer cell edges. The assumed centre lies at a raster-cell centre; actual office coordinates need not. These distances describe the whole cell footprint, rather than the separation between outermost cell centres. They are neither circular buffers nor estimates of a company's real footprint.

The 335-cell square spans 0.09028068605401192° per side. Its north–south midpoint distance is approximately 9.99–10.04 km across the illustrated latitudes, while its east–west distance ranges from 9.45 km at 20°N to 6.47 km at 50°N. Differences in cell-area weights, forest-cover fractions, masks and coordinate provenance require separate consideration.
