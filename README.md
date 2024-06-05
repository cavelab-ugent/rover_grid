# Emlid rover grid scripts

This repo contains scripts to generate a scanning grid using an Emlid Reach rover.
Detailed instructions on the entire Emlid workflow can be found in the attached Manual or on Teams.

1. Install dependencies: Python 3 + ``` pip/conda install pandas ``` (already installed if running on fieldwork phone)
2. Export Rover project to csv after registering 1/2/3/4 corners.
3. Run grid generation script
4. Import grid_generated.csv/custom_output_name.csv into Rover project

## Create grid from single (SW) point:

```
python create_grid.py --csv /path/to/csvfile --gridsize GRIDSIZE --ew_points EW_POINTS --ns_points NS_POINTS [--out_file /path/to/outfile] [--angle ANGLE] [--keep_corner] 
```

- -c/--csv: path to exported csv file
- -g/--gridsize: desired grid size in meters
- -e/--ew_points: desired number of points in East/West direction
- -n/--ns_points: desired number of points in North/South direction
- (optional) -a/--angle: angle with NS axis, rotated clockwise around SW corner 
- (optional) --keep_corner: also keeps the first sw point the grid is based on in the new csv file
- (optional) -o/--out_file: path of output file

> NOTE: SW corner is assumed in the script, however it will still work for other corners. Make sure to set ew_points, ns_points and angle accordingly and double check results.


## Create grid from 4 corner points:

```
python create_grid_4_corners.py --csv /path/to/csvfile  --ew_points EW_POINTS --ns_points NS_POINTS [--out_file /path/to/outfile]
```

- -c/--csv: path to exported csv file
- -e/--ew_points: desired number of points in East/West direction
- -n/--ns_points: desired number of points in North/South direction
- (optional) -o/--out_file: path of output file

> NOTE: ew direction is determined automatically as the edge from the most sw corner to the most se corner. If this does not give the desired result, just switch around the ew_points and ns_points args.

