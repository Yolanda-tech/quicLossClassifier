import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import os.path
import csv
import time
import figure_style as fs

M=100

def BOX(
        xticklabels,data_set,savepath,bar_name_set,xlabel_name,ylabel_name,title_name='',
        figure_size=fs.LINEof3_FIGURE_SIZE,
        x_tick_spacing=-1,
        y_tick_spacing=-1,
        xmin_limit='None',xmax_limit='None',
        ymin_limit='None',ymax_limit='None',
        grid_on=False
    ):

    # draw the figure
    fig,ax=plt.subplots(figsize=figure_size)

    bar_type=len(bar_name_set)  # bar type
    if bar_type==1 and len(data_set) != 1:
        # case:only one bar,the input one dim to two dim
        data_set=[data_set]
    bars_n=len(xticklabels)
    bar_width=figure_size[0]*1.0/(bars_n*(bar_type+1))

    gap=(bar_type+1)*bar_width  # group's bar gap: 1 bar
    start=bar_width
    end=start+bars_n*gap
    index=np.arange(start,end,gap)

    for i in range(bar_type):
        bp=ax.boxplot(x=data_set[i],
                        positions=index+i*bar_width,
                        widths=bar_width,
                        patch_artist=True#,showfliers=False
        )

        #for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
        #    plt.setp(bp[element], color=fs.mycolor[i])

        for patch in bp['boxes']:
            patch.set(facecolor=fs.mycolor[i])  

        # legend
        ax.legend(bar_name_set,fontsize=fs.LEGEND_SIZE,edgecolor='k').get_frame().set_linewidth(fs.LEGEND_EDGE_WIDTH)
        if grid_on == True:
            ax.grid(linestyle='--', linewidth=fs.GRID_WIDTH)
        ax.set_axisbelow(True)

        # set xticks
        ax.set_xticks(index + bar_width*(bar_type-1)/2.0)
        ax.set_xticklabels(xticklabels)

        #delete the upper and right frame
        ###ax.spines['right'].set_visible(False)
        ###ax.spines['top'].set_visible(False)

        #set x(y) axis (spines)
        ax.spines['bottom'].set_linewidth(fs.XY_SPINES_WIDTH)
        ax.spines['bottom'].set_color('k')
        ax.spines['left'].set_linewidth(fs.XY_SPINES_WIDTH)
        ax.spines['left'].set_color('k')
        ax.spines['right'].set_linewidth(fs.XY_SPINES_WIDTH)
        ax.spines['right'].set_color('k')
        ax.spines['top'].set_linewidth(fs.XY_SPINES_WIDTH)
        ax.spines['top'].set_color('k')

        # set x(y) limits
        if xmin_limit != 'None':
            ax.set_xlim(xmin=xmin_limit)
        if xmax_limit != 'None':
            ax.set_xlim(xmax=xmax_limit)
        if ymin_limit != 'None':
            ax.set_ylim(ymin=ymin_limit)
        if ymax_limit != 'None': 
            ax.set_ylim(ymax=ymax_limit)
    
        #set x(y) label
        plt.xlabel(xlabel_name,fontweight='normal',fontsize=fs.XY_LABEL_SIZE,fontname="Times New Roman",color='k',horizontalalignment='center',x=0.5)#plt.xlabel('Sep 2014                                     Oct 2014',fontweight='semibold',fontsize=16,color='gray',horizontalalignment='left',x=-0.02)
        ax.xaxis.labelpad = 2.5
        plt.ylabel(ylabel_name,fontweight='normal',fontsize=fs.XY_LABEL_SIZE,fontname="Times New Roman",color='k',horizontalalignment='center',y=0.5)
        ax.yaxis.labelpad = 2.5
        plt.title(title_name,fontweight='normal',fontsize=fs.TITLE_SIZE,fontname="Times New Roman",color='k',horizontalalignment='center',x=0.5,y=1)

        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(fs.TICK_LABEL_SIZE)
            tick.label.set_fontweight('normal')#tick.label.set_rotation('vertical')
            tick.label.set_color('k')

        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(fs.TICK_LABEL_SIZE)
            tick.label.set_fontweight('normal')#tick.label.set_rotation('vertical')
            tick.label.set_color('k')

        ax.tick_params(direction='in')

        # tick density
        if x_tick_spacing>=0:
            ax.xaxis.set_major_locator(ticker.MultipleLocator(x_tick_spacing))
        if y_tick_spacing>=0:
            ax.yaxis.set_major_locator(ticker.MultipleLocator(y_tick_spacing))
    
    # save figure
    fig.tight_layout()
    plt.savefig(savepath)
    plt.show()
    plt.close('all')




if __name__=="__main__":


    xticklabels=['4','6','8','10','12','14','16']
    data_set=[[[51.2415, 88.9983, 43.468, 40.9444, 56.4871, 100.0, 26.0504], [37.431, 49.1696, 24.8337, 29.7093, 41.6592, 53.2547, 26.0286], [36.8475, 48.7498, 24.9986, 30.301, 41.9619, 53.7968, 26.0286]], [[56.2106, 51.1341, 40.7401, 48.2009, 43.3968, 37.4365, 35.7738], [36.079, 33.6324, 22.7825, 31.5262, 34.1066, 24.3791, 35.5038], [39.8842, 33.11, 22.1068, 30.0695, 34.3319, 24.9526, 35.5505]], [[39.4151, 81.581, 51.4799, 53.4852, 44.0609, 32.1717, 57.5796], [32.4369, 44.8961, 27.69, 39.6422, 33.8809, 31.7453, 43.396], [32.2099, 45.4773, 28.0276, 39.3627, 33.6487, 32.1627, 43.392]], [[48.1337, 70.6727, 33.8443, 36.4744, 32.6512, 36.1977, 53.5269], [32.2281, 46.1905, 20.3624, 28.7561, 32.1843, 36.5229, 29.5429], [32.13, 46.1905, 19.8319, 28.9119, 32.4602, 36.5229, 29.8328]], [[35.7914, 52.2683, 44.0189, 45.1435, 42.7118, 30.0966, 77.2764], [31.8662, 38.7717, 25.4177, 28.9898, 29.4042, 30.0966, 54.5209], [31.4141, 39.4722, 23.3792, 29.7202, 29.2937, 29.7897, 54.6389]], [[40.9934, 64.4452, 44.1212, 32.0244, 53.8973, 30.5929, 39.4128], [40.9934, 39.734, 24.7894, 24.6057, 28.9555, 30.4475, 38.86], [40.9934, 39.2271, 23.9595, 24.5259, 28.9066, 30.1617, 38.9724]], [[42.4281, 50.1449, 46.4964, 66.1724, 31.0318, 38.9363, 39.7988], [28.6429, 37.6415, 24.1894, 35.3893, 27.3382, 38.368, 31.82], [27.2707, 35.8705, 24.226, 35.6701, 27.3929, 38.317, 31.801]], [[43.9519, 48.346, 47.2343, 37.2826, 57.2301, 31.54, 55.7391], [26.3741, 26.7776, 27.3608, 23.3185, 36.4318, 23.7999, 34.6251], [27.8743, 27.0322, 27.3394, 23.3195, 36.4318, 24.071, 35.527]], [[57.6572, 85.2004, 48.464, 45.9814, 63.8188, 65.8439, 37.4531], [36.5314, 54.0726, 26.116, 26.9842, 42.3767, 35.2138, 37.2064], [40.5081, 54.135, 26.116, 27.8904, 42.3393, 36.5469, 37.3604]], [[50.5862, 83.9462, 30.8219, 56.8895, 44.0616, 34.735, 48.9177], [38.941, 45.124, 21.4263, 30.854, 30.7765, 33.9958, 43.7837], [38.4712, 45.4034, 21.0001, 30.7289, 30.8619, 34.101, 43.8543]]]
    data_set_2=[[],[],[]]
    for an in range(3):
        for k in range(0,0+7,1):
            bwu_temp=[]
            for test_id in range(0,0+10,1):
                bwu_temp.append(data_set[test_id][an][k])
            data_set_2[an].append(bwu_temp)

    ###print(data_set_2)

    bar_name_set=['LP','LBFP','FAFP']
    savepath='.\\temp.pdf'
    xlabel_name='pods'
    ylabel_name='Max Bandwidth Utilization'
    BOX(xticklabels,data_set_2,savepath,bar_name_set,xlabel_name,ylabel_name)


    '''
    bar_type=len(data_set)

    # draw the figure
    fig,ax=plt.subplots( )

    index=[10,20,30]

    for i in range(bar_type):
        for j in range(len(index)):
            index[j]=index[j]+1
        print(index)
        rects=ax.boxplot(positions=index,x=data_set[i])
    ax.set_xlim(xmin=0)

    plt.show()
    plt.close('all')
    '''