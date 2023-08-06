from time import sleep

class Color:
    
    """
    TEXT COLOR	CODE	TEXT STYLE	CODE	BACKGROUND COLOR	CODE
    Black	    30	    No effect	0	    Black	                40
    Red	        31	    Bold	    1	    Red 	                41
    Green	    32	    Underline	2	    Green	                42
    Yellow	    33	    Negative1	3	    Yellow	                43
    Blue	    34	    Negative2	5	    Blue	                44
    Purple	    35			                Purple	                45
    Cyan	    36			                Cyan	                46
    White	    37			                White	                47

    1;32;40m , 1=Style, 32=Text color, 40=Background color
    """
    
    default = '\033[0;0;0m'
    # green   = '\033[1;32;40m'
    # white   = '\033[1;37;40m'
    # yellow  = '\033[1;33;40m'
    # red     = '\033[1;31;40m'

class Fg(Color):

    BLACK   = '30'
    RED     = '31'
    GREEN   = '32'
    YELLOW  = '33'
    BLUE    = '34'
    MAGENTA = '35'
    CYAN    = '36'
    WHITE   = '37'

class Bg(Color):

    BLACK   = '40'
    RED     = '41'
    GREEN   = '42'
    YELLOW  = '43'
    BLUE    = '44'
    MAGENTA = '45'
    CYAN    = '46'
    WHITE   = '47'

class Style(Color):

    NORMAL    = '0'
    BOLD      = '1'
    UNDERLINE = '2'


def upper_case(color):
    return color.upper()

def color_string(fg_color, bg_color, style):
    return '\033[{0};{1};{2}m'.format(style, fg_color, bg_color)

def loading(LOADING_BAR_RANGE=50, LOADING_MAX_VAL=100, 
            LOADING_TIME=0.1, LOOP_RANGE=10, loop_value=0, 
            fg_text_color="white", bg_text_color="black", text_style="NORMAL",
            fg_value_color="white", bg_value_color="black", value_style="NORMAL",
            symbol_load='#', symbol_bg='.'):
    
    LOADING_BAR_RANGE                   # Change length of Loading bar
    LOADING_MAX_VAL                     # Values upto which you want loading bar
    LOADING_TIME                        # Stepwise wait time for loading bar (seconds)

    fg_text_color = upper_case(fg_text_color)
    bg_text_color = upper_case(bg_text_color)
    text_style = upper_case(text_style)
    fg_value_color = upper_case(fg_value_color)
    bg_value_color = upper_case(bg_value_color)
    value_style = upper_case(value_style)

    symbol_1_range = round(LOADING_BAR_RANGE/LOOP_RANGE * loop_value)
    symbol_2_range = round(LOADING_BAR_RANGE - LOADING_BAR_RANGE/LOOP_RANGE * loop_value)
    value_range = round(LOADING_MAX_VAL/LOOP_RANGE * loop_value)

    # Add Color.color before the string and Color.default after string for no effects.
    fg_text_color, bg_text_color, text_style = getattr(Fg, fg_text_color),getattr(Bg, bg_text_color),getattr(Style, text_style)
    fg_value_color, bg_value_color, value_style= getattr(Fg, fg_value_color),getattr(Bg, bg_value_color),getattr(Style, value_style)
    
    text_format = color_string(fg_text_color, bg_text_color, text_style)
    value_format = color_string(fg_value_color, bg_value_color, value_style)

    bar = f'{text_format}{ symbol_load * symbol_1_range}{Color.default}{symbol_bg * symbol_2_range}'
    value = f'{value_format}{value_range} % {Color.default}'  
    load = '[ {0} ] {1}'.format(bar, value)
    
    print(load, end="\r")
    
    sleep(LOADING_TIME)


def main():

    """
    loading(LOADING_BAR_RANGE=50, LOADING_MAX_VAL=100, LOADING_TIME=0.1, LOOP_RANGE=10, 
            fg_text_color="green", bg_text_color="black", text_style="bold",
            fg_value_color="white", bg_value_color="black", value_style="normal",
                symbol_load='#', symbol_bg='.')
    
    LOADING_BAR_RANGE                   # Change length of Loading bar
    LOADING_MAX_VAL                     # Values upto which you want loading bar
    LOADING_TIME                        # Stepwise wait time for loading bar (seconds)
    LOOP_RANGE                          # Loop size where you want to use loading e-g for i in range(20), LOOP_RANGE=20
    loop_value                          # iteration value e-g i, for i in range(20)
    
    Colors                              # Red, green, white, yellow
    symbol                              # Symbole to use in loading bar
    """
    
    # Example loop, where we will use the loading bar
    LOOP_SIZE = 40
    for i in range(LOOP_SIZE):
        # some task
        loading(50, 10, 0.1, LOOP_SIZE, i+1,
                fg_text_color="green", bg_text_color="black", text_style="bold",
                fg_value_color="white", bg_value_color="black", value_style="normal",
                symbol_load='#', symbol_bg='.')
    

if __name__ == "__main__":
    main()