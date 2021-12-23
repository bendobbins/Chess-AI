import pygame

# Window constants
WIDTH = 650
HEIGHT = 700
BOXSIZE = 75
FIELDSIZE = 8
MARGIN = 25

# Window
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

def draw_text(widths, heights, phrases, fonttypes, fontcolor):
    """
    Given information about text boxes to be drawn, this draws the text into the window.

    widths -- List of integer x-axis placements in the window (one for each piece of text)
    heights -- List of integer y-axis placements in the window (one for each piece of text)
    phrases -- List of strings that are the text to be displayed
    fonttypes -- List of fonts (one for each piece of text)
    fontcolor -- RGB tuple of the foreground color of the text
    """
    for i in range(len(phrases)):
        text = fonttypes[i].render(phrases[i], True, fontcolor)
        textRect = text.get_rect()
        textRect.center = (widths[i], heights[i])
        DISPLAY.blit(text, textRect)

def get_box_placement(x, y):
    """
    Finds and returns the window coordinates for box (x, y) in the grid.
    """
    left = MARGIN + BOXSIZE * x 
    top = MARGIN + BOXSIZE * y
    return left, top


def select_square(mouse):
    """
    Given the position of a mouse click, return a tuple of the square on the grid that was clicked, or None if no square was clicked.
    """
    for box_x in range(FIELDSIZE):
        for box_y in range(FIELDSIZE):
            left, top = get_box_placement(box_x, box_y)
            box = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if box.collidepoint(mouse):
                return (box_x, box_y)
    return None