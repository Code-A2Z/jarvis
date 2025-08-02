import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Dataset paths
train_dir = "/kaggle/input/fer2013/train"
test_dir = "/kaggle/input/fer2013/test"

# Image generators
datagen = ImageDataGenerator(rescale=1./255)

train_gen = datagen.flow_from_directory(train_dir, target_size=(48,48), color_mode="grayscale",
                                        class_mode="categorical", batch_size=64)
test_gen = datagen.flow_from_directory(test_dir, target_size=(48,48), color_mode="grayscale",
                                       class_mode="categorical", batch_size=64)

# Model
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(48,48,1)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(7, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train
history = model.fit(train_gen, validation_data=test_gen, epochs=50)

# Save in .keras format
model.save("/kaggle/working/best_emotion_model.keras")
