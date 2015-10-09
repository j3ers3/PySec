import random
import mycolor

def main_header():

    header_1 = mycolor.color.cyan + """
      1000101100000000111111111111111000000011111110000
      0011111111000000011111101010101010101010000000000
      1111111111111111111111111000000000001010000000111
      0011110000001010101011111111111010101011111111111
      1111110011110000011111111111111111100000000111111
				00001111111
				00001111110
				11000000111
		0 0		01010101010
				01111111010
				11111100101
				00000001111101010101011
				11111111110001111010111

      11111111111110000000
      00000101010101111111""" + mycolor.color.end

    header_2 = mycolor.color.green + r"""
      MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
      MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
      M						      M
      M						      M
      M						      M
      M		    Whois's Framework   	      M
      M						      M
      M						      M
      MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
      MMMMMMMMMMMMMM			 MMMMMMMMMMMMMM
      MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM""" + mycolor.color.end

    header_3 = mycolor.color.purple + r"""
      ooooooooooooooooooooooooooooooooooooooooooooooooo
      VVVV##					 ##VVVV
       V	|\\\\"		        |\\\\'       V
                |___|                   |____|
	
			____________
			    |  |
			    |  |
			    UUUU
          ;					  ;  
	   ' \_________________________________'//
	     ; 0000000000000000000000000000000;
	       . \\000000000000000000000000//
	         ------------------------""" + mycolor.color.end

    header_4 = mycolor.color.darkcyan + """
                               ,;        ,;                            
         .               f#i       f#i .    .      t                  
        Ef.           .E#t      .E#t  Di   Dt     Ej              
        E#Wi         i#W,      i#W,   E#i  E#i    E#, t      .DD. 
        E#K#D:      L#D.      L#D.    E#t  E#t    E#t EK:   ,WK. L
        E#t,E#f.  :K#Wfff;  :K#Wfff;  E#t  E#t    E#t E#t  i#D :K
        E#WEE##Wt i##WLLLLt i##WLLLLt E########f. E#t E#t j#f  
        E##Ei;;;;. .E#L      .E#L     E#j..K#j... E#t E#tL#i    
        E#DWWt       f#E:      f#E:   E#t  E#t    E#t E#WW,       
        E#t f#K;      ,WW;      ,WW;  E#t  E#t    E#t E#K:    ee;.     
        E#Dfff##E,     .D#;      .D#; f#t  f#t    E#t ED.           
        jLLLLLLLLL;      tt        tt  ii   ii    E#t t               
	
    	""" + mycolor.color.end	

    header_5 = mycolor.color.blue + r"""
	 __________________________
        < whoami and u >
         --------------------------
                \   ^__^			---
                 \  (oo)\_______		|  \
                    (__)\       )\/\/		| o \
                        ||----w |		|    \
                        ||     ||		|-----\
						|
	---------E@###------------%%%###--------|

	E%###$%%%%%%$$##$%%^^^$$$$$$%#$ETTTE##33
	---------------------------------------||||
     """ + mycolor.color.end

    logo = [header_1,header_2,header_3,header_4,header_5]
    bann = random.choice(logo)
    print bann

