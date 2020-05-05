from preprocessor import preprocess
import tensorflow as tf
from keras.models import Sequential
from keras.layers import BatchNormalization, Dropout
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Flatten, Dense
import matplotlib.pyplot as plt


def build_model(x_train, y_train, x_test, y_test, x_valid, y_valid):
    input_shape = x_train[0].shape
    
    model = Sequential()

    # add convolutional layers
    model.add(BatchNormalization(input_shape=input_shape))
    model.add(Conv2D(16, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(16, (3, 3), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Dropout(0.25))

    model.add(BatchNormalization())
    model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Dropout(0.25))

    model.add(BatchNormalization())
    model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Dropout(0.25))

    # add dense layers
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(201, activation='softmax'))

    # loss 'sparse_categorical_crossentropy' => does not require one-hot encoding
    print(model.summary())
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    history = model.fit(x_train, y_train, epochs=5, validation_data=(x_valid, y_valid), use_multiprocessing=True)

    return model, history


def main():
    # set seed 12345 for consistent data (not random every time)
    x_train, y_train, x_test, y_test, x_valid, y_valid = preprocess(seed=12345)

    model, history = build_model(x_train, y_train, x_test, y_test, x_valid, y_valid)

    print(model.summary())

    # plot training progress
    plt.plot(history.history['accuracy'], label='accuracy')
    plt.plot(history.history['val_accuracy'], label='val_accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.ylim([0.5, 1])
    plt.legend(loc='lower right')

    # evalutate model
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
    print('test accuracy:', test_acc)


if __name__ == '__main__':
    main()
