import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import figure_style as fs

def subBoxPlot(path,connstr,typename,delay,loss,data0,data1):
    xlabel_name='Loss(%)'
    ylabel_name='PLT(s)'
    title_name='Delay=%sms(%s)' %(delay,connstr)

    data0 = map(eval, data0)
    data1 = map(eval, data1)
    data = [data0,data1]
    bar_type = len(data)

    #print delay,loss,data0,data1
    xticks = loss
    bars_n = len(xticks)

    figure_size=fs.LINEof_FIGURE_SIZE
    spine_width=.8
    spine_color="b"
    fig,ax = plt.subplots(figsize=figure_size)  

    bar_width=figure_size[0]*1.0/(bars_n*(bar_type+1))
    gap=(bar_type+1)*bar_width*0.95  # group's bar gap: 1 bar
    start=bar_width
    end=start+bars_n*gap
    index=np.arange(start,end,gap)
    #print index
    bp=[]
    for i in range(bar_type):
        bp.append(ax.boxplot(x=data[i],
                   positions=index+i*bar_width,
                   widths=bar_width,
                   patch_artist=True))

        for patch in bp[i]['boxes']:
            patch.set(facecolor=fs.mycolor[i],linewidth=spine_width,hatch = '' if i==0 else "///" )
        '''
        ax.spines['bottom'].set_linewidth(spine_width)
        ax.spines['bottom'].set_color(spine_color)
        ax.spines['left'].set_linewidth(spine_width)
        ax.spines['left'].set_color(spine_color)
        ax.spines['right'].set_linewidth(spine_width)
        ax.spines['right'].set_color(spine_color)
        ax.spines['top'].set_linewidth(spine_width)
        ax.spines['top'].set_color(spine_color)'''

        #ax.legend(typename,fontsize=15)#,fontsize=fs.LEGEND_SIZE).get_frame().set_linewidth(fs.LEGEND_EDGE_WIDTH)

        ax.set_xticks(index + bar_width*(bar_type-1)/2.0)
        ax.set_xticklabels(xticks,fontsize=15)
        ax.set_yticklabels([0,0.5,1,1.5,2,2.5],fontsize=15)
        
        plt.xlabel(xlabel_name,horizontalalignment='center',x=0.5,fontsize=15)#plt.xlabel('Sep 2014   fontweight='normal',fontsize=fs.XY_LABEL_SIZE,                                  Oct 2014',fontweight='semibold',fontsize=16,color='gray',horizontalalignment='left',x=-0.02)
        #ax.xaxis.labelpad = 2.5
        plt.ylabel(ylabel_name,horizontalalignment='center',y=0.5,fontsize=15)#,fontweight='normal',fontsize=fs.XY_LABEL_SIZE
        #ax.yaxis.labelpad = 2.5
        #plt.title(title_name,horizontalalignment='center',x=0.5,y=1,fontsize=12)

        '''
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(fs.TICK_LABEL_SIZE)
            tick.label.set_fontweight('normal')#tick.label.set_rotation('vertical')
            #tick.label.set_color('k')

        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(fs.TICK_LABEL_SIZE)
            tick.label.set_fontweight('normal')#tick.label.set_rotation('vertical')
            #tick.label.set_color('k')'''
        ax.set_ylim(ymin=0,ymax=2500)
        ax.tick_params(direction='in')

    ax.legend([bpi["boxes"][0] for bpi in bp], typename, loc='upper right',fontsize=15)
    plt.grid(axis='y')
    plt.savefig(path)
    #plt.show()
    plt.close()

def boxPlot(keys,path,filename,dictData):
    filePath = os.path.join(path, filename)
    columns = ['delay','loss','firstConnAll_0','firstConnAll_1', 'subsequentConnAll_0', 'subsequentConnAll_1']
    df_wine = pd.read_csv(filePath, usecols=columns, low_memory=False)
    df_wine['loss'] = pd.to_numeric(df_wine['loss'],errors='coerce') 
    df_wine.sort_values("loss",inplace=True)

    delayValue = list(set(df_wine['delay']))
    for delay in delayValue:
        data = df_wine.loc[df_wine['delay']==delay]
        if "_nc" in keys[0]:
            legend=["Without loss classifier","With loss classifier"]
        else:
            legend=["With loss classifier","Without loss classifier"]

        savefile='firstConnAll_delay%s.pdf' %delay
        savepath=os.path.join(path, savefile)
        connStr="First connection"
        subBoxPlot(savepath,connStr,legend,delay,data['loss'].values,data['firstConnAll_0'].values,data['firstConnAll_1'].values)
        
        savefile='subsequentConnAll_delay%s.pdf' %delay
        savepath=os.path.join(path, savefile)
        connStr="Subsequent connection"
        subBoxPlot(savepath,connStr,legend,delay,data['loss'].values,data['subsequentConnAll_0'].values,data['subsequentConnAll_1'].values)


    #df=pd.DataFrame()


    #df.boxplot()
    #plt.show()

    '''plt.boxplot(x=df.values,labels=df.columns,whis=1.5)
    plt.show()'''