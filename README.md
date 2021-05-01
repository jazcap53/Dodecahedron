## Dodeca: models a bicolored dodecahedron

#### Shows that no more than three blue faces can be placed on a red dodecahedron such that no two blue faces share an edge. 

The code creates a Pentagon class, to model the faces, and a Dodecahedron class, to model the regular solid. 

Each face is named with a single-letter string. The names are hard-coded only once in the program, to make it simple to adapt
the program for an icosahedron.

The number of blue faces can be given as a command-line argument; that number defaults to three.  

By default, the program tries every combination of three blue faces and nine red faces, until it finds one that 
fulfills the desired condition. It prints this combination as a solution.

If the program is handed the command-line argument four, it will try every combination of four blue faces and eight
red faces. It will find no solution, and prints the string "Failure".  
&nbsp;  
&nbsp;  
License: GNU GPLv3
