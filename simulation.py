import pygame
import numpy as np
from collections import deque
import time
import threading
from scipy.spatial.distance import cdist
import gymnasium as gym

# Define Body class
class Body: 

    def __init__(self, name, color, radius, mass, orbit_radius = None, orb_vel_in = None, init_func = None):
        self.name           = name
        self.color          = color
        self.radius         = radius                        # radius in kilometers
        self.mass           = mass                          # mass in kg
        self.orbit_radius   = orbit_radius
        self.orb_vel_in     = orb_vel_in

        self.acc            = np.array([0,0])               # acceleration in kilometers^2 per second
        self.vel            = np.array([0,0])               # orbital velocity of a body at in meters per second
        self.pos_xy         = None                          # position in meters
        self.pos_xy_vis     = None                          # position in pixels (for visualization)
        self.radius_vis     = None                          # radius in pixels (for visualization)
        self.path_vis       = deque(maxlen=1000)            # visualizaed trajectory of the body in pixels (for visualization)

        

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos_xy_vis, self.radius_vis)

    def update_position(self, pix_to_m, dt):
        self.vel       = self.vel + self.acc * dt
        self.pos_xy     = self.pos_xy + self.vel * dt
        self.pos_xy_vis = self.pos_xy_vis + self.vel * dt / pix_to_m

    def track_trajectory(self):
        self.path_vis.append((self.pos_xy_vis[0], self.pos_xy_vis[1]))

    def draw_path(self, surface):
        self.path_vis.append((self.pos_xy_vis[0], self.pos_xy_vis[1]))
        pygame.draw.lines(surface = surface,
                          color = self.color,
                          closed = False, 
                          points = self.path_vis) 


class Simulation(gym.Env):

    width = None
    height = None
    distance_scaler = None
    G_const = 6.67e-11  # gravitational constant, N*m^2*kg^-2

    @staticmethod
    def init_static_params(width, height):
        Simulation.width = width
        Simulation.height = height

    def __init__(self,
                 window=None,
                 dt=60*60*24,
                 compute_alg="old",
                 solver="newton",
                 logic_fps=1000,
                 init_func=None):
        """
        :param window: used to define in which window the drawing will occur.If window is None (default) the nothing will be drawn
        :param compute_alg: "vec" or "old" sets the algorith to be used for physics computation. Old is initial alg and vec is the new one
        :param logic_fps: frequency Hz, at which simulation logic will be computed
        """
        self.bodies = []
        self.dt = dt  # dt is in seconds
        self.cur_time = 0
        self.window = window
        if solver == "newton":  # type of differential equation diff_equation_solver
            self.diff_equation_solver = self._newton_diff_solver


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
        self.init_func = init_func  # function used to generate bodies on reset
        self.mass_vec = None
        self.pos_vec = None
        self.vel_vec = None
        self.acc_vec = None

    def run_in_thread(self):
        simulatiom_thread = threading.Thread(target=self._thread_run)
        simulatiom_thread.daemon = True  # Ensure the logic thread is killed when the program ends
        simulatiom_thread.start()

    def _parse_body_to_vec(self, body):
        if self.mass_vec is None:
            self.mass_vec = np.array([[body.mass]])
            self.pos_vec = body.pos_xy  # position in meters
            self.vel_vec = body.vel  # velocity in kilometers per second
            self.acc_vec = body.acc
        else:
            self.mass_vec = np.vstack((self.mass_vec, [body.mass]))
            self.pos_vec = np.vstack((self.pos_vec, body.pos_xy))  # position in meters
            self.vel_vec = np.vstack((self.vel_vec, body.vel))  # velocity in kilometers per second
            self.acc_vec = np.vstack((self.acc_vec, body.acc))

    def reset(self):
        self.bodies = []
        self.mass_vec = None
        self.pos_vec = None
        self.vel_vec = None
        self.acc_vec = None

        self.cur_time = 0
        self.is_paused = True
        self.is_running = True  # kills multithread if false (redesign the name)

        if self.init_func is not None:
            self.bodies, Simulation.distance_scaler = self.init_func(Simulation.width, Simulation.height)
        for body in self.bodies:
            self._parse_body_to_vec(body)

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
            self._parse_body_to_vec(body)
        elif bodies is not None:
            self.bodies.extend(bodies)
            for body in bodies:
                self._parse_body_to_vec(body)
        else:
            print("Error, body was not provided correctly")

    def _vec_physics_compute(self):

        # Compute squared distances directly
        distances = cdist(self.pos_vec, self.pos_vec, 'sqeuclidean')
        cube_distances = distances**3

        # Compute the inverse square distances
        # If the distance is zero, inverse sqrt is set to zero
        inverse_cube_distances = np.where(np.abs(cube_distances) > 1e-3, 1 / cube_distances, 0)
        g_inverse_cube_distance = inverse_cube_distances * Simulation.G_const
        #print(inverse_square_distances)
        # mass_mat = np.matmul(self.mass_vec, np.transpose(self.mass_vec))
        # gravity_force_mat = np.matmul(mass_mat, inverse_square_distances) * Simulation.G_const

        # getting direction of the force, not yet normalized. Also possible to compute a single matrix
        # single matrix: directions = points[np.newaxis, :, :] - points[:, np.newaxis, :]
        x_diff_matrix = self.pos_vec[:, 0][np.newaxis, :] - self.pos_vec[:, 0][:, np.newaxis]
        y_diff_matrix = self.pos_vec[:, 1][np.newaxis, :] - self.pos_vec[:, 1][:, np.newaxis]

        x_no_mass_acc = np.multiply(x_diff_matrix, g_inverse_cube_distance)
        y_no_mass_acc = np.multiply(y_diff_matrix, g_inverse_cube_distance)

        x_acc_vec = np.transpose(np.matmul(np.transpose(self.mass_vec), x_no_mass_acc))
        y_acc_vec = np.transpose(np.matmul(np.transpose(self.mass_vec), y_no_mass_acc))
        self.acc_vec = np.hstack((x_acc_vec, y_acc_vec))

    def _newton_diff_solver(self):
        self.vel_vec = self.acc_vec * self.dt
        self.pos_vec = self.vel_vec * self.dt

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

            self.bodies[ind_3].vel        = self.bodies[ind_3].vel + self.bodies[ind_3].acc * self.dt
            self.bodies[ind_3].pos_xy     = self.bodies[ind_3].pos_xy + self.bodies[ind_3].vel * self.dt


    def step(self):
        if self.is_paused:
            return
        self.compute_physics()
        self.diff_equation_solver()
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
                text = self.font.render(message, True, (255, 255, 255))  # White text
            self.window.blit(text, (10, 20 + 30*i))

    def render(self):  # function to visualize the simulation, name
        if self.window is not None:  # if it is none, the visualization is skipped for faster computations
            for body in self.bodies:

                body.pos_xy_vis = body.pos_xy / Simulation.distance_scaler

                body.draw(self.window)
                body.draw_path(self.window)
        self._draw_info()

    def close(self):  # used in gym environment for RL training
        pass


