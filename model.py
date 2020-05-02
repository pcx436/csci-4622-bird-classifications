from preprocessor import preprocess


def main():
    # TODO: start making that model!
    x_train, y_train, x_test, y_test, x_valid, y_valid = preprocess(seed=12345)

    print(len(x_train))


if __name__ == '__main__':
    main()
