import pandas as pd
import numpy as np
import argparse
import os
# import matplotlib.pyplot as plt
import math as m

def grid_from_4_corners(corners, n_points_x, n_points_y):
    # create grid with n_points in unit square
    x = np.linspace(0, 1, n_points_x)
    y = np.linspace(0, 1, n_points_y)
    xv, yv = np.meshgrid(x, y)
    positions = np.hstack([xv.ravel()[:,np.newaxis], yv.ravel()[:,np.newaxis]])

    # get orientation of points, assumes quasi rectangular
    sorted_by_x = corners[corners[:, 0].argsort()]
    left_points = sorted_by_x[:2]
    left_sorted_y = left_points[left_points[:, 1].argsort()]
    # bottom left point: minimal y-value of 2 left-most points
    left_bottom = left_sorted_y[0]
    # top left point
    left_top = left_sorted_y[1]
    right_points = sorted_by_x[2:]
    right_sorted_y = right_points[right_points[:, 1].argsort()]
    # bottom right point
    right_bottom = right_sorted_y[0]
    # top right point
    right_top = right_sorted_y[1]

    # base translation is just coordinate of bottom left point
    base_translation = left_bottom
    # get vector u and v
    u = right_bottom - left_bottom
    v = left_top - left_bottom
    # calculate vector w
    w = right_top - (base_translation + u + v)

    # get transformation matrix
    transformation_matrix = np.vstack((u,v,w)).T

    # get xy_column
    xy_column = positions[:,0]*positions[:,1]
    x_y_xy_matrix = np.hstack((positions, xy_column[:,np.newaxis])).T

    # perform transformation
    transformed_coords = np.matmul(transformation_matrix, x_y_xy_matrix).T
    # apply base translation
    transformed_coords += base_translation
    return transformed_coords

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--csv", type=str, required=True)
    parser.add_argument("-e", "--ew_points", type=int, required=True)
    parser.add_argument("-n", "--ns_points", type=int, required=True)
    parser.add_argument("-o", "--out_file", type=str, default=None)

    args = parser.parse_args()

    if not os.path.exists(args.csv):
        print("couldnt find csv_file, exiting")
        os._exit(1)

    print(f"Laying out grid based on four corners with {args.ew_points} points in east-west direction and {args.ns_points} in north-south direction.")
    print(f'INFO: This method "squeezes" a perfectly rectangular grid into the quadriliteral formed by the four corners. If the plot is very crooked, scan positions might be a bit sparse at the extremes.' )
    print(f"The east west direction will be determined by the edge between corners the most sw point and the most se point.")
    print(f"If the result is opposite then expected, just switch around the ew_points and ns_points args")

    df = pd.read_csv(args.csv)

    if len(df.index) < 4:
        print(f"ERROR: CSV file contains only {len(df.index)} rows, need 4 corners for this script, exiting.")
        os._exit(1)
    if len(df.index) > 4:
        print(f"WARNING: CSV file contains more than 4 rows ({len(df.index)}), using first 4")
        df = df.head(4)

    df_corners = df[["Easting", "Northing"]].values
    df_elevation = df[["Elevation"]].values[0][0]

    coords = grid_from_4_corners(df_corners, args.ew_points, args.ns_points)

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