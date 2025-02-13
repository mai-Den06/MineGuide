import cv2
from dotenv import load_dotenv
import time
import tkinter as tk

from config.setting import WINDOW_NAME
from modules.guide_manager import generate_description
from modules.overlay import OverlayInfo
from modules.prediction import pred
from modules.preprocessing import image_preprocessing
from modules.window_capture import WindowCapture

load_dotenv()

def main():
    """ Initialize """
    # window capture
    try:
        wincap = WindowCapture(WINDOW_NAME)
    except Exception as e:
        print(f'Error: {e}')

    # object detection
    last_time = time.time()
    object_names = []
    previous_object_names = []

    # overlay
    root = tk.Tk()
    root.withdraw()
    object_name = ["SAMPLE"]
    description = ["Sample text\nサンプルテキスト"]
    overlay = OverlayInfo(root, object_name, description)
    overlay.geometry('+1920+300')
    class_colors = {
        "coal_ore": (128, 128, 128),
        "copper_ore": (70, 97, 189),
        "lapis_lazuli_ore": (192, 115, 80),
        "iron_ore": (144, 173, 213),
        "gold_ore": (36, 193, 240),
        "redstone_ore": (1, 1, 237),
        "diamond_ore": (214, 215, 49),
        "emerald_ore": (100, 220, 44)
    }

    # main loop
    while True:
        # get screenshot
        screenshot = wincap.get_screenshot()

        # pretreatment
        screenshot = image_preprocessing(screenshot)

        # object detection
        result = pred(screenshot)

        if result.boxes is not None and len(result.boxes) > 0:
            class_indices = result.boxes.cls.cpu().numpy().astype(int)
            object_names = list(set([result.names[idx] for idx in class_indices]))
        
        # display boxes and labels
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = box.conf[0].item()
            object_name = result.names[box.cls[0].item()]

            label = f"{object_name}: {confidence:.2f}"

            default_color = (240, 240, 240)
            color = class_colors.get(object_name, default_color)

            cv2.rectangle(screenshot, (x1, y1), (x2, y2), color, 4)
            cv2.putText(screenshot, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, default_color, 2)

        if time.time() - last_time >= 1:

            # display description on overlay
            if len(object_names) > 0 and object_names != previous_object_names:
                print(object_names)

                descriptions = []
                for obj in object_names:
                    descriptions.append(generate_description(obj))
                overlay.update_overlay(object_names, descriptions)
            
                previous_object_names = object_names
            
            # update time
            last_time = time.time()

        # display boxes and labels
        # cv2.imshow('Computer Vision', screenshot)

        root.update()

        if overlay.stop_flag:
            break
        
        # Press "q" to quit
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break

    print('Done.')

if __name__ == "__main__":
    main()