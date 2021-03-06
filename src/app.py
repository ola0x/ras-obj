import cv2
from PIL import Image
import numpy as np
import os

from const import CLASSES, COLORS
from settings import DEFAULT_CONFIDENCE_THRESHOLD, DEMO_IMAGE, MODEL, PROTOTXT

def process_image(image):
    blob = cv2.dnn.blobFromImage(
        cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5
    )
    net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
    net.setInput(blob)
    detections = net.forward()
    return detections

def annotate_image(
    image, detections, confidence_threshold=DEFAULT_CONFIDENCE_THRESHOLD
):
    # loop over the detections
    (h, w) = image.shape[:2]
    labels = []
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        idx = int(detections[0, 0, i, 1])

        if confidence > confidence_threshold and CLASSES[idx] == "person":
            # extract the index of the class label from the `detections`,
            # then compute the (x, y)-coordinates of the bounding box for
            # the object
            
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # display the prediction
            label = f"{CLASSES[idx]}: {round(confidence * 100, 2)}%"
            labels.append(label)
            cv2.rectangle(image, (startX, startY), (endX, endY), COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(
                image, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2
            )
    return image, labels

# image = np.array(Image.open(DEMO_IMAGE))
# detections = process_image(image)
# image, labels = annotate_image(image, detections, DEFAULT_CONFIDENCE_THRESHOLD)
# img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# cv2.imwrite("sample.jpg", img)

## WebCam
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

while True:

    # Read the frames
    ret_val, img = cam.read()
    
    #Flip Image
    img = cv2.flip(img, 1)

    #Predict Frames
    detections = process_image(img)
    img, labels = annotate_image(img, detections, DEFAULT_CONFIDENCE_THRESHOLD)

    # Display Predictions
    cv2.imshow('cam', img)
    
    if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1)==27): 
        break  # esc to quit

#Close Camera
cam.release()
cv2.destroyAllWindows()