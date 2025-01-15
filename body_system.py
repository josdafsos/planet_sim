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


def create_solar_system_no_scaling(width, height):
    # Define instances of bodies

    # center_x_vis = width / 2
    # center_y_vis = height / 2
    #
    # max_distance = 228e9  # maximum distance (Mars to SUn) in meters
    # max_distance = 1.1 * max_distance  # maximum distance in meters
    # pix_to_m = max_distance / (width / 2)  # conversion of pixels to km

    rot_vel_venus = 35e3  # Venus rotational velocity around Sun, m/s
    rot_vel_mercury = 47e3  # Mercury rotational velocity around Sun, m/s
    rot_vel_earth = 30e3  # Earth tangential velocity around Sun, m/s
    rot_vel_moon = rot_vel_earth + 1.022e3  # Moons tangential velocity around Sun, m/s
    rot_vel_mars = 24e3  # Mars tangential velocity around Sun, m/s

    bodies = [
        Body(name='Sun',
             color=(252, 229, 112),
             radius=10,  # radius adjusted by 10 for visualization
             mass=2e30,
             pos_xy=np.array([0, 0])),

        Body(name='Venus',
             color=(255, 198, 73),
             radius=20,  # radius adjusted by 500 for visualization
             mass=4.57e24,
             pos_xy=np.array([108.2e9, 0]),
             vel=[0, rot_vel_venus]),

        Body(name='Mercury',
             color=(183, 184, 185),
             radius=20,  # radius adjusted by 500 for visualization
             mass=3.3e23,
             pos_xy=np.array([57.9e9, 0]),
             vel=[0, rot_vel_mercury]),

        Body(name='Earth',
             color=(0, 94, 184),
             radius=20,  # radius adjusted by 500 for visualization
             mass=5.97e24,
             pos_xy=np.array([149e9, 0]),
             vel=[0, rot_vel_earth]),

        Body(name='Moon',
             color=(246, 241, 213),
             radius=20,  # radius adjusted by 200 for visualization
             mass=7.35e22,
             pos_xy=np.array([(149e9 + 384.4e6), 0]),
             vel=[0, rot_vel_moon]),

        Body(name='Mars',
             color=(156, 46, 53),
             radius=20,  # radius adjusted by 500 for visualization
             mass=6.42e23,
             pos_xy=np.array([228e9, 0]),
             vel=[0, rot_vel_mars]),
    ]

    return bodies  # second argument is for temporary compatibility



def create_three_body_system(width, height):

    ax, ay = 100, 100
    bx, by = 200, 200
    bodies = [
        Body(name='A',
             color=(252, 0, 0),
             radius=10,
             mass=30e7,
             pos_xy=np.array([ax, ay])),

        Body(name='B',
             color=(0, 198, 0),
             radius=6,
             mass=10e6,
             pos_xy=np.array([bx, by]),
             vel=[0.001, -0.005]),

        Body(name='C',
             color=(0, 0, 200),
             radius=8,
             mass=15e6,
             pos_xy=np.array([1000, 1000]),
             vel=[0, 0.001]),

        ]
    return bodies


def create_body_system(width, height): 
    
     # Function to define instances of bodies 


     center_x_vis = width/2
     center_y_vis = height/2
     
     # Define instances of planets
     bodies = [
     Body(     name       = 'Sun', 
               color        = (252, 229, 112), 
               radius       = 696e6,                       
               mass         = 2e30, 
               orb_vel_in   = np.array([0,0]),
               orbit_radius = None),
    
     Body(     name         = 'Venus', 
               color        = (255, 198, 73), 
               radius       = 6.05e6,        
               mass         = 4.57e24,                        
               orb_vel_in   = np.array([0, 35.02e3]),
               orbit_radius = 108e9),
     
     Body(     name         ='Mercury', 
               color        = (183, 184, 185), 
               radius       = 2.44e6,       
               mass         = 3.3e23,
               orb_vel_in   = np.array([0,47.36e3]),
               orbit_radius = 58e9),
    
     Body(     name         = 'Earth', 
               color        = (0,94,184), 
               radius       = 6.371e6,
               mass         = 5.97e24,
               orb_vel_in   = np.array([0,29.8e3]),
               orbit_radius = 1.5e11),

     Body(     name         = 'Mars', 
               color        = (156, 46, 53), 
               radius       = 3.4e6,       
               mass         = 6.42e23,
               orb_vel_in   = np.array([0,24.08e3]),
               orbit_radius = 228e9),
     ]


     # Step 1 - define maximum distance and scaling 
     max_distance = 0    
     for body in bodies: 
          if body.orbit_radius is not None:
               max_distance = max(max_distance,body.orbit_radius)
     
     resolution       = min(width, height)
     max_distance     = 1.1 * max_distance                  # maximum distance in meters
     distance_scaler  = max_distance / (resolution / 2)     # conversion of pixels to km


     # Step 2 - define starting locations of the bodies in the system
        
     ## Step 2.1 - find the heaviest body and put it into the center
     mass            = 0
     center_body_ind = None
     for ind in range(0,len(bodies)): 
          if bodies[ind].mass > mass: 
               mass            = bodies[ind].mass
               center_body_ind = ind    
     bodies[center_body_ind].pos_xy      = np.array([max_distance, max_distance])      # coordinates in meters
     bodies[center_body_ind].pos_xy_vis  = np.array([height / 2, width / 2])           # coordinate in pixels
     bodies[center_body_ind].radius_vis  = resolution / 20                             # Radius of the heaviest body is randomly specified as resulution divided by 20
     bodies[center_body_ind].path_vis.append(np.array([height / 2, width / 2]))
     bodies[center_body_ind].path_vis.append(np.array([height / 2, width / 2]))
     
     radius_scaler  = bodies[center_body_ind].radius / bodies[center_body_ind].radius_vis


     ## Step 2.2 - define position of the bodies relative to the heaviest body
     for ind in range(0,len(bodies)): 
          if ind != center_body_ind: 
               
               bodies[ind].pos_xy = np.array([max_distance - bodies[ind].orbit_radius, max_distance])         
               bodies[ind].radius_vis = max(bodies[ind].radius / radius_scaler, resolution / 100)  

          bodies[ind].pos_xy_vis = bodies[ind].pos_xy / distance_scaler
          bodies[ind].path_vis.append(bodies[ind].pos_xy_vis)
          bodies[ind].path_vis.append(bodies[ind].pos_xy_vis)         


     return bodies, distance_scaler


