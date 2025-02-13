import mss
import numpy as np
import pygetwindow as gw

class WindowCapture:

    # properties
    hwnd = None

    def __init__(self, window_name=None):

        self.window_name = window_name

        # Find the window by its title
        self.hwnd = gw.getWindowsWithTitle(self.window_name)[0]
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(self.window_name))
        
        # Attempt to bring the window to the foreground
        self.hwnd.activate()

    def get_screenshot(self):

        # Get the window rectangle (left, top, right, bottom)
        bbox = (self.hwnd.left, self.hwnd.top, self.hwnd.right, self.hwnd.bottom)

        with mss.mss() as sct:
            # Capture the specified region
            sct_img = sct.grab(bbox)
            # Convert to a format OpenCV can read
            img = np.array(sct_img)
            return img