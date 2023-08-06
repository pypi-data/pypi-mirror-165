# Python Simple Loading Bar
This is very simple and customizable loading/progress bar.

### Usage:
```python
from simplebar import loading

    loading(LOADING_BAR_RANGE=50, LOADING_MAX_VAL=100, LOADING_TIME=0.1, LOOP_RANGE=10, 
            fg_text_color="green", bg_text_color="black", text_style="bold",
            fg_value_color="white", bg_value_color="black", value_style="normal",
            symbol_load='#', symbol_bg='.')
 ```
 ### Help:
 ```
LOADING_BAR_RANGE                   # Change length of Loading bar.
LOADING_MAX_VAL                     # Values upto which you want loading bar.
LOADING_TIME                        # Stepwise wait time for loading bar (seconds).
LOOP_RANGE                          # Loop size where you want to use loading e-g for i in range(20), LOOP_RANGE=20.
loop_value                          # iteration value e-g i, for i in range(20).

fg_text_color                       # Symbols text color in the bar.
bg_text_color                       # Symbols background color in the bar.
text_style                          # Style of symbol BOLD,NORMAL.

fg_value_color                      # Value text color at end of bar.
bg_value_color                      # Value background color at end of bar.
value_style                         # Style of value at end of bar BOLD,NORMAL.

symbol_load                         # Symbol to use in loading bar.
symbol_bg                           # Background symbol to use in loading bar.
```