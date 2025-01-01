import pygame
import numpy as np


# Define Body class
class Body: 


    def __init__(self, name, color, radius, mass, pos_xy_vis, pos_xy, dxdy, d2xd2y, d2xd2y_int, path_vis):
        self.name        = name
        self.color       = color
        self.radius      = radius           # radius in kilometers
        self.mass        = mass             # mass in kg 
        self.pos_xy_vis  = pos_xy_vis       # position in pixels 
        self.pos_xy      = pos_xy           # position in meters
        self.dxdy        = dxdy             # velocity in kilometers per second
        self.d2xd2y      = d2xd2y           # acceleration in kilometers^2 per second  
        self.d2xd2y_int  = d2xd2y_int       # placeholder to store results of the intermediate calculations
        self.path_vis    = path_vis
        

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos_xy_vis, self.radius)


    def update_position(self, pix_to_m, dt):
        self.dxdy       = self.dxdy + self.d2xd2y*dt
        self.pos_xy     = self.pos_xy + self.dxdy*dt
        self.pos_xy_vis = self.pos_xy_vis + self.dxdy*dt/pix_to_m


    def draw_path(self, surface):
        self.path_vis.append((self.pos_xy_vis[0],self.pos_xy_vis[1])) 

        pygame.draw.lines(surface = surface, 
                          color = self.color,
                          closed = False, 
                          points = self.path_vis) 


class Simulation:

    width = None
    max_distance = None  
    pix_to_m = None         

    @staticmethod
    def init_static_params(width):
        Simulation.width = width
        Simulation.max_distance = 228e9                            # maximum distance (Mars to SUn) in meters
        Simulation.max_distance = 1.1*Simulation.max_distance                 # maximum distance in meters
        Simulation.pix_to_m = Simulation.max_distance/(Simulation.width/2)           # conversion of pixels to km
        

    G_const = 6.67e-11                        # gravitational constant, N*m^2*kg^-2
    
    def __init__(self, window=None, dt=60*60*24):
        self.bodies = []
        self.dt = dt  # dt is in seconds
        self.cur_time = 0
        self.window = window

    def add_body(self, body=None, bodies=None):
        if not (body is None):
            self.bodies.append(body)
        elif not (bodies is None):
            self.bodies.extend(bodies)
        else:
            print("Error, body was not provided correctly")


    def step(self):
        for ind_1 in range(0,len(self.bodies)): 

            d2xd2y_data = np.array([0,0])

            for ind_2 in range(0,len(self.bodies)):

                if self.bodies[ind_1].name != self.bodies[ind_2].name: 

                    pos_diff    = self.bodies[ind_1].pos_xy - self.bodies[ind_2].pos_xy                   # difference in positions, m
                    distance    = np.sqrt(pos_diff[0]**2 + pos_diff[1]**2)                      # distance between objects, m
                    force       = Simulation.G_const*self.bodies[ind_1].mass*self.bodies[ind_2].mass/(distance**2)   # gravitational force, N 
                    
                    # adjusting the sign of the force
                    if self.bodies[ind_1].mass > self.bodies[ind_2].mass: 
                        d2dx          = force/self.bodies[ind_1].mass*pos_diff[0]/distance
                        d2dy          = force/self.bodies[ind_1].mass*pos_diff[1]/distance    
                    else:
                        d2dx          = -1*force/self.bodies[ind_1].mass*pos_diff[0]/distance
                        d2dy          = -1*force/self.bodies[ind_1].mass*pos_diff[1]/distance    
                        
                    d2xd2y        = np.array([d2dx,d2dy])                    
                    d2xd2y_data   = d2xd2y_data + d2xd2y

            self.bodies[ind_1].d2xd2y_int = d2xd2y_data.copy()

        for ind_3 in range(0,len(self.bodies)):
            
            self.bodies[ind_3].d2xd2y = self.bodies[ind_3].d2xd2y_int
            self.bodies[ind_3].update_position(Simulation.pix_to_m, dt=self.dt)    
            self.bodies[ind_3].draw_path(self.window)

        self.cur_time += self.dt


    def draw_all(self):
        for body in self.bodies:
            body.draw(self.window)
            body.draw_path(self.window)
