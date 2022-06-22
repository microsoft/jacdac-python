# Import and initialize the pygame library
from time import sleep
import pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

# Import and initialize the jacdac library
from jacdac.bus import Bus
from jacdac.button import ButtonClient

bus = Bus()
btn = ButtonClient(bus, "button")

# circle radius is our game variable
radius = 100

# increment on button click
def inc_radius(pkt):
    global radius
    radius = radius + 5
btn.on_down(inc_radius)

# Run until the user asks to quit
running = True
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    if radius < 10:
        screen.fill((255, 0, 0))
    else:
        screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), radius)

    # Flip the display
    pygame.display.flip()

    # reduce radius
    radius = max(5, radius - 1)

    # wait a little bit
    sleep(0.04)

# Done! Time to quit.
pygame.quit()