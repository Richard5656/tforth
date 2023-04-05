: CR 10 EMIT ;
: IF INVERT SKBLKC  SBLK ;
: THEN EBLK ;

: BEGIN SBLK ;
: UNTIL  INVERT SRKBLKC EBLK ;

: COND SBLK ;


: WHILE INVERT SSKBLKC ;


: REPEAT SRKBLK EBLK ;

( Syntax
      EX [condition] WHILE REPEAT
)


: DUP2 DUP >r SWAP DUP >r SWAP r> r> ; ( duplicates 2 items on the stack )

: FOR 1 + SBLK SWAP 1 +  SWAP DUP2 < INVERT SSKBLKC ;
: END_FOR SRKBLK EBLK DROP DROP ;
( Syntax
       [start num] [end num] FOR END_FOR
)

: GFI SWAP DUP 1 - >R SWAP R> ; ( Gets the index of the For loop currently  )


: PRINT 1 - 
	BEGIN
		
		 
		1 + 
		
		DUP @ DUP
		0 = INVERT if
			EMIT
		THEN
		DUP @ 0 =
		
	UNTIL 
; ( Prints out strings )

: dps DUP . CR ; ( debug printer )


: INC ( Increments varible by ) DUP >r @ + r> ! ; ( [inc ammt] [memloc] INC )
: DEC ( Increments varible by ) DUP >r @ - r> ! ; ( [dec ammt] [memloc] DEC )

( temp stack functions for stuff I want to save )


VARIABLE sp ( Start of return stack )
VARIABLE bp ( bp[0] will ussually be the return )
7500 sp !
7000 bp !

: >r sp @ ! sp @ 1 + sp ! ( Increment stack ) ;
: r> sp @ 1 - sp ! ( decrement stack ) sp @ @ ;
: r@ sp @ ( copy on to data stack from return stack ) ;

: LBPA bp + @ ; ( [mem_loc] LDBA )
: SBPA bp + ! ; ( [mem_loc] [offset] SDBA )
VARIABLE array_area_start
1 array_area_start !

: get_arr array_area_start DUP INC ; ( increments arr pointer and then return position )

: GETC @ ;

: { ;
: } ; 

: ARRACK + @ ; ( Array access at certain index )




