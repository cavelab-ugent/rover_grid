# Script to generate a grid from SW position using Rover.

1. Install dependencies: Python 3 + ``` pip/conda install pandas ```
2. Export Rover project to csv after registering SW corner
3.
```
python create_grid.py --csv /path/to/csvfile --gridsize GRIDSIZE --ew_points EW_POINTS --ns_points NS_POINTS --angle ANGLE
```

- -c/--csv: path to exported csv file
- -g/--gridsize: desired grid size in meters
- -e/--ew_points: desired number of points in East/West direction
- -n/--ns_points: desired number of points in North/South direction
- -a/--angle: angle with NS axis, rotated clockwise around SW corner (optional)
- --add_first: also write the first sw point the grid is based on to new csv (optional)

4. Import created grid.csv into Rover project
