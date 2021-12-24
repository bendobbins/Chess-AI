import pygame

# Window constants
WIDTH = 650
HEIGHT = 700
BOXSIZE = 75
FIELDSIZE = 8
MARGIN = 25

WHITE = (255, 255, 255)
LIGHTGREY = (225, 225, 225)
BLACK = (0, 0, 0)
LARGEFONT = pygame.font.SysFont("Helvetica", 30)
SMALLFONT = pygame.font.SysFont("Courier", 13)

BUTTONFONT = pygame.font.SysFont("Courier", 16)

# Window
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

def start_page():
    """
    Displays the introductory page where difficulty is chosen and returns hitboxes for difficulty buttons.
    """
    # Draw start page text
    textPlacementX = [WIDTH / 2, WIDTH / 2]
    textPlacementY = [HEIGHT / 2 - 200, HEIGHT / 2 - 100]
    phrases = ["CHESS", "Choose how you want to play"]
    fonts = [LARGEFONT, SMALLFONT]
    draw_text(textPlacementX, textPlacementY, phrases, fonts, WHITE)

    # Draw difficulty buttons
    buttonPlacementX = [WIDTH / 3 - 40, (WIDTH / 3) * 2 - 40]
    buttonPlacementY = [HEIGHT / 2, HEIGHT / 2]
    buttonWidths = 110
    buttonHeights = 50
    phrases = ["By Myself", "Against AI"]
    buttons = draw_buttons(buttonPlacementX, buttonPlacementY, buttonWidths, buttonHeights, phrases, LIGHTGREY, BLACK)

    return buttons


def draw_text(widths, heights, phrases, fonttypes, fontcolor):
    """
    Given information about text boxes to be drawn, this draws the text into the window.

    widths -- List of integer x-axis placements in the window (one for each piece of text)\n
    heights -- List of integer y-axis placements in the window (one for each piece of text)\n
    phrases -- List of strings that are the text to be displayed\n
    fonttypes -- List of fonts, one for each phrase\n
    fontcolor -- RGB tuple of the foreground color of the text\n
    """
    for i in range(len(phrases)):
        text = fonttypes[i].render(phrases[i], True, fontcolor)
        textRect = text.get_rect()
        textRect.center = (widths[i], heights[i])
        DISPLAY.blit(text, textRect)


def draw_buttons(widths, heights, boxwidth, boxheight, phrases, boxcolor, fontcolor):
    """
    Given information about a series of buttons to be built, draw those buttons and return their hitboxes.

    widths -- List of integer x-axis placements in the window (one for each button)\n
    heights -- List of integer y-axis placements in the window (one for each button)\n
    boxwidth -- Integer for the width of each button to be drawn\n
    boxheight -- Integer for the height of each button to be drawn\n
    phrases -- List of strings that are the text that will go into each button\n
    boxcolor -- RGB tuple of the background color for each button\n
    fontcolor -- RGB tuple of the foreground color for each button\n
    """
    buttons = []
    for i in range(len(phrases)):
        button = pygame.Rect(widths[i], heights[i], boxwidth, boxheight)
        text = BUTTONFONT.render(phrases[i], True, fontcolor)
        rect = text.get_rect()
        rect.center = button.center
        pygame.draw.rect(DISPLAY, boxcolor, button)
        DISPLAY.blit(text, rect)
        buttons.append(button)

    return buttons


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