#generate a random PGN with up to 7 pieces (including both kings)

#curl http://tablebase.lichess.ovh/standard?fen=k7/p7/8/8/8/8/8/K7_w_-_-_0_1


#randomly pick # of pieces (3-7)
#randomly pick type [p,n,b,r,q]*2
#place randomly (don't worry about overwriting any)
#then place two kings randomly (or avoiding check?)

#TODO: increase efficiency. prevent backrank pawns, then smarter king placement. Switch to pychess? Filter out knight and bishop?



import random
import subprocess
import time
import json
import chess
import pdb

def convertToPGN(board):
    #split into rows, then merge contiguous x's
    board_rows = [board[i*8:(i+1)*8] for i in range(8)]
    pgn_rows = []
    #print(board_rows)
    for row in board_rows:
        #this is so dirty
        pgn_row = row
        for i in range(1,9)[::-1]:
            #print("")
            #print(pgn_row)
            pgn_row = pgn_row.replace("x"*i,str(i))
            #print(pgn_row)
        pgn_rows.append(pgn_row)
    player = "wb"[random.randint(0,1)]
    pgn = "/".join(pgn_rows)+"_{}_-_-_0_1".format(player)

    return pgn

def genPGN():
    board = "x"*64
    #nPieces = random.randint(2,5) #besides kings
    nPieces = 4 #besides kings
    #print("nPieces",nPieces)
    for i in range(nPieces):
        board = throwPiece(board)

    board = throwPiece(board,'k')
    board = throwPiece(board,'K')
    board = convertToPGN(board)
    return board

def throwPiece(board,type_of_piece=None):
    pieces = "pnbrqPNBRQ"
    if type_of_piece is None:
        type_of_piece = pieces[random.randint(0,9)]

    if type_of_piece in "pP":
        position = random.randint(8,55)
    else:
        position = random.randint(0,63)
    return board[0:position] + type_of_piece + board[position+1:64]

#for x in range(5):
while True:
    validPosition=False
    while validPosition!=True:
        print("try")
        pgn = genPGN()
        validPosition=chess.Board(pgn.replace("_"," ")).is_valid()

    #print(pgn)
    #output = subprocess.check_output(['curl','http://tablebase.lichess.ovh/standard?fen=k7/p7/8/8/8/8/8/K7_w_-_-_0_1'])
    #gameResult=os.popen('curl http://tablebase.lichess.ovh/standard?fen=k7/p7/8/8/8/8/8/K7_w_-_-_0_1').read()
    #gameResultTxt=os.popen('curl http://tablebase.lichess.ovh/standard?fen='+pgn).read()
    print("curl http://tablebase.lichess.ovh/standard?fen="+pgn)
    #gameResultTxtFull=subprocess.Popen(["curl","http://tablebase.lichess.ovh/standard?fen="+pgn],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
    gameResultTxtFull=subprocess.Popen(["curl","-s","-w","'%{stderr}%{http_code}%{stdout}'","http://tablebase.lichess.ovh/standard?fen="+pgn],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    gameResultTxt=gameResultTxtFull.stdout.read()
    gameResultErr=gameResultTxtFull.stderr.read()
    if gameResultErr==b"429": 
        print(gameResultErr,gameReultTxt)
        time.sleep(60)
    elif gameResultErr!=b"200":
        print(gameResultErr,gameReultTxt)
    else: 
    #try:
        gameResult = json.loads(gameResultTxt[:-2]) #where are these slashes coming from?

        result = gameResult['category']
        print(result+"\t"+str(gameResult['dtm']),pgn)
        pdb.set_trace()
        if gameResult['dtm']>=50:
            print(pgn)
            with open("games.txt","a") as f:
                player = pgn.split("_")[1]
                if player=="w":
                    player = "White"
                else:
                    player = "Black"
                f.write(result+"\t"+str(gameResult['dtm']) + "\t" + pgn+"\n")
                #pdb.set_trace()
                text = "{} mates in {}".format(player,gameResult['dtm']) 
                pngCommand = ["python3","fen-to-img/main.py"]+pgn.split("_")+["-o",player+"_"+str(gameResult['dtm'])+"_"+pgn.replace("/","").replace("-","")]+["-d","pngs/"]
                pngCommand[4]="KQ"
                print(" ".join(pngCommand))
                subprocess.Popen(pngCommand)

        #if result in ['cursed-win','blessed-loss']:
            #print(gameResult['dtm'],result,"for white!")
    #except:
        #print(gameResultTxt)
    #    pass
    time.sleep(1)


