from app.prediction import predict
import os


# image_path = os.path.join("app","static","images","input_0.jpg")
image_path = "C:\\Users\\victo\\Documents\\L2L tech final assignments\\data\\training\\Cats\\Cats_18.jpg"
print(predict(image_path))