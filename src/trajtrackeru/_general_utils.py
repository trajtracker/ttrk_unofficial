"""

 Copyright (c) 2017 Dror Dotan

This module is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This TrajTracker add-ons module is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with TrajTracker.  If not, see <http://www.gnu.org/licenses/>.
"""

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
        raise ValueError ("Invalid window position ({:}) - expecting x,y coordinates (0,0 = left-top corner of the screen)".
                          format(window_position))

    os.environ['SDL_VIDEO_WINDOW_POS'] = "{:},{:}".format(window_position[0], window_position[1])
