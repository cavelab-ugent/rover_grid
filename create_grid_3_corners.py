import pandas as pd
import numpy as np
import argparse
import os
# import matplotlib.pyplot as plt
import math as m

from create_grid_4_corners import grid_from_4_corners

def grid_from_3_corners(corners, n_points_x, n_points_y, inner_index):

    # generate fourth corner:
    # take corner point with two neighbours and add vectors to neighbours to optain fourth corner

    if inner_index is not None:

        c_ind = inner_index -1
        center_point = corners[c_ind]
        edge_points = [corners[(c_ind+1)%3], corners[(c_ind+2)%3]]
    
    else:
        # detect inner corner automatically
        # check distance between 3 corners, assume 2 points with largest distance between them are edges
        distance_0_1 = np.linalg.norm(corners[1]-corners[0])
        distance_0_2 = np.linalg.norm(corners[2]-corners[0])
        distance_1_2 = np.linalg.norm(corners[2]-corners[1])

        if distance_0_1 > distance_0_2 and distance_0_1 > distance_1_2:
            center_point = corners[2]
            edge_points = [corners[0], corners[1]]
        elif distance_0_2 > distance_1_2:
            center_point = corners[1]
            edge_points = [corners[0], corners[2]]
        else:
            center_point = corners[0]
            edge_points = [corners[1], corners[2]]


    fourth_corner = center_point + (edge_points[0] - center_point) + (edge_points[1] - center_point)
    corners = np.concatenate((corners, np.expand_dims(fourth_corner, axis=0)), axis=0)

    # then just run as if given 4 corners

    return grid_from_4_corners(corners, n_points_x, n_points_y)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--csv", type=str, required=True)
    parser.add_argument("-e", "--ew_points", type=int, required=True)
    parser.add_argument("-n", "--ns_points", type=int, required=True)
    parser.add_argument("-i", "--inner_index", type=int)
    parser.add_argument("-o", "--out_file", type=str, default=None)

    args = parser.parse_args()

    if not os.path.exists(args.csv):
        print("couldnt find csv_file, exiting")
        os._exit(1)

    print(f"Laying out grid based on three corners with {args.ew_points} points in east-west direction and {args.ns_points} in north-south direction.")
    print(f'INFO: This method generates a four corner, then squeezes grid into quadriliteral formed by these corners')
    print(f"The inner crom from which to project will be determined as the corner with the largest angle in the triangle formed by the 3 corners.")
    print(f"In a very parallelogram-shaped plot, this might not give the desired plot, in which case you can give the index (1,2 or 3) of the inner corner point using the -i/--inner_index parameter.")

    df = pd.read_csv(args.csv)

    if len(df.index) < 3:
        print(f"ERROR: CSV file contains only {len(df.index)} rows, need 3 corners for this script, exiting.")
        os._exit(1)
    if len(df.index) > 3:
        print(f"WARNING: CSV file contains more than 3 rows ({len(df.index)}), using first 3")
        df = df.head(3)

    if args.inner_index is not None:
        if args.inner_index not in range(1,4):
            print(f"Inner index {args.inner_index} is not in (1,2,3), please pick appropriate value.")
            os._exit(1)

    df_corners = df[["Easting", "Northing"]].values
    df_elevation = df[["Elevation"]].values[0][0]

    coords = grid_from_3_corners(df_corners, args.ew_points, args.ns_points, args.inner_index)

    # add dummy elevation
    elevation_arr = np.ones((len(coords),1)) * df_elevation
    coords_el = np.hstack((coords, elevation_arr))

    df = pd.DataFrame(coords_el, columns=["Easting", "Northing", "Elevation"])
    df['Name'] = df.index

    if args.out_file is not None:
        out_path = args.out_file
    else:
        out_path = "grid_generated.csv"
    df.to_csv(out_path, index=False)
    print(f"Done, output csv saved at {out_path}")


if __name__ == "__main__":
    main()