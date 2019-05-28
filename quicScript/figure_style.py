mycolor=['r','g','maroon','lightpink','b','c','m','k','orange','plum','gold','lime','deeppink','chocolate','blueviolet','navy','slategray','deepskyblue','peru','midnightblue','orangered','orchid']
mylinestyle=['-','--','-.',':']
mymarker=['s','p','^','o','v','*','<','>',',']
patterns = (" ","////" , "...." ,"////" , "\\\\\\", "----" , "||||"  , "++++" , "xxxx", "oooo", "O", ".", "*" )

def cm2inch(*tupl):
    inch = 5#2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)

# figure size

LINEof_FIGURE_SIZE=cm2inch(30,25)

LINEof3_FIGURE_SIZE=cm2inch(6,4.5)  # 3figs
LINEof2_FIGURE_SIZE=cm2inch(8,6)    # 2figs
SMALL_FIGURE_SIZE=cm2inch(8,6)      # 1col small fig
BIG_FIGURE_SIZE=cm2inch(12,6)       # double cols big fig
# content size
LINE_WIDTH=1
MARKER_SIZE=5
MARKEREDGE_WIDTH=1
LEGEND_SIZE=5
ERRORLINE_WIDTH=1
ERRORCAP_SIZE=2
# label text size
TITLE_SIZE=10
XY_LABEL_SIZE=8
TICK_LABEL_SIZE=6
TICK_WIDTH=0.5
# legend
LEGEND_EDGE_WIDTH=0.1
# spines width
XY_SPINES_WIDTH=0.5
# grid
GRID_WIDTH=0.1
