import pandas as pd
import numpy as np
import argparse
import os
# import matplotlib.pyplot as plt
import math as m

def sw_corner_to_grid(easting_northing_sw, grid_size, ew_number_of_pos, ns_number_of_points, angle):
    # get array of points on ew and ns edges
    easting_array = np.arange(easting_northing_sw[0], easting_northing_sw[0] + ew_number_of_pos*grid_size, grid_size)
    northing_array = np.arange(easting_northing_sw[1], easting_northing_sw[1] + ns_number_of_points*grid_size, grid_size)
    # convert edge arrays to coordinate grid
    xv, yv = np.meshgrid(easting_array, northing_array)
    coords = np.array([xv.flatten(), yv.flatten()]).T

    # rotate around sw_point
    # first translate to origin
    coords = coords - easting_northing_sw
    # apply rotation
    c = m.cos(np.deg2rad(angle))
    s = m.sin(np.deg2rad(angle))
    matrix = np.array([[c,s], [-s, c]])
    coords = np.matmul(matrix, coords.T).T
    # translate back
    coords += easting_northing_sw
    return coords

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--csv", type=str, required=True)
    parser.add_argument("-g", "--gridsize", type=int, required=True)
    parser.add_argument("-e", "--ew_points", type=int, required=True)
    parser.add_argument("-n", "--ns_points", type=int, required=True)
    parser.add_argument("-a", "--angle", type=float, required=True)

    args = parser.parse_args()

    if not os.path.exists(args.csv):
        print("couldnt find csv_file, exiting")
        os._exit(1)

    print(f"Laying out {args.ew_points} points in east-west direction and {args.ns_points} in north-south direction.")
    print(f"Using a gridsize of {args.gridsize} m. and angle of {args.angle} deg. (angle with n-s axis in clockwise direction around sw point)")
    
    df = pd.read_csv(args.csv)

    # TODO: change to lat/long so Global CS can be used on the Rover

    # get SW point info, assumes only one position
    df_east = df[["Easting"]].values[0][0]
    df_north = df[["Northing"]].values[0][0]
    df_elevation = df[["Elevation"]].values[0][0]

    coords = sw_corner_to_grid(np.array([df_east, df_north]), args.gridsize, args.ew_points, args.ns_points, args.angle)

    # DEBUG
    # print(coords)
    # plt.axis('equal')
    # plt.scatter(coords[:,0], coords[:,1])
    # plt.show()

    # add dummy elevation
    elevation_arr = np.ones((len(coords),1)) * df_elevation
    coords_el = np.hstack((coords, elevation_arr))

    df = pd.DataFrame(coords_el, columns=["Easting", "Northing", "Elevation"])
    
    # start at 1
    df['Name'] = df.index + 1
    # remove first row as this points has been recorded already
    df = df.iloc[1:]

    df.to_csv("grid.csv", index=False)


if __name__ == "__main__":
    main()