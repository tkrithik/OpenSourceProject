import cv2
import os
import face
print("--- SPACE BAR to capture picture -------")
print('--- ESC key to terminate ---------------')

username = input('please input username---->')


cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0


newpath = './Images/'+username
if not os.path.exists(newpath):
    os.makedirs(newpath)
while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "{}/{}_{}.jpg".format(newpath, username, img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
face.train()