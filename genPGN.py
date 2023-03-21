#generate a random PGN with up to 7 pieces (including both kings)

#curl http://tablebase.lichess.ovh/standard?fen=k7/p7/8/8/8/8/8/K7_w_-_-_0_1


#randomly pick # of pieces (3-7)
#randomly pick type [p,n,b,r,q]*2
#place randomly (don't worry about overwriting any)
#then place two kings randomly (or avoiding check?)

#TODO: Put final positions in stockfish (local?) to weed out inefficient solutions. Or, download 6 piece table and deep search locally. Or try monte carlo approach with API
#Improve crawl efficiency with /standard/mainline (this+MC?)



import random
import subprocess
import time
import json
import chess
import chess.engine
import pdb


engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
limit=chess.engine.Limit(time=20)

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


def query_tablebase(pgn,mainline=False):
    if mainline:
        #print("mainline")
        time.sleep(5)
    time.sleep(1)
    #print("curl http://tablebase.lichess.ovh/standard?fen="+pgn)
    if not mainline:
        gameResultTxtFull=subprocess.Popen(["curl","-s","-w","'%{stderr}%{http_code}%{stdout}'","http://tablebase.lichess.ovh/standard?fen="+pgn],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    else:
        gameResultTxtFull=subprocess.Popen(["curl","-s","-w","'%{stderr}%{http_code}%{stdout}'","http://tablebase.lichess.ovh/standard/mainline?fen="+pgn],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    gameResultTxt=gameResultTxtFull.stdout.read()
    gameResultErr=gameResultTxtFull.stderr.read()
    if gameResultErr==b"429": 
        print(gameResultErr,gameResultTxt)
        time.sleep(60)
        gameResult=query_tablebase(pgn,mainline=False)
    elif gameResultErr!=b"200":
        print(gameResultErr,gameResultTxt)
        gameResult=None
    else: 
    #try:
        gameResult = json.loads(gameResultTxt[:-2]) #where are these slashes coming from?

    return gameResult

#for x in range(5):
while True:
    validPosition=False
    while validPosition!=True:
        #print("try")
        pgn = genPGN()
        #pgn = "2q2q2/8/2k5/Q7/2b5/8/8/1K6_b_-_-_0_1"
        boardState=chess.Board(pgn.replace("_"," "))
        validPosition=boardState.is_valid()

    gameResult = query_tablebase(pgn)
    
    if gameResult!=None:
        result = gameResult['category']
        print(result+"\t"+str(gameResult['dtm']),pgn)
        

        if result=="loss":
            #print("flip")
            #make best move, result="win"
            boardState.push(chess.Move.from_uci(gameResult['moves'][0]['uci']))
            boardState.fullmove_number-=1
            pgn = boardState.fen().replace(" ","_")
            gameResult = query_tablebase(pgn)
            result="win"



        if result=="win":

            if gameResult['dtm']==None:
                lowest_dtm=9999
                #check a few mainlines and use lowest result
                for i,move in enumerate(gameResult['moves']):
                    if move['category']=='loss' and i<5: #i.e. move results in their loss. Limit to 5 for sake of server
                        
                        
                        variationBoard = boardState.copy()
                        variationBoard.push(chess.Move.from_uci(move['uci']))
                        varPGN = variationBoard.fen().replace(" ","_")
                        
                        info = engine.analyse(variationBoard, limit)
                        
                        if info['score'].is_mate() and 'pv' in info:
                            dtm = len(info['pv'])
                            #print("stockfish {}".format(dtm))
                        
                        else:
                            varResult = query_tablebase(varPGN,mainline=True)
                            dtm = len(varResult['mainline'])
                            print(move['san'],dtm)
                        lowest_dtm = min(dtm,lowest_dtm)
                        if lowest_dtm<50:
                            break
                
                #pdb.set_trace()
                gameResult["dtm"] = lowest_dtm

            if gameResult['dtm']!=None and gameResult['dtm']>=50:
                print("MOVES {}".format(gameResult['dtm']),pgn)
                with open("games.txt","a") as f:
                    player = pgn.split("_")[1]
                    if player=="w":
                        player = "White"
                    else:
                        player = "Black"
                    f.write(result+"\t"+str(gameResult['dtm']) + "\t" + pgn+"\n")
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


