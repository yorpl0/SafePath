import threading
import time
from keras.layers import Dense, AveragePooling2D,Flatten, Dropout
from keras.optimizers import Adam
from keras.applications.resnet import ResNet50, preprocess_input
from keras.models import Model
import cv2,numpy as np
import requests as rq
from ultralytics import YOLO

boxer = YOLO('yolov8x.pt')

URL = 'localhost:5000/upd'
sex_ratio = None
categories = ['Male', 'Female']
st = 2
def resnet50_modelarch():   
    lr = 1e-5
    epochs = 10 
    basemodel= ResNet50(include_top=False, input_shape=(200,100,3))
    headmodel= basemodel.output
    headmodel= AveragePooling2D(pool_size=(3,3))(headmodel)
    headmodel = Flatten(name="flatten")(headmodel)
    headmodel = Dense(512, activation="relu")(headmodel)
    headmodel = Dropout(0.3)(headmodel)
    headmodel = Dense(256, activation="relu")(headmodel)
    headmodel = Dropout(0.3)(headmodel)
    headmodel = Dense(128, activation="relu")(headmodel)
    headmodel = Dropout(0.3)(headmodel)
    headmodel = Dense(64, activation="relu")(headmodel)
    headmodel = Dense(2, activation='softmax')(headmodel)
    model=Model(inputs=basemodel.input, outputs=headmodel)
    
    for layer in basemodel.layers:
        layer.trainable=False
        
    opt=Adam(learning_rate=lr, weight_decay=lr / epochs)
    model.compile(loss="binary_crossentropy",optimizer=opt,metrics=["accuracy"])    
    return model

model = resnet50_modelarch()
model.summary()

model.load_weights("model_weights.h5")

CLASSES = ['Male','Female']

def pred(img_arr):
    for i in range(len(img_arr)):
        img_arr[i] = cv2.resize(img_arr[i], (100, 200))
    y = model.predict(np.asarray(img_arr))    
    ans = [CLASSES[np.argmax(x)] for x in y]
    men = ans.count('Male')
    women = ans.count('Female')
    global sex_ratio
    if sex_ratio == None or women == 0 or men / women != sex_ratio:
        if women == 0: 
            sex_ratio = 0
        else:
            sex_ratio = men / women
    print("Sex Ratio: ", sex_ratio)
    return sex_ratio , [CLASSES[np.argmax(x)] for x in y]

sos = 0

# Function to send HTTP requests
def send_request():
    global sos,st
    while True:
        try:
            # Example payload (customize as needed)
            payload = {'sos': sos}
            print('sent : ' + str(sos))
            response = rq.post('http://localhost:5000/upd', json=payload)
            if sos: 
                st = 5
                sos = 0
            print(f"Request sent, status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        # Wait for a specified interval before sending the next request
        time.sleep(st)  # Adjust the interval as needed

# Start sending requests in a separate thread
request_thread = threading.Thread(target=send_request, daemon=True)
request_thread.start()

def pred_vid(path):
    global sos
    cap = cv2.VideoCapture(path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Ignoring empty camera frame.")
            continue
        res = boxer.predict(frame,classes=0)
        a = []
        loc = {}
        for result in res:
            for i,box in enumerate(result.boxes):# Extract bounding box coordinates
                x_min, y_min, x_max, y_max = box.xyxy[0].tolist()  # Get bounding box as [x_min, y_min, x_max, y_max]
                x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)  # Convert to integers
                loc[i] = (x_min, y_min, x_max, y_max)
                # Crop the region of interest
                img = frame[y_min:y_max, x_min:x_max]
                a.append(img)
        sr, x = pred(a)
        # Draw BB Green for male , red for female
        for i in range(len(loc)):
            x_min, y_min, x_max, y_max = loc[i]
            color = (0, 255, 0) if x[i] == "Male" else (0, 0, 255)
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 2)
            cv2.putText(frame, x[i], (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                
        if sr > 1:
            print('Danger!')
            sos = 1
        cv2.imshow('Footage', frame)
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    
pred_vid('test.mp4')