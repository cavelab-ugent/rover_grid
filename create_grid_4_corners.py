import pandas as pd
import numpy as np
import argparse
import os
import matplotlib.pyplot as plt
import math as m

def grid_from_corners(corners, n_points):
    # create grid with n_points in unit square
    x = np.linspace(0, 1, n_points)
    y = np.linspace(0, 1, n_points)
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
    parser.add_argument("-n", "--n_points", type=int, required=True)
    parser.add_argument("--keep_corners", action='store_true', help="whether to keep the already recorded/marked corners in the output csv file")
    parser.add_argument("-o", "--out_file", type=str, default=None)

    args = parser.parse_args()

    if not os.path.exists(args.csv):
        print("couldnt find csv_file, exiting")
        os._exit(1)

    print(f"Laying out grid based on four corners of {args.n_points} points per line.")
    print(f'This method "squeezes" a perfectly rectangular grid into the quadriliteral formed by the four corners. If the plot is very crooked, scan positions might be a bit sparse at the extremes.' )
    
    df = pd.read_csv(args.csv)

    # TODO: get four corners out
    df_corners = df[["Easting", "Northing"]].values
    df_elevation = df[["Elevation"]].values[0][0]

    coords = grid_from_corners(df_corners, args.n_points)

    # DEBUG
    # print(coords)
    # plt.axis('equal')
    # plt.scatter(coords[:,0], coords[:,1])
    # # plt.scatter(df_corners[:,0], df_corners[:,1], color="r")
    # plt.show()

    # add dummy elevation
    elevation_arr = np.ones((len(coords),1)) * df_elevation
    coords_el = np.hstack((coords, elevation_arr))

    df = pd.DataFrame(coords_el, columns=["Easting", "Northing", "Elevation"])
    

    # remove first row as this points has been recorded already
    if not args.keep_corners:
        df = df.iloc[4:]
    df['Name'] = df.index
    if args.out_file is not None:
        df.to_csv(args.out_file, index=False)
    else:
        df.to_csv("grid_generated.csv", index=False)


if __name__ == "__main__":
    main()