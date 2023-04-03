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

0 code !


( 0 10 FOR GFI . CR REPEAT )


(
: ADD S" POP EAX POP EBX ADD EAX EBX PUSH EAX" DROP PRINT ;

ADD

S" lore" DROP PRINT
0 10 FOR 
	GFI .
REPEAT

)


0 code !

EX code @ 100 < WHILE
	code @ .
	code @ 1 + code !
REPEAT


(
0 10 FOR 
	GFI . CR
REPEAT
)

90 90 = if 
	65 EMIT
then 



 