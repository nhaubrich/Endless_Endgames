# Endless Endgames
Generate an unlimited number of random chess positions with specified pieces and open them in Lichess for study.

## Overview
Books on chess endgames tend to be dense with explanations but relatively light on drills. To master a technique, one needs practice. This repo is a tool to generate random positions given a set of pieces (e.g. king and pawn vs king) that are opened in Lichess in the browser. Lichess allows the position to be played against a computer or looked up in the tablebase for the optimal solution. This enables efficient practice of many common endgames by repeated example.

## Usage
`python endgameTest.py [pieces] [side] [positions]` where `[pieces]` are specified by algebraic names with uppercase denoting white; `[side]` is "w","b", or "r" for white,black, and random, respectively; and `[positions]` is the integer number of positions to generate.

`python endgameTest.py KkP r 10`: Generate 10 positions of king and pawn vs king, taking a random side.

`python endgameTest.py KkNB w 5`: Generate 5 positions of king, knight, and bishop vs king, taking the stronger side.

`python endgameTest.py KkQppp b 1`: Generate 1 position of king and queen vs king and three pawns, taking the weaker side.

## Sample Positions
![image](https://github.com/user-attachments/assets/09e8bc8f-fb6b-403b-9709-39f6bb800e63)
![image](https://github.com/user-attachments/assets/d892fba3-07b7-4af7-b9ec-4ada8c8ac360)
![image](https://github.com/user-attachments/assets/6c1db955-7969-48b0-8674-81280debb515)

