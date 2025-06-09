import cv2



def wideo():
    cam=cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2000)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 2000)
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    fps = 20.0
    widht = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter("lallal.avi", fourcc, fps ,(widht,height))
    while True:
        red, frame =cam.read()


        if red :
            cv2.imshow("Koolac", frame)
            out.write(frame)
            key = cv2.waitKey(1)
        if key == ord("q"):
            break
    cam.release()
    out.release()
    cv2.destroyAllWindows()
wideo()