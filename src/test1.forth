IMPORT std.forth

: recurse ( recursion test )
	DUP
	900 < if
	DUP . 10 EMIT
		1 + recurse
	then
	;
0 recurse


( Block test )
VARIABLE T
0 T ! 
VARIABLE A
0 A !

SBLK
	0 T !
	SBLK
		89 emit
		T @ 1 + T !
		T @ . CR
	EBLK
		T @ 10 < 
	RKBLKC 
EBLK
	90 emit
	A @ 1 + A !
	A @ 10 < 
RKBLKC



( Print test )
S" opop" DROP PRINT

( testing syntax stuff )
: def : ;
: { SBLK ;
: } EBLK ;

def popbob ( ) {
	
} ;


