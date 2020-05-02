from preprocessor import preprocess
import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt


def build_model(x_train, y_train, x_test, y_test, x_valid, y_valid):
    # following first guide on https://www.tensorflow.org/tutorials/images/cnn
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=x_train[0].shape))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))

    # add dense layers
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(201))

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    history = model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test), use_multiprocessing=True)

    return model, history


def main():
    # seed 12345 so not random data each time
    x_train, y_train, x_test, y_test, x_valid, y_valid = preprocess(seed=12345)
    model, history = build_model(x_train, y_train, x_test, y_test, x_valid, y_valid)

    print(model.summary())

    plt.plot(history.history['accuracy'], label='accuracy')
    plt.plot(history.history['val_accuracy'], label='val_accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.ylim([0.5, 1])
    plt.legend(loc='lower right')

    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
    print('test accuracy:', test_acc)


if __name__ == '__main__':
    main()
