import os, sys, argparse
import chess.pgn

import multiprocessing

def getAllFen(game):
    board = game.board()

    listOfFen = []

    for move in game.mainline_moves():
        board.push(move)
        listOfFen.append(board.fen())
    
    return listOfFen

def retrieveAllGames(filePath):
    listOfAllGames = []

    pgn = open(filePath)

    game = chess.pgn.read_game(pgn)
    while game != None:
        listOfAllGames.append(chess.pgn.read_game(pgn))
    
    pgn.close()

    return listOfAllGames

def saveFenToFile(fenStrings, outFilePath):
    with open(outFilePath, mode="w") as f:
        for fen in fenStrings:
            f.write(fen + "\n")

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

    games = retrieveAllGames(filePath)

    with multiprocessing.Pool() as pool:
        listOfAllFen = pool.map(getAllFen, games)
        
    listOfAllFen = [fen for sublist in listOfAllFen for fen in sublist]

    saveFenToFile(listOfAllFen, outFile)
    print("Output written to:", outFile)