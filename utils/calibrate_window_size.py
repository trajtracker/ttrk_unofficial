#*******************************************************************************************
#
# Calibration script for running TrajTracker in a window that occupies only part of the screen.
#
# The script lets you visually determine the screen boundaries (e.g. to match the size of
# a touchpad that you put on top of the screen). The script's output is the python commands
# that you can use to setup the window size.
#
#*******************************************************************************************


#===========================================================================================
#              Set-up
#===========================================================================================

import expyriment as xpy

import trajtracker as ttrk
import trajtrackerp as ttrkp

xpy.control.defaults.window_mode = False
ttrk.log_to_console = True

# width/height ratio for touchscreen
ratio = 0.7557
# 4 rectangles=one for left,right,top,bottom or three for left, right,top
howmanyrectangles = 3

#===========================================================================================
#              Prepare stimuli
#===========================================================================================

exp = xpy.control.initialize()


def create_stimuli():

    # Set-up rectangle consisting of two colours with an arrow on top and the
    # response square
    square = xpy.stimuli.Rectangle(size=(300, 50), position=(0, 25), colour=(255, 0, 0))
    square1 = xpy.stimuli.Rectangle(size=(300, 50), position=(0, -25), colour=(0, 0, 255))
    arrow = ttrkp.num2pos.DownArrow()
    arrow.decompress()
    arrow.rotate(180)
    response_square = xpy.stimuli.Rectangle(size=(80, 80), position=(0, 0), colour=(0, 255, 0))

    deg = 0
    xpos = [0, -200, 0, 200]
    ypos = [200, 0, -200, 0]

    # -- Create four canvases with rectangles rotated with varying degrees
    if howmanyrectangles not in (3, 4):
        raise Exception("Unsupported config")

    stim_list = []
    for i in range(howmanyrectangles):
        canv = xpy.stimuli.Canvas(size=(300, 100), position=(xpos[i], ypos[i]), colour=[255, 255, 255])
        square.plot(canv)
        square1.plot(canv)
        arrow.plot(canv)
        stim_list.append(canv)
        canv.rotate(deg)
        deg += 90

    # -- Store all stimuli in one container so we can easily show them together
    stim_container = ttrk.stimuli.StimulusContainer()
    [stim_container.add(c, visible=True) for c in stim_list]
    stim_container.add(response_square, visible=True)

    return stim_container, stim_list, response_square


stim_container, stimulus_list, resp_square = create_stimuli()


#===========================================================================================
#              Functions
#===========================================================================================

#----------------------------------------------------------------
# Function to wait until one of the rectangles is clicked. 'exp' are expyriment elements
# such as mouse, 'stim_ls' is the list of all rectangles that can be clicked,
# 'resp_square' contains the response square in the middle of the screen which
# can be clicked to end the calibration
#
def wait_until_shape_clicked(exp, stim_ls, resp_square):

    while True:
        exp.clock.wait(10)
        if exp.mouse.check_button_pressed(0):
            for i in range(howmanyrectangles):
                if stim_ls[i].overlapping_with_position(exp.mouse.position):
                    return i
            if resp_square.overlapping_with_position(exp.mouse.position):
                return -1
        
#----------------------------------------------------------------
# Drag_until_unclicked enables the user to move the shapes around until the
# mouse button is released. 'exp' are all expyriment elements such as the mouse,
# 'canv' is the shape that was clicked and is the one to be dragged.
#
def drag_until_unclicked(exp, canv):

    while exp.mouse.check_button_pressed(0):
        canv.position = exp.mouse.position
        stim_container.present()


#----------------------------------------------------------------
# Positions of all shapes are saved in a csv file. 'stim_ls' contains all canvases.
#
def save_results(stim_ls):
    
    left = stim_ls[1].position[0]
    top = stim_ls[0].position[1]
    right = stim_ls[howmanyrectangles - 1].position[0]

    width = right - left
    height = int(width * ratio)

    with open('virtual_screen_pos.py', 'wb') as myfile:
        myfile.write("window_position = ({:}, {:})\n".format(left, top))
        myfile.write("window_size = ({:}, {:})\n".format(width, height))

    print('The results were saved to the "virtual_screen_pos.py" file')
        
            
#===========================================================================================
#              Run the calibration
#===========================================================================================

#-- Initialize Expyriment
xpy.control.start(exp)
if not xpy.misc.is_android_running():
    exp.mouse.show_cursor()

#-- Infinite while loop to present stimulus at every frame        
while True:    
    stim_container.present()
    stim_number = wait_until_shape_clicked(exp, stimulus_list, resp_square)
    if stim_number>=0:
        drag_until_unclicked(exp, stimulus_list[stim_number])
    else:
        save_results(stimulus_list)
        break
            
        
xpy.io.Keyboard.process_control_keys()

xpy.control.end()
