import numpy as np
from psychopy import visual, core, gui, event
from datetime import datetime
import keyboard
from Oracle import Oracle_switcher
import os

# ---------------------------------------------------------------------------- #
#                                   Switches                                   #
# ---------------------------------------------------------------------------- #
isFullScreen = False


# ---------------------------------------------------------------------------- #
#                        Enter experimental information                        #
# ---------------------------------------------------------------------------- #
info = {
    "Participant-A ID": "",
    "Participant-B ID": "",
    "# Repetitions": 1,
    "date": datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
}

infoDlg = gui.DlgFromDict(
    dictionary=info,
    title="Joint Action Experiment-Rating",
    order=["Participant-A ID", "Participant-B ID", "# Repetitions", "date"],
)

if infoDlg.OK == False:
    core.quit()  # user pressed cancel

# ---------------------------------------------------------------------------- #
#                    Create data folder if it doesn't exist'                   #
# ---------------------------------------------------------------------------- #
if not os.path.exists("data"):
    os.makedirs("data")

# ---------------------------------------------------------------------------- #
#                               create an oracle                               #
# ---------------------------------------------------------------------------- #
oracle = Oracle_switcher(wSize=1)


# ---------------------------------------------------------------------------- #
#                                  Parameters                                  #
# ---------------------------------------------------------------------------- #
## experiment parameters
nRep = info["# Repetitions"]
nTrial = 2
trialTime = 20  # seconds
dr_fill = 5  # change rate: how much time is needed to fill the circle from min to max radius (seconds)

## time bar parameters
barWidth = 0.8

## circle parameters
circle_radius_min = 0.05
circle_radius_max = 0.4

## text parameters
fontSize = 0.05

# ---------------------------------------------------------------------------- #
#                      Create window and stimulus objects                      #
# ---------------------------------------------------------------------------- #
# create a window with aspect ratio 1:1.
win = visual.Window(units="height", size=[800, 800], fullscr=isFullScreen, color="black")

# create a rectangle bar stimulus at the top of the window'
bar = visual.Rect(win, width=barWidth, height=0.05, fillColor="white", pos=[0, 0.45])

# create a centre circle stimulus
circle_c = visual.Circle(win, radius=circle_radius_min, fillColor="black")

# create a circle stimulus
circle = visual.Circle(win, radius=circle_radius_min, fillColor="white")

# create a circle stimulus for maximum radius with only contour
circle_max = visual.Circle(win, radius=circle_radius_max, fillColor=None, lineColor="white")

# create a text stimulus
text_trial = visual.TextStim(win, height=fontSize, pos=[0, 0.25], color="white")

# create two squares on the left and right side of the screen
start_square1 = visual.Rect(win, width=0.1, height=0.1, pos=[-0.25, 0], lineColor="white")
start_square2 = visual.Rect(win, width=0.1, height=0.1, pos=[0.25, 0], lineColor="white")

# ---------------------------------------------------------------------------- #
#                            Prepare data container                            #
# ---------------------------------------------------------------------------- #
data = []


# ---------------------------------------------------------------------------- #
#                                Welcome message                               #
# ---------------------------------------------------------------------------- #
text_welcome = visual.TextStim(win, text="Welcome to the experiment\n\nPress SPACE to continue", height=fontSize)
text_welcome.draw()
win.flip()
keys = event.waitKeys(keyList=["space"])


# ---------------------------------------------------------------------------- #
#                             Start the experiment                             #
# ---------------------------------------------------------------------------- #
for iTrial in range(nTrial):
    # ------------------------------ reset variables ----------------------------- #
    circle.radius = circle_radius_min
    x1s, x2s, ys, ts = [], [], [], []
    acc = False
    rt = None

    # ---------------------------------------------------------------------------- #
    #                             inter-trial interval                             #
    # ---------------------------------------------------------------------------- #
    ## display "Trial #"
    text_trial.text = "Trial {}\nPress both keys to start".format(iTrial + 1)

    while True:
        key1, key2 = False, False

        if keyboard.is_pressed("q"):
            # change square color
            start_square1.fillColor = "green"
            key1 = True
        else:
            # clean square color
            start_square1.fillColor = None

        if keyboard.is_pressed("p"):
            start_square2.fillColor = "green"
            key2 = True
        else:
            # clean square color
            start_square2.fillColor = None

        if keyboard.is_pressed("esc"):
            # terminate the experiment
            win.close()
            core.quit()

        text_trial.draw()
        start_square1.draw()
        start_square2.draw()
        win.flip()

        if key1 and key2:
            core.wait(0.5)
            win.flip()
            break

    core.wait(1)

    # ---------------------------------------------------------------------------- #
    #                             start the next trial                             #
    # ---------------------------------------------------------------------------- #
    # start timer
    t0 = core.getTime()
    t_frame1 = t0
    while True:
        x1, x2 = False, False   

        # ----------------------------- Detect key press ----------------------------- #
        if keyboard.is_pressed("q"):
            x1 = True

        if keyboard.is_pressed("p"):
            x2 = True

        if keyboard.is_pressed("esc"):
            # terminate the experiment
            win.close()
            core.quit()

        # --------------------------- get the current time --------------------------- #
        t = core.getTime() - t0
        
        # -------------------------------- Compute dr -------------------------------- #
        # compute the time elapsed since the last frame
        t_frame2 = core.getTime()
        dt = t_frame2 - t_frame1
        t_frame1 = t_frame2

        # compute dr
        dr = (circle_radius_max - circle_radius_min) / (dr_fill) * dt

        # ---------- change circle radius based on the interaction function ---------- #
        # get current radius
        r = circle.radius

        # get interaction result
        y = oracle.interaction([x1, x2], t, iTrial)

        # change circle radius based on the interaction result
        if y:
            r += dr
        else:
            r -= dr

        if r <= circle_radius_min:
            circle.radius = circle_radius_min
        elif r >= circle_radius_max:
            acc = True
            rt = t
            break
        else:
            circle.radius = r

        # ------------- decerase the bar width based on the time elapsed ------------- #
        bar.width = barWidth - (t) / trialTime * barWidth

        # ----------------------------- update the window ---------------------------- #
        bar.draw()
        circle_max.draw()
        circle.draw()
        circle_c.draw()
        win.flip()

        # --------------------------------- save data -------------------------------- #
        x1s.append(x1)
        x2s.append(x2)
        ys.append(y)
        ts.append(t)

        # check if time is up
        if t >= trialTime:
            break

        # wait for 1 ms
        # core.wait(0.001)

    # ---------------------------------------------------------------------------- #
    #                               save data to file                              #
    # ---------------------------------------------------------------------------- #
    data.append(
        {
            "x1": x1s,
            "x2": x2s,
            "y": ys,
            "t": ts,
            "acc": acc,
            "rt": rt,
        }
    )

    # save data at the end of each trial
    filename = "data/{}_{}_{}.npy".format(info["Participant-A ID"], info["Participant-B ID"], info["date"])
    np.save(filename, data, allow_pickle=True)

    # ------------------------- add inter-trial interval ------------------------- #
    core.wait(1)

# ---------------------------------------------------------------------------- #
#                             End of the experiment                            #
# ---------------------------------------------------------------------------- #
text_end = visual.TextStim(win, text="Thank you", height=fontSize)
text_end.draw()
win.flip()
core.wait(3)
win.close()
core.quit() 