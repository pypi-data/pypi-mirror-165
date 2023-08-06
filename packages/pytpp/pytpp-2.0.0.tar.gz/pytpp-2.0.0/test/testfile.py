from test.bla import A, B


def main():
    a = A(b=B(c='c_str'))
    print(a.b.c)


if __name__ == '__main__':
    main()

