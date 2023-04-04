IMPORT std.forth
IMPORT interpreter.forth

VARIABLE tokens 100 get_arr tokens !
VARIABLE buffer 100 get_arr buffer !
VARIABLE stk 1000 get_arr stk !
VARIABLE code S" 90" DROP code ! 

VARIABLE index
code @ index ! ( index in code )

: eval ;

(
buffer @ print CR
)
S" opop" drop PRINT 

VARIABLE x
0 code !
0 x !







WHILE

	WHILE
				90 EMIT
				code @ .
				code @ 1 + code !
				10 EMIT
	code @ 10 <	
	REPEAT
	
	89 EMIT
	x @ .
	x @ 1 + x !
	10 EMIT
	 x @ 2 <
REPEAT


90 90 = if 
	65 EMIT
then 



 
