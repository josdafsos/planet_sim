from simulation import Body
import numpy as np

def create_solar_system(width, height):
    # Define instances of bodies

    center_x_vis = width / 2
    center_y_vis = height / 2

    max_distance = 228e9  # maximum distance (Mars to SUn) in meters
    max_distance = 1.1 * max_distance  # maximum distance in meters
    pix_to_m = max_distance / (width / 2)  # conversion of pixels to km

    rot_vel_venus = 35e3  # Venus rotational velocity around Sun, m/s
    rot_vel_mercury = 47e3  # Mercury rotational velocity around Sun, m/s
    rot_vel_earth = 30e3  # Earth tangential velocity around Sun, m/s
    rot_vel_moon = rot_vel_earth + 1.022e3  # Moons tangential velocity around Sun, m/s
    rot_vel_mars = 24e3  # Mars tangential velocity around Sun, m/s

    bodies = [
        Body(name='Sun',
             color=(252, 229, 112),
             radius=696e6 * 10,  # radius adjusted by 10 for visualization
             mass=2e30,
             pos_xy_vis=np.array([center_x_vis, center_y_vis]),
             pos_xy=np.array([max_distance, 0])),

        Body(name='Venus',
             color=(255, 198, 73),
             radius=6.05e6 * 500,  # radius adjusted by 500 for visualization
             mass=4.57e24,
             pos_xy_vis=np.array([center_x_vis - 108.2e9 / pix_to_m, height / 2]),
             pos_xy=np.array([max_distance - 108.2e9, 0]),
             vel=[0, rot_vel_venus]),

        Body(name='Mercury',
             color=(183, 184, 185),
             radius=2.44e6 * 1000,  # radius adjusted by 500 for visualization
             mass=3.3e23,
             pos_xy_vis=np.array([center_x_vis - 57.9e9 / pix_to_m, height / 2]),
             pos_xy=np.array([max_distance - 57.9e9, 0]),
             vel=[0, rot_vel_mercury]),

        Body(name='Earth',
             color=(0, 94, 184),
             radius=6371e3 * 500,  # radius adjusted by 500 for visualization
             mass=5.97e24,
             pos_xy_vis=np.array([center_x_vis - 149e9 / pix_to_m, height / 2]),
             pos_xy=np.array([max_distance - 149e9, 0]),
             vel=[0, rot_vel_earth]),

        Body(name='Moon',
             color=(246, 241, 213),
             radius=1737e3 * 200 * 2,  # radius adjusted by 200 for visualization
             mass=7.35e22,
             pos_xy_vis=np.array([center_x_vis - (149e9 + 384.4e6) / pix_to_m, height / 2]),
             pos_xy=np.array([max_distance - (149e9 + 384.4e6), 0]),
             vel=[0, rot_vel_moon]),

        Body(name='Mars',
             color=(156, 46, 53),
             radius=3.4e6 * 500,  # radius adjusted by 500 for visualization
             mass=6.42e23,
             pos_xy_vis=np.array([center_x_vis - (228e9) / pix_to_m, height / 2]),
             pos_xy=np.array([max_distance - (228e9), 0]),
             vel=[0, rot_vel_mars]),
    ]

    return bodies

def create_three_body_system(width, height):

    ax, ay = 100, 100
    bx, by = 200, 200
    bodies = [
        Body(name='A',
             color=(252, 229, 112),
             radius=696e6 * 10,  # radius adjusted by 10 for visualization
             mass=30e4,
             pos_xy_vis=np.array([ax, ay]),
             pos_xy=np.array([ax, ay])),

        Body(name='B',
             color=(255, 198, 73),
             radius=6.05e6 * 500,  # radius adjusted by 500 for visualization
             mass=10e4,
             pos_xy_vis=np.array([bx, by]),
             pos_xy=np.array([bx, by]),
             vel=[0, 10]),

        ]
    return bodies