import numpy as np
import pygame
import sys
from simulation import Body
from simulation import Solar_system
from simulation import Simulation

import time

# Initialize Pygame
pygame.init()

# Set up the displachat
width, height = 800, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Solar system')

center_x_vis = width/2
center_y_vis = height/2

# Define instances of planets
bodies = [
    Body(      name       = 'Sun', 
               color        = (252, 229, 112), 
               radius       = 696e6,                       
               mass         = 2e30, 
               orb_vel_in   = np.array([0,0]),
               satellite_of = None, 
               orbit_radius = None),
    
    Body(      name         = 'Venus', 
               color        = (255, 198, 73), 
               radius       = 6.05e6,        
               mass         = 4.57e24,                        
               orb_vel_in   = np.array([0, 35.02e3]),
               satellite_of = None,
               orbit_radius = 108e9),

    Body(      name         ='Mercury', 
               color        = (183, 184, 185), 
               radius       = 2.44e6,       
               mass         = 3.3e23,
               orb_vel_in   = np.array([0,47.36e3]),
               satellite_of = None, 
               orbit_radius = 58e9),

    Body(      name         = 'Earth', 
               color        = (0,94,184), 
               radius       = 6.371e6,       
               mass         = 5.97e24,
               orb_vel_in   = np.array([0,29.8e3]),
               satellite_of = None, 
               orbit_radius = 1.5e11),

    Body(      name         = 'Mars', 
               color        = (156, 46, 53), 
               radius       = 3.4e6,       
               mass         = 6.42e23,
               orb_vel_in   = np.array([0,24.08e3]),
               satellite_of = None, 
               orbit_radius = 228e9),
]


# Define instances of satellites
bodies.extend([
    Body(      name         = 'Moon', 
               color        = (246, 241, 213), 
               radius       = 1737e3,       
               mass         = 7.35e22,
               orb_vel_in   = np.array([0,1.022e3]), 
               satellite_of = next((body for body in bodies if body.name == "Earth"), None),
               orbit_radius = 384.4e6),

    Body(      name         = 'Phobos', 
               color        = (0, 0, 0),                
               radius       = 11.1e3,       
               mass         = 1.06e16,
               orb_vel_in   = np.array([0,2.14e3]),                
               satellite_of = next((body for body in bodies if body.name == "Mars"), None),
               orbit_radius = 9.6e6),

    Body(      name         = 'Deimos', 
               color        = (158,143,179), 
               radius       = 6.2e3,       
               mass         = 1.5e15,
               orb_vel_in   = np.array([0,1.35e3]), 
               satellite_of = next((body for body in bodies if body.name == "Mars"), None),
               orbit_radius = 23.46e6)
               
])


Solar_system.initiate_system(width, height, bodies)
simulation = Simulation(window=window)

simulation.add_body(bodies=bodies)
simulation.add_info("days")

# Initialize the clock
clock = pygame.time.Clock()
fps = 30          # fps set to hours


def main_loop():
    button_pressed = None
    running = True

    simulation.run_in_thread()  # runs the game logic in a separate thread
    # use simulation.logic_fps = 100 # to change computation frequency
    simulation.logic_fps = 1000

    while running:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE: # If space bar gets pressed --> rotation is initiated
                    print("space is released")
                    if button_pressed is None:
                        button_pressed = False
                        Solar_system.initiate_movement(bodies)
                    else:
                        button_pressed = not button_pressed
                    simulation.is_paused = button_pressed

        # drawing section:
        window.fill((255, 255, 255))  # Clear the screen
        simulation.draw_all()

        # Flip the display
        pygame.display.flip()

        # Control the framerate
        clock.tick(fps)


main_loop()
# Quit Pygame
pygame.quit()
sys.exit()





