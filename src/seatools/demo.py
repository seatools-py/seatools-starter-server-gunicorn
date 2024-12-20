import argparse

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("args", nargs="*", help=argparse.SUPPRESS)
    args = parser.parse_args()
    print(args)


if __name__ == '__main__':
    run()
