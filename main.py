import os, sys, argparse
import chess.pgn

import multiprocessing

def findAmountOfGames(filePath):
    gameCounter = 0
    with open(filePath, mode="r") as file:
        for line in file:
            if line.startswith("[Event "):
                gameCounter += 1
    return gameCounter

def getAllFen(game):
    board = game.board()

    setOfFen = set()

    for move in game.mainline_moves():
        board.push(move)
        setOfFen.add(board.fen())

    return setOfFen

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
    parser.add_argument("-b", "--batches", help="Amount of batches to run program with", default=50)

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
                outFile = os.path.join(outFile, "output")
        else:
            print(f"Error: The output path '{args.output}' does not exist.")
            sys.exit(1)
        
    if args.batches:
        try:
            amountBatches = int(args.batches)
        except ValueError:
            print(f"Error: Amount of batches: '{args.batches}' cannot be parsed as an int.")
            sys.exit(1)


    

    # Find amount of games in file
    print("Counting total games...")
    totalGames = findAmountOfGames(filePath)
    print("Total games:", totalGames)

    gamesPerBatch = totalGames // amountBatches
    remainingGames = totalGames % amountBatches

    file = open(filePath, "r")

    for batchIndex in range(amountBatches):
        print(f"Working on batch {batchIndex + 1}")
        batchGames = []

        for _ in range(gamesPerBatch + (1 if batchIndex < remainingGames else 0)):
            game = chess.pgn.read_game(file)
            if game is None:
                break
            batchGames.append(game)
        
        print(f"Extracting FEN's")

        with multiprocessing.Pool() as pool:
            setOfAllFen = pool.map(getAllFen, batchGames)

        allFen = set().union(*setOfAllFen)

        batchOutFile = str(outFile) + "_batch_" + str(batchIndex+1) + ".txt"
        saveFenToFile(allFen, batchOutFile)
    
    print("Completed")

