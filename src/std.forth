: CR 10 EMIT ;
: IF INVERT SKBLKC SBLK ;
: ELSE SKBLK EBLK SBLK ;
: THEN EBLK ;


: BEGIN SBLK ;
: UNTIL EBLK INVERT RKBLKC ;

: WHILE  SBLK INVERT SKBLKC  ;



: REPEAT    SRKBLK EBLK ;

( Syntax 
	EX [condition] WHILE REPEAT
)


: DUP2 DUP PSH SWAP DUP PSH SWAP POP POP ; ( duplicates 2 items on the stack )

: FOR SBLK SWAP 1 +  DUP2 < INVERT SKBLKC ;

( Syntax 
	 [start num] [end num] FOR REPEAT
)


: GFI DUP 1 - ; ( Gets the index of the For loop currently )


: DO ! ! LBL ;
: LOOP
     DUP DUP ( duplicates index VARIABLE )
     @ 1 + SWAP ! ( Increment index )
     @ SWAP @ < ( Compare )
	 BC ( Branch )
;

( Syntax 

[value] [start varible] [value] [end varible] do
	[start varible] [end varible]
	LOOP
)



: PRINT 1 - 
	BEGIN 
		1 + 
		DUP @  EMIT 
		DUP @ 0 = 
UNTIL ;

: dps DUP . CR ; ( debug printer )


: INC ( Increments varible by ) DUP PSH @ + POP ! ; ( [inc ammt] [memloc] INC )
: DEC ( Increments varible by ) DUP PSH @ - POP ! ; ( [dec ammt] [memloc] DEC )

( temp stack functions for stuff I want to save )


VARIABLE sp
VARIABLE bp ( bp[0] will ussually be the return )
7500 sp !
7000 bp !

: PSH sp @ ! sp @ 1 + sp ! ( Increment stack ) ;
: POP sp @ 1 - sp ! ( decrement stack ) sp @ @ ;
: LBPA bp + @ ; ( [mem_loc] LDBA )
: SBPA bp + ! ; ( [mem_loc] [offset] SDBA )
VARIABLE array_area_start
1 array_area_start !

: get_arr array_area_start DUP INC ; ( increments arr pointer and then return position )

: GETC @ ;

: { ;
: } ;

: ARRACK + @; ( Array access at certain index )
: isDigit 
	1 SBPA ( stores string location in the bp )
	1 0 SBPA 
	BEGIN
		39 1 LBPA @ < 
		58 1 LBPA @ > and 
		0 LBPA and ( check if it is between the correct ascii codes to be a digit )
		0 SBPA ( store and and return address )
		1 LBPA 1 + 1 SBPA  ( increment address )
		1 LBPA @ 0 =
	UNTIL

	0 LBPA
; 
