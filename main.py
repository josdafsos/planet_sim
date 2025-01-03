import pygame
import sys
from simulation import Body
from simulation import Simulation
import body_system

# Initialize Pygame
pygame.init()

# Set up the displachat
width, height = 700, 700
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Solar system')

          


Simulation.init_static_params(width, height)
Body.init_static_properties(width)
simulation = Simulation(window=window,
                        compute_alg="old",  # use "old" for the initial algorithm
                        init_func=body_system.create_solar_system)
#simulation = Simulation(window=window, init_func=body_system.create_three_body_system)


#simulation.add_body(bodies=bodies)
simulation.add_info("days")

# Initialize the clock
clock = pygame.time.Clock()
fps = 30          # fps set to hours


def main_loop():
    button_pressed = None
    running = True

    simulation.reset()
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
                    else:
                        button_pressed = not button_pressed
                    simulation.is_paused = button_pressed

        # drawing section:
        window.fill((0, 0, 0))  # Clear the screen
        simulation.render()
        pygame.display.flip()  # Flip the display
        clock.tick(fps)  # Control the framerate


main_loop()
# Quit Pygame
pygame.quit()
sys.exit()





