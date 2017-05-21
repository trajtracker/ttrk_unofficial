
import os


#-------------------------------------------------
def set_default_window_position(window_position):
    """
    When working in window mode - use this to set the position of the window to open.
    Call this method before you call trajtracker.initialize() 

    :param window_position: (x,y) 
    """

    if len(window_position) != 2 or \
            not isinstance(window_position[0], int) or \
            not isinstance(window_position[1], int):
        raise ValueError ("Invalid window position ({:}) - expecting x,y coordinates (0,0 = top left)".
                          format(window_position))

    os.environ['SDL_VIDEO_WINDOW_POS'] = "{:},{:}".format(window_position[0], window_position[1])
