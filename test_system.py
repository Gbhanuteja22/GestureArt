import cv2
import numpy as np
import sys
def check():
    print("running system check for gestureart...")
    print("-" * 50)
    try:
        import mediapipe
        import tensorflow
        print("opencv version:", cv2.__version__)
        print("mediapipe version:", mediapipe.__version__)
        print("numpy version:", np.__version__)
        print("tensorflow version:", tensorflow.__version__)
    except Exception as error:
        print("problem with required libraries:", error)
        return False
    try:
        camera = cv2.VideoCapture(0)
        success, frame = camera.read()
        camera.release()
        if not success:
            print("could not access camera.")
            return False
    except Exception as error:
        print("camera error:", error)
        return False
    print("✓ everything looks good")
    return True
if __name__ == "__main__":
    passed = check()
    print("-" * 50)
    if passed:
        print("all tests passed! you can now run gestureart.")
    else:
        print("some checks failed. please check the messages above.")
    sys.exit(0 if passed else 1)
