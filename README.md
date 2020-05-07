# heroku_classifier
Using a simple heroku application to deploy a tensorflow classification model

## Classifier
We use a ResNet (v2) pretrained on ImageNet and finetuned on a dataset of images from Google Image to differentiate Pikachu, Kanye West and Cats. The task is really easy and only meant to play with deploying models on Heroku. Accuracy is about 97% on testing set.

## Inference optimization
To make inference faster we:
1. Quantized our model using tensorflows tf lite converter
2. Converted our model to TF-Lite and use the tf-lite interpreter to do the inference

## Data Privacy
We chose to store uploaded images so that they could be rendered in the html for a better user experience. To ensure the privacy of the data, we attribute a single image slot for each IP; each IP can only access it's own image, stored images are automatically deleted after 2 minutes, images can be deleted by the user.