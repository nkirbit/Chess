# -*- coding: utf-8 -*-
"""
Chess!  Let's start with a program that defines what pieces are.
"""
### A note about location: location will be a tuple defined as (file,rank).
### This is so location matches chess notation. a1 would be (0,0) and d7
### would be (3,6).

### General question: When a piece moves, should I update its info or create
### an entirely new object? I'm not sure. For now I am updating info, but
### the other method could be better. I will see if problems arise with this
### method.

class ChessPiece:
    def __init__(self,color,location):
        self.color = color
        self.location = location
        self.possible_moves = self.get_possible_moves()

    def move(self, new_location):
        ### All pieces have the ability to move.  Two things happen here:
        ### 1) The location is updated to the new location.
        ### 2) The possible moves are updated
        ###
        ### Whether a move is valid needs to be checked.  Not sure if this
        ### will happen here or in the function managing the game.
        self.location = new_location
        self.possible_moves = self.get_possible_moves()
        return self

    def radiate_outwards(self,file_delta,rank_delta):
        ### Extends outward from a location in a particular direction.
        ### file_delta and rank_delta can take on values of -1, 0, or 1.
        ### returns a list of possible moves.
        ###
        ### If called with (0,0), return an empty list.  Staying in place
        ### is not a valid move!
        ###
        ### This function is used by the Queen, Rook, and Bishop.

        ### Eventually this will likely stop if it hits a piece, but it
        ### doesn't for now.
        possible_moves = []
        if file_delta == 0 and rank_delta == 0:
            return []
        ### Grab initial values.  Will start having moved one space away
        ### from the location to initialize the while loop.
        file_pos = self.location[0] + file_delta
        rank_pos = self.location[1] + rank_delta
        ### Each step, we will check if the piece is on the board. This uses
        ### The helper function is_on_board
        while self.is_on_board(file_pos,rank_pos):
            possible_move = (file_pos,rank_pos)
            possible_moves.append(possible_move)
            file_pos += file_delta
            rank_pos += rank_delta
        return possible_moves

    def is_on_board(self,file,rank):
        if file >= 0 and file <= 7 and rank >= 0 and rank <= 7:
            return True
        else:
            return False

class King(ChessPiece):
    def __init__(self,color,location):
        ChessPiece.__init__(self,color,location)
        self.piece = "K"
        self.has_moved = False

    def get_possible_moves(self):
        ### Will not worry about castling for now.  The possible moves are the
        ### 8 squares around the king, provided they are on the board.
        ### Not concerned (for the time being) if these are eligible moves
        file = self.location[0]
        rank = self.location[1]
        possible_moves = []
        ### Max and mins capture the end of the board.
        ### Maybe should rewrite using is_on_board ?
        for file_pos in range(max(0,file-1),min(file+2,8)):
            for rank_pos in range(max(0,rank-1),min(rank+2,8)):
                if rank_pos != rank or file_pos != file:
                    possible_move = (file_pos,rank_pos)
                    possible_moves.append(possible_move)
        return possible_moves


class Queen(ChessPiece):
    def __init__(self,color,location):
        ChessPiece.__init__(self,color,location)
        self.piece = "Q"

    def get_possible_moves(self):
        possible_moves = []
        ## Call radiate_outwards for each possible direction.
        for file_delta in [-1,0,1]:
            for rank_delta in [-1,0,1]:
                possible_moves.extend(self.radiate_outwards(file_delta,rank_delta))
        return possible_moves

class Rook(ChessPiece):
    def __init__(self,color,location):
        ChessPiece.__init__(self,color,location)
        self.piece = "R"

    def get_possible_moves(self):
        possible_moves = []
        ## Call radiate_outwards for each possible direction.
        possible_moves.extend(self.radiate_outwards(0,1))
        possible_moves.extend(self.radiate_outwards(0,-1))
        possible_moves.extend(self.radiate_outwards(1,0))
        possible_moves.extend(self.radiate_outwards(-1,0))
        return possible_moves

class Bishop(ChessPiece):
    def __init__(self,color,location):
        ChessPiece.__init__(self,color,location)
        self.piece = "B"

    def get_possible_moves(self):
        possible_moves = []
        ### Call radiate_outwards for each possible direction.
        possible_moves.extend(self.radiate_outwards(1,1))
        possible_moves.extend(self.radiate_outwards(-1,-1))
        possible_moves.extend(self.radiate_outwards(1,-1))
        possible_moves.extend(self.radiate_outwards(-1,1))
        return possible_moves

class Knight(ChessPiece):
    def __init__(self,color,location):
        ChessPiece.__init__(self,color,location)
        self.piece = "N"

    def get_possible_moves(self):
        file = self.location[0]
        rank = self.location[1]
        possible_moves = []
        ### Eight possible jumps. Just need to evaluate if jumps are on the board
        ### I'm sure there is a way to do this
        ### more elegantly, but it may obfuscate what's happening.
        for file_delta in [-1,1]:
            for rank_delta in [-2,2]:
                if self.is_on_board(file+file_delta,rank+rank_delta):
                    possible_move = (file+file_delta,rank+rank_delta)
                    possible_moves.append(possible_move)
        for file_delta in [-2,2]:
            for rank_delta in [-1,1]:
                if self.is_on_board(file+file_delta,rank+rank_delta):
                    possible_move = (file+file_delta,rank+rank_delta)
                    possible_moves.append(possible_move)
        return possible_moves

class Pawn(ChessPiece):
    ### Still need to handle promotion. I think that should be handled
    ### by adjusting the move method, but I will leave that for later.
    def __init__(self,color,location):
        ChessPiece.__init__(self,color,location)
        self.piece = "P"

    def get_possible_moves(self):
        ### For now, this will just capture moving forward.
        ### I need to incorporate captures, but won't do that until
        ### I set up the board and learn how I'm referencing other squares.
        ###
        ### No en passant for now
        possible_moves = []
        file = self.location[0]
        rank = self.location[1]
        ### Black and White move in opposite directions, so will
        ### just immediately ask what color the piece is.
        if self.color == "White":
            ###White
            if rank == 1:
                ### rank = 1 is starting space for White. If it is on this
                ### space, it can move one or two spaces.
                possible_moves.append((file,rank+1))
                possible_moves.append((file,rank+2))
            else:
                ### otherwise it can just move forward one space.
                possible_moves.append((file,rank+1))
        else:
            ###Black
            if rank == 6:
                ### starting pawn space for black.
                possible_moves.append((file,rank-1))
                possible_moves.append((file,rank-2))
            else:
                possible_moves.append((file,rank-1))
        return possible_moves
    
    
class GameState:
    def __init__(self,start = True):
        self.turn = "White"
        #self.check = self.getCheck()
        self.pieces = [[None]*8 for _ in range(8)]
        if start == True:
            ### start is asking "Do you want the position at the
            ### start of a standard chess game?  This gives you
            ### that.
            self.pieces[0][0] = Rook("White",(0,0))
            self.pieces[1][0] = Knight("White",(1,0))
            self.pieces[2][0] = Bishop("White",(2,0))
            self.pieces[3][0] = Queen("White",(3,0))
            self.pieces[4][0] = King("White",(4,0))
            self.pieces[5][0] = Bishop("White",(5,0))
            self.pieces[6][0] = Knight("White",(6,0))
            self.pieces[7][0] = Rook("White",(7,0))
            self.pieces[0][7] = Rook("Black",(0,7))
            self.pieces[1][7] = Knight("Black",(1,7))
            self.pieces[2][7] = Bishop("Black",(2,7))
            self.pieces[3][7] = Queen("Black",(3,7))
            self.pieces[4][7] = King("Black",(4,7))
            self.pieces[5][7] = Bishop("Black",(5,7))
            self.pieces[6][7] = Knight("Black",(6,7))
            self.pieces[7][7] = Rook("Black",(7,7))
            for file in range(8):
                self.pieces[file][1] = Pawn("White",(file,1))
                self.pieces[file][6] = Pawn("Black",(file,6))

    def remove_piece(self,file,rank):
        self.pieces[file][rank] = None
        return self

    def add_piece(self,file,rank,piece_type,color):
        ### Figure out a better way to do this at some point.
        ### This is fine for this problem but doesn't scale well.
        if piece_type == "K":
            piece = King(color,(file,rank))
        elif piece_type == "Q":
            piece = Queen(color,(file,rank))
        elif piece_type == "R":
            piece = Rook(color,(file,rank))
        elif piece_type == "B":
            piece = Bishop(color,(file,rank))
        elif piece_type == "N":
            piece = Knight(color,(file,rank))
        elif piece_type == "P":
            piece = Pawn(color,(file,rank))
        self.pieces[file][rank] = piece
        return self

    def switch_turn(self):
        if self.turn == "White":
            self.turn = "Black"
        elif self.turn == "Black":
            self.turn = "White"
        return self

    def display_board(self):
        output = [[None]*8 for _ in range(8)]
        for i in range(8):
            for j in range(8):
                if self.pieces[i][j] == None:
                    pass
                else:
                    output[i][j] = self.pieces[i][j].piece
        print(output)
        return self
#%%