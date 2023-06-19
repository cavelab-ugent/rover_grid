import pandas as pd
import numpy as np
import argparse
import os

def sw_corner_to_grid(easting_northing_sw, grid_size, ew_number_of_pos, ns_number_of_points):
    # get array of points on ew and ns edges
    easting_array = np.arange(easting_northing_sw[0], easting_northing_sw[0] + ew_number_of_pos*grid_size, grid_size)
    northing_array = np.arange(easting_northing_sw[1], easting_northing_sw[1] + ns_number_of_points*grid_size, grid_size)
    # convert edge arrays to coordinate grid
    xv, yv = np.meshgrid(easting_array, northing_array)
    coords = np.array([xv.flatten(), yv.flatten()]).T
    return coords

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--csv", type=str, required=True)
    parser.add_argument("-g", "--gridsize", type=int, required=True)
    parser.add_argument("-e", "--ew_points", type=int, required=True)
    parser.add_argument("-n", "--ns_points", type=int, required=True)

    args = parser.parse_args()

    if not os.path.exists(args.pointcloud):
        print("couldnt find csv_file, exiting")
        os._exit(1)
    
    df = pd.read_csv(args.csv)

    # get SW point info, assumes only one position
    df_east = df[["Easting"]].values[0][0]
    df_north = df[["Northing"]].values[0][0]
    df_elevation = df[["Elevation"]].values[0][0]

    coords = sw_corner_to_grid(np.array([df_east, df_north]), args.gridsize, args.ew_points, args.ns_points)

    # add dummy elevation
    elevation_arr = np.ones((len(coords),1)) * df_elevation
    coords_el = np.hstack((coords, elevation_arr))

    df = pd.DataFrame(coords_el, columns=["Easting", "Northing", "Elevation"])
    
    df['Name'] = df.index

    df.to_csv("grid.csv", index=False)


if __name__ == "__main__":
    main()