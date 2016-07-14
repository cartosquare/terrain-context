## features
this part of program will extract deep-features of downloaded images, and split them into training and validate set

### workflow
* first, use *extract_image_list.py* to generate a image list that will feed into caffe
* then, use *extract_training_features.py* to calculate deep-features for the images in the list that will generated in the last step
* finally, use *generate_train_test.py* to split the deep-features as training set and validate set
