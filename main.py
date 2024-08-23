import os, sys, argparse
import chess.pgn

if __name__ == "__main__":

    parser = argparse.ArgumentParser("Program description")

    parser.add_argument("-f", "--file", help="Path to the input file", required=True)
    parser.add_argument("-o", "--output", help="Path to the output file / directory", default=".")

    args = parser.parse_args()

    if args.file:
        if os.path.exists(args.file):
            filePath = os.path.abspath(args.file)
        else:
            print(f"Error: The file '{args.file}' does not exist.")
            sys.exit(1)

    if args.output:
        if os.path.exists(args.output):
            outFile = os.path.abspath(args.output)
            if os.path.isdir(outFile):
                outFile = os.path.join(outFile, "output.txt")
        else:
            print(f"Error: The output path '{args.output}' does not exist.")
            sys.exit(1)

