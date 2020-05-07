from app.prediction import predict
import os

image_path = os.path.join("app","static","images","input_0.jpg")
print(predict(image_path))