"""Console script for ppw."""

import fire


def help():
    print("ppw")
    print("=" * len("ppw"))
    print("Skeleton project created by Python Project Wizard (ppw)")


def main():
    fire.Fire({"help": help})


if __name__ == "__main__":
    main()  # pragma: no cover
