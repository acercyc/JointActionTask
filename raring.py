# %%
from psychopy import visual, core, event, gui
from datetime import datetime
import sys  # for exiting the program


# def quitExp():
#     win.close()
#     core.wait(1)
#     core.quit()
#     sys.exit()

# # set up the global key
# event.globalKeys.clear()
# event.globalKeys.add("escape", func=quitExp)

# GUI for participant information
dateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# show infomation dialog
info = {"ParticipantID": "", "# Repetitions": 5, "date": dateTime}
infoDlg = gui.DlgFromDict(
    dictionary=info, title="Joint Action Experiment-Rating", order=["ParticipantID", "# Repetitions", "date"]
)
if infoDlg.OK == False:
    core.quit()  # user pressed cancel

# create a window
win = visual.Window(size=[800, 800], fullscr=False, color=[-1, -1, -1], units="height")

# create visual stimuli
text_trial = visual.TextStim(win, text="Trial #", pos=[0, 0.45], color=[1, 1, 1], height=0.05)
q1 = visual.TextStim(
    win, text="How much control do you think you have over the target?", pos=[0, 0.35], color=[1, 1, 1], height=0.03
)
slider1 = visual.Slider(win, pos=(0, 0.2), size=(0.5, 0.05), labels=["0", "10"], granularity=0, ticks=[0, 5, 10])

q2 = visual.TextStim(
    win, text="How much do you think you contribute to the current result?", pos=[0, 0.05], color=[1, 1, 1], height=0.03
)


slider2 = visual.Slider(win, pos=(0, 0), size=(0.5, -0.05), labels=["0", "10"], granularity=0, ticks=[0, 5, 10])

q3 = visual.TextStim(
    win,
    text="How much do you think your partner's contribute to the current result?",
    pos=[0, -0.1],
    color=[1, 1, 1],
    height=0.03,
)


slider3 = visual.Slider(win, pos=(0, -0.2), size=(0.5, 0.05), labels=["0", "10"], granularity=0, ticks=[0, 5, 10])
button_text = visual.TextStim(win, text="Okay", pos=[0, -0.4], height=0.05)

# create a mouse object
mouse = event.Mouse()


for trial in range(5):  # Assuming 5 trials
    text_trial.text = "Trial {}".format(trial + 1)

    # reset the sliders
    slider1.reset()
    slider2.reset()
    slider3.reset()
    slider_values = [None, None, None]

    while True:
        text_trial.draw()
        q1.draw()
        q2.draw()
        q3.draw()
        slider1.draw()
        slider2.draw()
        slider3.draw()
        button_text.draw()
        win.flip()

        # get slider values
        slider_values = [slider1.getRating(), slider2.getRating(), slider3.getRating()]

        # check if slider values are all filled
        isSliderFilled = all([x is not None for x in slider_values])

        # get mouse position
        mouse_pos = mouse.getPos()

        # detect if mouse cursor is inside the button_text
        if button_text.contains(mouse_pos) and isSliderFilled:
            button_text.color = [0, 1, 0]  # Change color to green
        else:
            button_text.color = [1, 1, 1]

        if mouse.isPressedIn(button_text) and isSliderFilled:
            break  # Exit the while loop to move to the next trial

    # clean the screen
    win.flip()

    # wait for 1 second
    core.wait(1)
win.close()
core.quit()
# %%
