"""Console script for ppw0810."""

import fire


def help():
    print("ppw0810")
    print("=" * len("ppw0810"))
    print("Skeleton project created by Python Project Wizard (ppw)")


def main():
    fire.Fire({"help": help})


if __name__ == "__main__":
    main()  # pragma: no cover
