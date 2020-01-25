from queue import PriorityQueue
import math
def bfssearch(graph, landing_column, landing_row, x, y, columns, rows, max_elevation):
    queue = [[landing_row,landing_column]]
    visited = [[landing_row,landing_column]]
    parent = {}
    path = False
    while len(queue) > 0:
        p = queue[0]
        queue = queue[1:]
        i, j = p[0], p[1]
        for row in range(-1,2):
            for col in range(-1,2):
                if row == 0 and col == 0:
                    continue
                X = i + row
                Y = j + col  
                #print(graph[i][j], graph[X][Y])
                if X >= 0 and X < rows and Y >= 0 and Y < columns and abs(graph[X][Y] - graph[i][j]) <= max_elevation:
                    if [X,Y] not in visited:
                        visited.append([X,Y])
                        queue.append([X,Y])
                        parent[(X,Y)] = (i,j)
                        if X == x and Y == y:
                            #path found
                            path = True
                            path_exists = returnpath(parent, landing_column,landing_row,x,y)
                            x = [str(j)+","+str(i) for i, j in path_exists]
                            output = " ".join(x)
                            #print(output)
                            return output                            
    if not path:
        return "FAIL"
    
    
def returnpath(parent,landing_column,landing_row,x,y):
    path = [(x,y)]
#    print(parent)
    while path[-1] != (landing_row,landing_column):
        path.append(parent[path[-1]])
    path.reverse()
    return path
       
def ucssearch(graph, landing_column, landing_row, x, y, columns, rows, max_elevation):
    queue = PriorityQueue()
    queue.put([0, landing_row, landing_column])
    costmatrix = [[math.inf for u in range(columns)] for v in range(rows)]
    parent = [[[-1,-1] for i in range(columns)] for j in range(rows)]
    vis = [[False for i in range(columns)] for j in range(rows)]
    parent[landing_row][landing_column] = [landing_row, landing_column]
    flag = False
    totalcost = 0

    while not queue.empty():
        v = queue.get()
        cost, r, c = v[0], v[1], v[2]
        vis[r][c] = True
        if r == x and c == y:
            flag = True
            break

        for i in range(-1,2):
            for j in range(-1,2):
                if i == 0 and j == 0:
                    continue
                X, Y = i + r, j + c
                if X >=0 and X < rows and Y >= 0 and Y < columns and abs(graph[X][Y] - graph[r][c]) <= max_elevation and not vis[X][Y]:
                    add_cost = 0
                    if r == X or c == Y:
                        add_cost = 10
                    else:
                        add_cost = 14
                    totalcost = cost + add_cost
                    if costmatrix[X][Y] > totalcost:
                        costmatrix[X][Y] = totalcost 
                        parent[X][Y] = [r,c]
                    queue.put([costmatrix[X][Y],X,Y])

    if flag:
        path = []
        path.append((x,y))
        while path[-1] != (landing_row, landing_column):
            path.append(tuple(parent[path[-1][0]][path[-1][1]]))
        path.reverse()
        x = [str(j)+","+str(i) for i, j in path]
        output = " ".join(x)
        return output
    else:
        return "FAIL"

def sldheuristic(x1, y1, x2, y2):
    distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    return distance
    
def astarsearch(graph, landing_column, landing_row, x,y, columns, rows, max_elevation):
    queue = PriorityQueue()

    queue.put([sldheuristic(landing_row, landing_column,x,y),landing_row, landing_column])
    parent = [[[-1,-1] for i in range(columns)] for j in range(rows)]
    costmatrix = [[math.inf for u in range(columns)] for v in range(rows)]
    costmatrix[landing_row][landing_column] = 0
    totalcost = 0
    vis = [[False for i in range(columns)] for j in range(rows)]
    parent[landing_row][landing_column] = [landing_row, landing_column]
    flag = False


    while not queue.empty():
        v = queue.get()
        r, c = v[1], v[2]
        cost = costmatrix[r][c]
        vis[r][c] = True
        if r == x and c == y:
            flag = True
            break

        for i in range(-1,2):
            for j in range(-1,2):
                if i == 0 and j == 0:
                    continue
                X, Y = i + r, j + c
                if X >=0 and X < rows and Y >= 0 and Y < columns and abs(graph[X][Y] - graph[r][c]) <= max_elevation and not vis[X][Y]:
                    add_cost = 0
                    if r == X or c == Y:
                        add_cost = 10
                    else:
                        add_cost = 14
                    totalcost = cost + add_cost + abs(graph[X][Y] - graph[r][c])
                    if costmatrix[X][Y] > totalcost:
                        costmatrix[X][Y] = totalcost 
                        parent[X][Y] = [r,c]
                    queue.put([costmatrix[X][Y]+sldheuristic(X,Y,x,y),X,Y])
    if flag:
        path = []
        path.append((x,y))
        while path[-1] != (landing_row, landing_column):
            path.append(tuple(parent[path[-1][0]][path[-1][1]]))
        path.reverse()
        x = [str(j)+","+str(i) for i, j in path]
        output = " ".join(x)
        #print(output)
        return output


    else:
        return "FAIL"

                    

inputfile = open("input.txt")
inputfile_string = inputfile.read().split('\n')
search_algo = inputfile_string[0]
columns, rows = (int(x) for x in inputfile_string[1].split())
landing_column, landing_row = (int(y) for y in inputfile_string[2].split())
max_elevation = int(inputfile_string[3])
target_count = int(inputfile_string[4])
targetlist = []
for i in range(target_count):
    a,b = (int(z) for z in inputfile_string[5+i].split())
    targetlist.append([a,b])    
graph = []
for i in range(rows):
    a = list(map(int, inputfile_string[5+target_count+i].split()))
    graph.append(a)
#print(search_algo,columns,rows,landing_column,landing_row,max_elevation,target_count,targetlist, graph)
s = []
for i in targetlist:
    y, x = i[0], i[1]
    if search_algo == "BFS":
        s.append(bfssearch(graph, landing_column,landing_row,x,y, columns, rows, max_elevation))
    if search_algo == "UCS":
        s.append(ucssearch(graph, landing_column,landing_row,x,y, columns, rows, max_elevation))
    if search_algo == "A*":
        s.append(astarsearch(graph, landing_column,landing_row,x,y, columns, rows, max_elevation))
        
with open('output.txt','w') as f:
    for i in range(len(s)):
        if i == len(s)-1:
            f.write(s[i])
        else:
            f.write(s[i]+"\n")