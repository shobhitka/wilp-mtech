;	if (a<b) {
;		x=5
;		y=c+d
;	} else {
;		y=c-d
;	}

	AREA RESET, CODE, READONLY
	ENTRY
START
	ADR R4,SRC  ;same section location
	LDR R5,=DST ;used for accessing labels in other section, we use LDR
	BL SUB1     ;L => link register contains the return address -> R14
STOP 
	B STOP

SUB1 LDR R0,[R4],#4
	LDR R1,[R4],#4
	CMP R0,R1
	BGE FB1
	LDR R0,[R4],#4
	LDR R1,[R4],#4
	ADD R0,R0,R1
	MOV R2,#5
	STR R2,[R5],#4
	STR R0,[R5]
	B AFT
FB1 LDR R0,[R4],#4
	LDR R1,[R4]
	SUB R0,R0,R1
	STR R0,[R5,#4]
AFT MOV PC,LR
SRC DCD 0x40, 0x40, 0x30, 0x10

	AREA RESULT, DATA, READWRITE
DST DCD 0, 0
	END