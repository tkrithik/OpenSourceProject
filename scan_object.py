import cv2
import datetime
#thres = 0.45 # Threshold to detect object


def scan():
    classNames = []
    classFile = "coco.names"
    with open(classFile,"rt") as f:
        classNames = f.read().rstrip("\n").split("\n")

    configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
    weightsPath = "frozen_inference_graph.pb"

    net = cv2.dnn_DetectionModel(weightsPath,configPath)
    net.setInputSize(320,320)
    net.setInputScale(1.0/ 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)


    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    #cap.set(10,70)

    start_time  = datetime.datetime.now()
    thres = 0.65
    nms = 0.2
    draw = True
    objects = []

    while True:
        success, img = cap.read()

        #result, objectInfo = getObjects(img,0.45,0.2)

        classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
        #print(classIds,bbox)
        if len(objects) == 0: objects = classNames
        objectInfo =[]
        if len(classIds) != 0:
            for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
                className = classNames[classId - 1]
                if className in objects:
                    objectInfo.append([box,className])
                    if (draw):
                        cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                        cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                        cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

        print(objectInfo)
        cv2.imshow("Output",img)
        current_time = datetime.datetime.now()
        time_delta = current_time - start_time
        if time_delta.total_seconds() > 5:
            break
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break

    item = []
    for item_list in objectInfo:
        item.append(item_list[1])

    print(item)
    cap.release()
    cv2.destroyAllWindows()

    return item

if __name__ == "__main__":
    print(scan())
