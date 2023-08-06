import os
import argparse


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file to run")
    args = parser.parse_args()

    os.system(f"g++ {args.filename}")
    os.system(f"./a.out")
    os.system(f"rm -rf ./a.out")


if __name__ == "__main__":
    cli()