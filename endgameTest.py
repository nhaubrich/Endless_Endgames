#generate random king+pawn v king endgames, then link to lichess study and see if win or loss
from genPGN import *

def GetRank(piece,board):
    if piece in board:
        return 1+board[::-1].find(piece) // 8
    else:
        return -1

def KingAndPawnVKing():
    board = "x"*64
    board = throwPiece(board,"K")
    board = throwPiece(board,"k")
    if random.randint(0,1):
        board = throwPiece(board,"P")
    else:
        board = throwPiece(board,"p")
    #veto cases where the opposing king can't catch the pawn
    player = "wb"[random.randint(0,1)]

    if "P" in board: #white pressing
        #get rank of P, rank of k
        pawnRank = GetRank("P",board)
        kingRank = GetRank("k",board)

    else: 
        pawnRank = GetRank("p",board)
        kingRank = GetRank("K",board)
    
    pawnPastKing = pawnRank-kingRank

    #if (pawnPastKing>1)and("P" in board) or (pawnPastKing<-1)and("p" in board):
    if (pawnPastKing>(player=="b"))and("P" in board) or (pawnPastKing<-1*(player=="w"))and("p" in board):
        print("veto  http://lichess.org/analysis/"+convertToPGN(board,player))
        return KingAndPawnVKing()

    return convertToPGN(board,player)

def KingAndPawnVKingAndPawn():
    board = "x"*64
    board = throwPiece(board,"K")
    board = throwPiece(board,"k")
    
    board = throwPiece(board,"P")
    board = throwPiece(board,"p")
    
    player = "wb"[random.randint(0,1)]


    return convertToPGN(board,player)

def KRPvKR():
    board = "x"*64
    board = throwPiece(board,"K")
    board = throwPiece(board,"k")
    
    board = throwPiece(board,"R")
    board = throwPiece(board,"r")
    
    if random.randint(0,1):
        board = throwPiece(board,"P")
    else:
        board = throwPiece(board,"p")
    
    player = "wb"[random.randint(0,1)]


    return convertToPGN(board,player)


if __name__=="__main__":
    #engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
    #limit=chess.engine.Limit(time=20)

    
    for i in range(20):
        #game = KingAndPawnVKingAndPawn()
        validPosition=False
        while not validPosition:
            game=KRPvKR()
            boardState=chess.Board(game.replace("_"," "))
            validPosition=boardState.is_valid()


        url = "http://lichess.org/analysis/"+game
        print(url)
        subprocess.Popen(["firefox","-new-tab",url])
