import cv2
import numpy as np
from tensorflow.keras.models import load_model

classifier = load_model('ASLModel.h5')  # loading the model
roiLeftTop = (530, 100)
roiRightBottom = (750, 300)


def hand_detection(frame):
    # Chuyển đổi frame sang không gian màu HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Xác định phạm vi màu của bàn tay trong không gian màu HSV
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    # Tìm các điểm ảnh thuộc về màu da
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Tìm contours trong mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Xác định bounding box của bàn tay
    bounding_box = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:  # Chọn ngưỡng diện tích tùy thuộc vào kích thước của ảnh
            x, y, w, h = cv2.boundingRect(contour)
            bounding_box = [(x, y), (x + w, y + h)]
            break

    return bounding_box

def fileSearch():
    fileEntry = []
    for file in os.listdir("SampleGestures"):
        if file.endswith(".png"):
            fileEntry.append(file)
    return fileEntry

def predictor(frame):
    # Binarize thành inRange dựa trên giá trị HSV màu của bàn tay
    lower_blue = np.array([0, 58, 50])
    upper_blue = np.array([30, 255, 255])
    imcrop = frame[roiLeftTop[1]:roiRightBottom[1], roiLeftTop[0]:roiRightBottom[0]]
    hsv = cv2.cvtColor(imcrop, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Điều chỉnh kích thước ảnh để phù hợp với mô hình
    hand_img = cv2.resize(mask, (64, 64))

    # Gọi hàm predictor để nhận diện bàn tay
    recognized_result = predictor(hand_img)

    return recognized_result

def draw_bounding_box(frame, bbox):
    cv2.rectangle(frame, bbox[0], bbox[1], (0, 255, 0), 2)

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)

    # Xử lý frame để có được bounding box bàn tay
    bbox = hand_detection(frame)

    # Hiển thị bounding box
    if bbox:
        cv2.rectangle(frame, bbox[0], bbox[1], (0, 255, 0), 2)

    cv2.imshow('Hand Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()