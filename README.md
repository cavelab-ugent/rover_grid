# Emlid rover grid scripts

This repo contains scripts to generate a scanning grid using an Emlid Reach rover.
Instructions on rover usage can be found in the included pdf, instructions to run the grid setup can be found below.

1. Install dependencies: Python 3 + ``` pip/conda install pandas ```
2. Export Rover project to csv after registering SW corner
3. Two options:

Create grid from SW point:

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


Create grid from 4 corner points

```
python create_grid_4_corners.py --csv /path/to/csvfile  --n_points N_POINTS [--out_file /path/to/outfile]
```

- -c/--csv: path to exported csv file
- -n/--n_points: desired number of points per line (NOTE: different number of points not supported yet, if you need this send me an email)
- (optional) -o/--out_file: path of output file



4. Import grid_generated.csv/output_name.csv into Rover project (also see manual on Teams)
