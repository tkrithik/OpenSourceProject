import face_recognition
import cv2
import numpy as np
import time
import pickle
def detect():
    video_capture = cv2.VideoCapture(1)
    video_capture.read()
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    names = []
    try:
        data = pickle.loads(open('face_enc', "rb").read())
    except:
        print("No data")
        return "n"
    start_time = time.time()
    while True and (time.time() - start_time) < 3:
        fps_time = time.time()
        ret, frame = video_capture.read()
        fast_frame = cv2.resize(frame, (0, 0), fx= 0.25, fy=0.25)
        #rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(fast_frame)
        face_encodings = face_recognition.face_encodings(fast_frame, face_locations, model="cnn")
        #names = []
        for (top, right, bottom, left), face_encodings in zip(face_locations, face_encodings):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            #matches = face_recognition.compare_faces(known_face_encodings, face_encodings)
            name = "Unknown"
            face_distances = face_recognition.face_distance(data["encodings"], face_encodings)
            #print(face_distances)
            min_recognize = face_distances.min()
            if min_recognize < 0.41:
                best_match_index = np.argmin(face_distances)
                #print(best_match_index)
                name = data["names"][best_match_index]
                names.append(name)
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom + 25), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_COMPLEX_SMALL
            cv2.putText (frame, name, (left + 6, bottom - 6), font, 0.7, (255, 255, 255), 1)
            cv2.putText (frame, str(round(min_recognize, 4)), (right - 6, top - 6), font, 0.7, (255, 255, 255), 1)
        #print(names)
        cv2.imshow('Video', frame)
        #print("FPS ", 1.0 / (time.time() - fps_time))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    #print(names)
    return (max(set(names), key=names.count))


if __name__ == "__main__":
    print(detect())