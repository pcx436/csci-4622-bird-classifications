from preprocessor import preprocess
from tensorflow import keras


# TODO: start making that model!
def build_model(x_train, y_train, x_test, y_test, x_valid, y_valid):
    pass


def main():
    # seed 12345 so not random data each time
    x_train, y_train, x_test, y_test, x_valid, y_valid = preprocess(seed=12345)


if __name__ == '__main__':
    main()
