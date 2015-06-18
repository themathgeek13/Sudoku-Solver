import random 
from copy import *

file=open('sudoku.txt','r')
file2=open('sudoku_17.txt')
c=file2.read().strip()
p=c.split()
content=file.read().strip()
grids=content.split()
for string in grids[:]:		#twice to remove both...
	if(len(string)<5):
		grids.remove(string)

gridarray=[]
dummy=[]
for i in range(450):
    dummy.append(list(grids[i]))
    if((i+1)%9==0):
        gridarray.append(dummy)
        dummy=[]


def checkbox(line,pos):			#find the box referred to
    if(line<3):
        if(pos<3):
            return 0
        elif(3<=pos<6):
            return 1
        elif(6<=pos<9):
            return 2
    elif(3<=line<6):
        if(pos<3):
            return 3
        elif(3<=pos<6):
            return 4
        elif(6<=pos<9):
            return 5
    elif(6<=line<9):
        if(pos<3):
            return 6
        elif(3<=pos<6):
            return 7
        elif(6<=pos<9):
            return 8

def search_box(grid,search,boxnum):
    bythree=boxnum/3
    ctr=0
    modthree=boxnum%3
    for i in range(bythree*3,3*bythree+3):
        for j in range(3*modthree,3*modthree+3):
            if(grid[i][j]==search):
                ctr+=1
    return ctr

#search columns
def search_col(grid,search,pos):
    ctr=0
    for i in range(9):
        if(grid[i][pos]==search):
            ctr+=1
    return ctr

#search line
def search_line(grid,search,line):
    ctr=0
    for i in range(9):
        if(grid[line][i]==search):
            ctr+=1
    return ctr

def conflict(grid,search, line, pos):
    box=checkbox(line,pos)
    if(search_box(grid,search,box)):
        return True
    elif(search_col(grid,search,pos)):
        return True
    elif(search_line(grid,search,line)):
        return True
    return False

def fill_no_conflicts(grid):
    total=0
    for i in range(9):
        for j in range(9):
            count=0
            for k in range(1,10):
                if(conflict(grid,str(k),i,j)==False and grid[i][j]=='0'):
                    count+=1
                    num=k
            if(count==1):
                grid[i][j]=str(num)
                total+=1
    return total

def fill_grid(grid,num=-1):
    if(num==-1):
            num=gridarray.index(grid)
    while(True):
        i=fill_no_conflicts(grid)
        if(i==0):
            break
    for i in range(9):
            for j in range(9):
                    l2=candidates[num][i][j]
                    if(len(l2)==1):
                            val=l2[0]
                            grid[i][j]=val
                            for k in range(9):
                                    if val in candidates[num][i][k]:
                                            candidates[num][i][k].remove(val)
                            l2=[]

def allowed_at(grid,line,pos):
    num_count=0
    list_allow=[]
    for i in range(1,10):
        if(conflict(grid,str(i),line,pos)==False):
            num_count+=1
            if grid[line][pos]=='0':
                    list_allow.append(str(i))
    return list_allow

def crosshatch(grid):
    cdd=[]                         
    dummy=[]
    for j in range(9):
         for k in range(9):
             if(grid[j][k]=='0'):
                     dummy.append(allowed_at(grid,j,k))
             elif(grid[j][k]!='0'):
                     dummy.append([])
         cdd.append(dummy)
         dummy=[]
    return cdd

candidates=[]
for i in range(50):
        candidates.append(crosshatch(gridarray[i]))

def s_ch(grid,boxnum,search, num=-1):
    if(num<0):
            num=gridarray.index(grid)
    count=0
    for i in range(9):
            for j in range(9):
                    if(search in candidates[num][i][j] and checkbox(i,j)==boxnum):
                            count+=1
                            place=i
    if(count==1):
        return (place)
    else:
        return -1

def boxfill(grid,boxnum,pos,value):
    l=(boxnum/3)*3+(pos/3)
    p=(boxnum%3)*3+(pos%3)
    if(grid[l][p]=='0' and conflict(grid, str(value), l,p)==False):
            grid[l][p]=str(value)

def solve(grid, num=-1):
    for src in range(9):
        for box in range(9):
            place=s_ch(grid,box,str(src),num)
            if(place>-1):
                boxfill(grid,box,place,str(src))

coords=[]

gridc=[]
for i in range(50):
    gridc=[]
    for j in range(9):
        for k in range(9):
            if(gridarray[i][j][k]=='0'):
                gridc.append((j,k))
    coords.append(gridc)

def complete(grid):
    for line in grid:
        for num in line:
            if num=='0':
                return False
    return True

def reload(grid):
    grid_index=gridarray.index(grid)
    for i in range(9):
        for j in range(9):
            if (i,j) in coords[grid_index]:
                grid[i][j]='0'

def blanks_left(grid):
    count=0
    for i in range(9):
        for j in range(9):
            if grid[i][j]=='0':
                count+=1
    return count

#gridnav1((x,y)) ---> grid1[x][y]

def error(grid):
    if(complete(grid)):
	return False
    for i in range(9):
        for j in range(9):
            if(len(allowed_at(grid,i,j))==0 and grid[i][j]=='0'):
                return True,i,j
    return False

def logicsolve(grid,num=-1):
        fill_grid(grid,num)
        final=blanks_left(grid)
        prev=0
        while(prev!=final):
                trythis(grid,num)
                prev=final
                final=blanks_left(grid)
        return final

#allow2(grid)-> list: elements [list['possible1','possible2'] and tuple(x,y)]

def allow2(grid):
    allow=[]
    for i in range(9):
        for j in range(9):
            num=allowed_at(grid,i,j)
            if(len(num)>=2 and grid[i][j]=='0'):
                allow.append([num,(i,j)])
    return allow

def writefile():
        file=open('solved.txt','w')
        for i in range(50):
                for j in range(9):
                        for k in range(9):
                                file.write(gridarray[i][j][k])
                        file.write('\n')
                file.write('\n')
        file.close()
        
def solve_str(s1,num=-1):
    g1=[]
    for i in range(9):
        g1.append(list(s1[9*i:9*i+9]))
    gridarray[1]=deepcopy(g1)
    gridarray[1]=recsolve(gridarray[1],1,1)
    return gridarray[1]
                        
def trythis(grid,num=-1):
    for i in range(10):
        if complete(grid):
                return 0
        allowinline(grid,i%9)
        allowinrow(grid,i%9)
        allowinbox(grid,i%9)
        fill_grid(grid,num)
    return blanks_left(grid)

def allowinline(grid,line):
    l1=[]; l2=[]
    for i in range(9):
        a=allowed_at(grid,line,i)
        for item in a:
            l1.append(item)
    for item in l1:
        if l1.count(item)==1:
            l2.append(item)
    for i in range(9):
        a=allowed_at(grid,line,i)
        for item in l2:
            if item in a:
                grid[line][i]=item
                break
    return blanks_left(grid)


def allowinrow(grid,row):
    l1=[]; l2=[]
    for i in range(9):
        a=allowed_at(grid,i,row)
        for item in a:
            l1.append(item)
    for item in l1:
        if l1.count(item)==1:
            l2.append(item)
    for i in range(9):
        a=allowed_at(grid,i,row)
        for item in l2:
            if item in a:
                grid[i][row]=item
                break
    return blanks_left(grid)


def allowinbox(grid,box):
    l1=[]; l2=[]
    for i in range(9):
            for j in range(9):
                    if checkbox(i,j)==box:
                            a=allowed_at(grid,i,j)
                            for item in a:
                                    l1.append(item)
    for item in l1:
            if l1.count(item)==1:
                    l2.append(item)
    for i in range(9):
            for j in range(9):
                    if checkbox(i,j)==box:
                            a=allowed_at(grid,i,j)
                            for item in l2:
                                    if item in a:
                                            grid[i][j]=item
                                            break
    return blanks_left(grid)

def convert2str(grid):
    s=''
    for i in range(9):
        for j in range(9):
            s+=grid[i][j]
    return s

def recsolve(grid,num=-1,rnd=0):
        logicsolve(grid,num)
        if complete(grid):
                return grid
        possible=['dummy',grid]
        while len(possible)>1:
                for item in possible[1:]:
                        allowed=allow2(item)
                        if rnd==1:
                                first=random.choice(allowed)

                        else:
                                first=allowed[0]
                        opts=first[0]
                        coords=first[1]
                        x,y=coords
                        for p in opts:
                                g2=deepcopy(item)
                                g2[x][y]=p
                                logicsolve(g2,num)
                                if complete(g2):
                                        grid=g2
                                        return grid
                                if not error(g2) and g2 not in possible:
                                        possible.append(g2)
                                        #print "blank=",blanks_left(g2)
                        #possible.remove(item)
                        print len(possible)
                for item in possible[1:]:
                        if complete(item):
                                possible=[item]
                                break
                        elif error(item):
                                possible.remove(item)
        return item
