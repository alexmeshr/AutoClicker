import mouse
import time

def clicked():
    x, y = mouse.get_position()
    print(f"Clicked on ({x}, {y})")


def exit_click():
    exit()


mouse.on_click(clicked)
#mouse.on_right_click(exit_click())
i=0
while True:
    time.sleep(0.1)
