import pygame
import numpy as np
from collections import deque
import time
import threading

# Define Body class
class Body: 

    def __init__(self, name, color, radius, mass, satellite_of, orbit_radius, orb_vel_in):
        self.name           = name
        self.color          = color
        self.radius         = radius           # radius in meters
        self.mass           = mass             # mass in kg
        self.satellite_of   = satellite_of     # defines if the Body is someone's satellite (used to adjust position and orbital velocity)
        self.orbit_radius   = orbit_radius     # orbit radius of the body in meters
        self.orb_vel_in     = orb_vel_in       # orbital velocity in meters per second (to initiate the movement)

        # the following parameters will be defined when Solar system is initiated
        self.vel            = np.array([0,0])           # orbital velocity of a body at in meters per second
        self.pos_xy         = None                      # position in meters
        self.pos_xy_vis     = None                      # position in pixels (for visualization) 
        self.radius_vis     = None                      # radius in pixels (for visualization)
        self.path_vis       = deque(maxlen=24*1000)        # visualizaed trajectory of the body in pixels (for visualization)


    def update_position(self, distance_scaler, dt):
        self.vel        = self.vel + self.acc * dt
        self.pos_xy     = self.pos_xy + self.vel * dt
        self.pos_xy_vis = self.pos_xy_vis + self.vel * dt / distance_scaler


    def track_trajectory(self):
        self.path_vis.append((self.pos_xy_vis[0], self.pos_xy_vis[1]))


class Solar_system:

    @staticmethod
    def initiate_system(width, height, bodies):
        # this function is used to define the following: 
        # 1) starting x- and y- coordinates of all the bodies (in meters)
        # 2) starting x- and y- coordinates of all the bodies (in pixels for visualization)
        # 3) radii of all the bodies (scaled in pixels for visualization)

        # Step 1 - define maximum distance and scaling 
        max_distance = 0    
        for body in bodies: 
            if body.orbit_radius is not None:
                max_distance = max(max_distance,body.orbit_radius)
        
        Solar_system.resolution       = min(width, height)
        Solar_system.max_distance     = 1.1 * max_distance                                            # maximum distance in meters
        Solar_system.distance_scaler  = Solar_system.max_distance / (Solar_system.resolution / 2)     # conversion of pixels to km

        # Step 2 - define starting locations of the bodies in the system
        
        ## Step 2.1 - find the heaviest body and put it into the center
        mass            = 0
        center_body_ind = None
        for ind in range(0,len(bodies)): 
            if bodies[ind].mass > mass: 
                mass            = bodies[ind].mass
                center_body_ind = ind    
        bodies[center_body_ind].pos_xy      = np.array([Solar_system.max_distance, Solar_system.max_distance])      # coordinates in meters
        bodies[center_body_ind].pos_xy_vis  = np.array([height / 2, width / 2])                                     # coordinate in pixels
        bodies[center_body_ind].radius_vis  = Solar_system.resolution / 20                                          # Radius of the heaviest body is randomly specified as resulution divided by 20

        bodies[center_body_ind].path_vis.append(np.array([height / 2, width / 2]))
        bodies[center_body_ind].path_vis.append(np.array([height / 2, width / 2]))
        
        Solar_system.radius_scaler          = bodies[center_body_ind].radius / bodies[center_body_ind].radius_vis


        ## Step 2.2 - define position of the bodies relative to the heaviest body
        for ind in range(0,len(bodies)): 
            if ind != center_body_ind: 
                
                if bodies[ind].satellite_of is None: 
                    bodies[ind].pos_xy = np.array([Solar_system.max_distance - bodies[ind].orbit_radius, Solar_system.max_distance])         
                    bodies[ind].radius_vis = max(bodies[ind].radius / Solar_system.radius_scaler, Solar_system.resolution / 100)           

                elif bodies[ind].satellite_of is not None:
                    bodies[ind].pos_xy = np.array([Solar_system.max_distance - bodies[ind].satellite_of.orbit_radius - bodies[ind].orbit_radius, Solar_system.max_distance])
                    bodies[ind].radius_vis = max(bodies[ind].radius / Solar_system.radius_scaler, Solar_system.resolution / 200)

                else:
                    print('Body is not defined properly')

                bodies[ind].pos_xy_vis = bodies[ind].pos_xy / Solar_system.distance_scaler
                bodies[ind].path_vis.append(bodies[ind].pos_xy_vis)
                bodies[ind].path_vis.append(bodies[ind].pos_xy_vis)
        

    @staticmethod
    def initiate_movement(bodies): 
        for body in bodies: 
            if body.satellite_of is None:
                body.vel = body.orb_vel_in
            if body.satellite_of is not None: 
                body.vel = body.satellite_of.orb_vel_in + body.orb_vel_in


    @staticmethod
    def draw_bodies(surface, bodies):
        
        for body in bodies:
            pygame.draw.circle(surface, body.color, body.pos_xy_vis, body.radius_vis)
        

    @staticmethod
    def draw_trajectories(surface, bodies):

        for body in bodies:
            pygame.draw.lines(surface = surface, 
                              color   = body.color,
                              closed  = False, 
                              points  = body.path_vis)
        
    


class Simulation:

    resolution   = None
    max_distance = None  
    pix_to_m     = None         
    

    G_const = 6.67e-11                        # gravitational constant, N*m^2*kg^-2
    
    def __init__(self, window=None, dt=60*60, compute_alg="old", logic_fps=1000):
        """
        :param window: used to define in which window the drawing will occur.If window is None (default) the nothing will be drawn
        :param compute_alg: "vec" or "old" sets the algorith to be used for physics computation. Old is initial alg and vec is the new one
        :param logic_fps: frequency Hz, at which simulation logic will be computed
        """
        self.bodies = []
        self.dt = dt  # dt is in seconds
        self.cur_time = 0
        self.window = window
        if compute_alg == "vec":
            self.compute_physics = self._vec_physics_compute
        elif compute_alg == "old":
            self.compute_physics = self._old_physics_compute
        else:
            raise Exception("Unknown physics engine type")

        self.info = []  # list of tracking info to write
        self.font = pygame.font.Font(None, 20)  # None for default font, 50 is the font size  font = pygame.font.SysFont('Arial', 50)

        self.is_paused = True
        self.is_running = True  # kills multithread if false (redesign the name)

        # multithreading variables
        self.logic_fps = logic_fps
        self.current_time = time.time()
        self.last_logic_update_time = time.time()

    def run_in_thread(self):
        simulatiom_thread = threading.Thread(target=self._thread_run)
        simulatiom_thread.daemon = True  # Ensure the logic thread is killed when the program ends
        simulatiom_thread.start()

    def _thread_run(self):
        while self.is_running:
            self.current_time = time.time()
            elapsed_time = self.current_time - self.last_logic_update_time
            if elapsed_time >= (1 / self.logic_fps):  # Update game logic as fast as possible
                self.step()
                self.last_logic_update_time = self.current_time

    def add_body(self, body=None, bodies=None):
        if body is not None:
            self.bodies.append(body)
        elif bodies is not None:
            self.bodies.extend(bodies)
        else:
            print("Error, body was not provided correctly")

    def _vec_physics_compute(self):
        pass

    def _old_physics_compute(self):
        for ind_1 in range(0, len(self.bodies)):

            d2xd2y_data = np.array([0, 0])

            for ind_2 in range(0, len(self.bodies)):

                if self.bodies[ind_1].name != self.bodies[ind_2].name:

                    pos_diff = self.bodies[ind_1].pos_xy - self.bodies[ind_2].pos_xy  # difference in positions, m
                    distance = np.sqrt(pos_diff[0] ** 2 + pos_diff[1] ** 2)  # distance between objects, m
                    force = Simulation.G_const * self.bodies[ind_1].mass * self.bodies[ind_2].mass / (
                                distance ** 2)  # gravitational force, N

                    # adjusting the sign of the force
                    if self.bodies[ind_1].mass > self.bodies[ind_2].mass:
                        d2dx = force / self.bodies[ind_1].mass * pos_diff[0] / distance
                        d2dy = force / self.bodies[ind_1].mass * pos_diff[1] / distance
                    else:
                        d2dx = -1 * force / self.bodies[ind_1].mass * pos_diff[0] / distance
                        d2dy = -1 * force / self.bodies[ind_1].mass * pos_diff[1] / distance

                    d2xd2y = np.array([d2dx, d2dy])
                    d2xd2y_data = d2xd2y_data + d2xd2y

            self.bodies[ind_1].d2xd2y_int = d2xd2y_data.copy()

        for ind_3 in range(0, len(self.bodies)):
            self.bodies[ind_3].acc = self.bodies[ind_3].d2xd2y_int
            self.bodies[ind_3].update_position(Solar_system.distance_scaler, dt=self.dt)
            #self.bodies[ind_3].draw_path(self.window)

    def step(self):
        if self.is_paused:
            return
        self.compute_physics()
        for body in self.bodies:
            body.track_trajectory()
        self.cur_time += self.dt

    def add_info(self, info: str):
        """
        adds a tracking of a value and puts a text information
        :param info: type of value to be visualized
        Supported info types: "days" - number of days in the simulation
        """

        self.info.append(info)

    def _draw_info(self):
        # TODO add energy texting option
        for i in range(len(self.info)):
            if self.info[i] == "days":
                message = "Days passed: " + str(self.cur_time/60/60/24)
                text = self.font.render(message, True, (0, 0, 0))  # White text
            self.window.blit(text, (10, 20 + 30*i))

    def draw_all(self):
        if self.window is not None:  # if it is none, the visualization is skipped for faster computations
            Solar_system.draw_bodies(self.window, self.bodies)
            Solar_system.draw_trajectories(self.window, self.bodies)
            
            """ for body in self.bodies:
                body.draw(self.window)
                body.draw_path(self.window) """
        self._draw_info()


