import pandas as pd
import numpy as np
import argparse
import os
# import matplotlib.pyplot as plt
import math as m

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def grid_from_2_corners(corners, grid_size, n_point_along, n_points_projection, project_inverse=False):
    # first translate to origin
    corners_translated = corners - corners[0]

    # get angle between y-axis and edge from corner 1 to corner 2
    vector_edge = corners_translated[1] - corners_translated[0]
    vector_y_axis = [0,1]
    angle = angle_between(vector_edge, vector_y_axis)

    # rotate so edge 1-2 is aligned with y-axis
    c = m.cos(angle)
    s = m.sin(angle)
    matrix = np.array([[c,s], [-s, c]])
    corners_rotated = np.matmul(matrix, corners_translated.T).T

    # layout grid aligned with x,y
    if project_inverse:
        easting_array = np.arange(corners_rotated[0][0] - n_points_projection*grid_size, corners_rotated[0][0], grid_size)
    else:
        easting_array = np.arange(corners_rotated[0][0], corners_rotated[0][0] + n_points_projection*grid_size, grid_size)
    northing_array = np.linspace(corners_rotated[0][1], corners_rotated[1][1], num=n_point_along)

    print(f"Info: actual grid size along edge: {northing_array[1]-northing_array[0]}")
    # convert edge arrays to coordinate grid
    xv, yv = np.meshgrid(easting_array, northing_array)
    coords = np.array([xv.flatten(), yv.flatten()]).T

    # then rotate with opposite angle as in initial rotation (see one point method!)
    coords = np.matmul(matrix.T, coords.T).T

    # retranslate coordinates
    coords = coords + corners[0]

    return coords



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--csv", type=str, required=True)
    parser.add_argument("-g", "--gridsize", type=int, required=True)
    parser.add_argument("-a", "--n_points_along", type=int, required=True)
    parser.add_argument("-p", "--n_points_projected", type=int, required=True)
    parser.add_argument("--project_inverse", action="store_true")
    parser.add_argument("-o", "--out_file", type=str, default=None)

    args = parser.parse_args()

    if not os.path.exists(args.csv):
        print("couldnt find csv_file, exiting")
        os._exit(1)

    print(f"Laying out grid based on two corners with {args.n_points_along} points along the direction of the edge between given corners and {args.n_points_projected} in projected direction.")
    print(f'INFO: this method generates the grid by projecting perpendicular to the edge defined by the 2 given corners.')
    print("By default, it projects to the right size of the vector between corner 1 and 2, so on the right when walking from the first measurement to the second.")

    df = pd.read_csv(args.csv)

    if len(df.index) < 2:
        print(f"ERROR: CSV file contains only {len(df.index)} rows, need 2 corners for this script, exiting.")
        os._exit(1)
    if len(df.index) > 2:
        print(f"WARNING: CSV file contains more than 2 rows ({len(df.index)}), using first 2")
        df = df.head(2)

    df_corners = df[["Easting", "Northing"]].values
    df_elevation = df[["Elevation"]].values[0][0]

    coords = grid_from_2_corners(df_corners, args.gridsize, args.n_points_along, args.n_points_projected, args.project_inverse)

    # add dummy elevation
    elevation_arr = np.ones((len(coords),1)) * df_elevation
    coords_el = np.hstack((coords, elevation_arr))

    df = pd.DataFrame(coords_el, columns=["Easting", "Northing", "Elevation"])
    df['Name'] = df.index

    # print(f"INFO: actual grid_size along given edge: {}")

    if args.out_file is not None:
        out_path = args.out_file
    else:
        out_path = "grid_generated.csv"
    df.to_csv(out_path, index=False)
    print(f"Done, output csv saved at {out_path}")


if __name__ == "__main__":
    main()