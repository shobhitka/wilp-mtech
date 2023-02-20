	AREA RESET, CODE, READONLY
	ENTRY
		
; Exception vectors
Vectors
	LDR PC, reset_addr
	LDR PC, swi_addr
		
reset_addr
	DCD Reset_Handler
swi_addr
	DCD SWI_Handler
	B SWI_Handler
			
;Reset handler
Reset_Handler
	MSR CPSR_C,#0x10		;switch to user mode
	MOV R0,#5				; initialize with number 5
	SWI 0x25

STOP
	B STOP
	
SWI_Handler
	LDR SP,=0x40000100
	STMFD SP!,{R1-R12}		;Store the registers on the stack, exclude R0 where we store the final result
	
	; write code logic
	LDR R1,[LR,#-4] 		;Since on execution of SWI, LR is loaded with address of next instruction
							;R0 now contains the address of SWI instruction
	BIC R1,R1,#0xFF000000	;Clear top 8 bits as lower comment bits contain excepion number
	CMP R1,#0x20			;Comapare R1(passwd exception number) with 0x20 and set CPSR flag accordingly
	MOVEQ R2,R0				;if Zero flag set, then load R0 to R2, else R2 will remian 0
	MOVEQ R3,#10			;Load number 10 in R3 is zero flag set else it remains 0
	MUL R0,R2,R3			;Multiple R1 and R2 and store result in R0
	
	LDMFD SP!,{R1-R12}		;Restore the register back on stack, exclude R0 having final result
	MOVS PC,LR

			