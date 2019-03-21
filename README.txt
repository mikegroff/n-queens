for nqueens file runs on python 3 with only standard libraries: collections.deque,time,copy,numpy & matplotlib. 
Running the file will output the graph in the report for individual solutions edit the main function to simply read:
ss(n), bt(n), btfc(n), or btfcdo(n), these functions return solution nodes, for solution indices youll need printindex(soln, Board(n))
where n is the size of the board and soln = bt(n) (for example).
