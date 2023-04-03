( probably bootstrap )


: concat 
	@ 1 - ( Decrements given address ) 
	BEGIN
	1 + DUP
	@ DPS 0 =
	UNTIL
	!
;

: strcmp ;