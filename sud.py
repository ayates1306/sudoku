#! /usr/bin/python3

import logging

puzzle_hard = [0,0,0,  0,9,0,  0,0,0,
          0,7,3,  0,0,0,  6,8,0,
          0,6,4,  0,0,0,  9,3,0,
          
          0,0,0,  4,7,5,  0,0,0,
          0,1,5,  0,0,0,  2,4,0,
          0,0,0,  0,1,0,  0,0,0,
          
          0,3,0,  0,0,0,  0,9,0,
          6,0,0,  0,0,0,  0,0,8,
          8,0,9,  0,5,0,  7,0,6  
    ]


puzzle_easy = [ 1,3,8,  0,4,0,  0,0,0,
           5,0,9,  0,0,7,  1,0,0,
           2,0,0,  0,9,0,  6,0,0,
           
           4,8,0,  0,6,9,  0,0,0,
           0,0,0,  0,0,0,  0,0,0,
           0,0,0,  7,2,0,  0,3,8,
           
           0,0,4,  0,1,0,  0,0,5,
           0,0,6,  8,0,0,  9,0,7,
           0,0,0,  0,7,0,  8,1,4,
    ]


sub_square_done = [False, False, False,
                   False, False, False,
                   False, False, False]

puzzle1 = [ 0,2,0, 6,0,0, 0,0,4,
           0,7,6, 0,2,4, 1,0,9,
           0,0,0, 0,8,0, 0,0,0,

           0,1,0, 0,0,6, 0,3,2,
           9,8,4, 0,0,0, 5,1,6,
           2,6,0, 4,0,0, 0,9,0,

           0,0,0, 0,6,0, 0,0,0,
           1,0,2, 7,4,0, 9,6,0,
           6,0,0, 0,0,8, 0,5,0
    ]


def get_row(puz, r):
    return puz[r*9 : r*9+9]

def get_col(puz, c):
    return puz[c : 81 : 9]

# return the 3x3 sub square
# x, y are 0..2
# returned data is array 0..8 in the format
# row1, row2, row3
def get_sub_square(puz, x,y):
    index = x*3 + y*27
    r1 = puz[index : index + 3]
    index += 9
    r2 = puz[index : index + 3]
    index += 9
    r3 = puz[index : index + 3]
    return r1+r2+r3

def check_multiples(data_set):
    for i in range(1,9):
        if (data_set.count(i) > 1):
            return False
    return True
        
        

def prep_missing(data_set):
    expect = [1,2,3,4,5,6,7,8,9]
    for i in data_set:
        if i in expect:
            expect.remove(i)
    return expect


# This function takes the sub square at x,y
# then for each missing number, checks if that number
# has 1 and only 1 possibly place in the empty sqaures
def find_numbers(puz, x, y):
    #breakpoint()
    found = False
    s = get_sub_square(puz, x, y)
    m = prep_missing(s)
    print (m)
    for num in m:
        poss = 0
        pc = None
        pr = None
        for col in range (0,3):
            if poss > 1: # Did we already find more than 1 possibility in the inner loop?
                break
            c = get_col(puz, x*3 + col)
            for row in range (0, 3):
                if (puz[x*3 + y*27 + row *9 + col] != 0):
                    continue
                r = get_row(puz, y*3 + row)
                #print ("row ", row, ":", r)
                mix = c + r
                try:
                    mix.index(num)
                except:
                    #print("Possible for ",num," at ", col, ",", row)
                    poss = poss + 1
                    pc = col
                    pr = row
                    if poss == 2: # No need to keep looking, we know there is no place for the number
                        break;
                 
        if poss == 1:
            print ("num ", num, "had ", poss, "possible place; adding to ", pc, ",", pr)
            print("before ", puz)
            puz[x*3 + y*27 + pr *9 + pc] = num
            print("after ", puz)
            found = True
    return found

# solve_square, x = 0 to 2, y = 0 to 2
# Iterate through all 0 spaces
# Look for numbers, fill them in
# Repeat until all squares filled or no new numbers added
# Return True if the square is solved
def solve_square(puz, x, y):
    find_numbers(puz, x, y)
    # How many empty spaces are there?
    s = get_sub_square(puz, x, y)
    m = prep_missing(s)
    mcnt = len(m)
    print("m", m)
    if (len(m) == 0):  # The sub square is complete
        return True
    if (len(m) == 1):  # There is only 1 entry to fill in the sub square so fill it in
        i = s.index(0)
        puz[x*3 + y*27 + (i //3 * 9) + i % 3] = m[0]
        return True

    cnt = 0
    while True:
        updated = False
        # Find the empty spaces; repeat until there are no further updates
        for col in range (0,3):
            for row in range (0,3):
                s = get_sub_square(puz, x, y)
                print ("sub square ", s)
                col_ok = False
                row_ok = False
                # Is the sub square row incomplete?
                # Is there only 1 space in the row?
                try:
                    s[row*3:row*3+3].index(0)
                    row_ok = True
                    r = get_row(puz, y*3 + row)
                    m = prep_missing(s + r)
                    print("col #", col, "row #", row, " row", r)
                    if (len(m) == 1):  # There is only 1 entry to fill in the sub row so fill it
                      print("add entry to row; m=", m)
                      i = r.index(0, x*3)   # The space must be in the ROW of the square
                      puz[row * 9 + y*27 +  i] = m[0]
                      updated = True
                      mcnt = mcnt -1
                      continue
                except:
                    pass
                    #print("ROW Exception")
                    
                try:
                    s[row*3+col::row*3+col+3].index(0)
                    col_ok = True
                    # Is there only 1 space in the column?
                    c = get_col(puz, x*3 + col)
                    print("col #", col, "row #", row, " col", c)
                    m = prep_missing(s + c)
                    # Is there only 1 space in the row + column?
                    if (len(m) == 1):  # There is only 1 entry to fill in the sub col so fill it
                      print("add entry to col; m=",m)
                      i = c.index(0, y*3)   # The space must be in the COLUMN on the square
                      print ("Insert ", m[0], "into pos x ", x, "i ",i, "col ", col )
                      puz[col + x*3 + i*9] = m[0]
                      updated = True
                      mcnt = mcnt -1
                      continue
                except:
                    pass
                    #print("Col exception")
                    
                # Now consider intersections of the row + column but only if the row and col were incomplete
                if row_ok == True and col_ok == True and puz[col + x*3 + row*9 + y*27] == 0:
                    m = prep_missing(s + c + r)
                    # Is there only 1 space in the row + column?
                    if (len(m) == 1):  # There is only 1 entry to fill in the sub col so fill it
                      print("add entry to intersection of row and col; m=",m)
                      print ("c = ", c)
                      print ("r = ", r)
                      print ("Insert ", m[0], "into square ", x, ",",y, " box col ", col, "row ", row)
                      puz[col + x*3 + row*9 + y*27] = m[0]
                      print(puz)
                      updated = True
                      mcnt = mcnt -1
                      continue
        # Abort the search if not more updates
        if updated == False:
            break;
    print (mcnt," numbers left")
    if mcnt == 0:
        return True
    return False


#########################################################################


loop = 0
done = 0

puzzle = puzzle_easy

while True:
    ds= done
    puz_state = puzzle
    print("Loop number ", loop, "completed boxes ", done)
    print(puzzle)
    for y in range(0,3):
        for x in range(0,3):
            if sub_square_done[x + y*3]:
                continue
            if solve_square(puzzle, x, y):
                sub_square_done[x + y*3] = True
                done = done + 1
    loop = loop + 1
    if puzzle == puz_state:
        print ("No new number added, stopping")
        break


print(puzzle)

def main():
    print("Main")
