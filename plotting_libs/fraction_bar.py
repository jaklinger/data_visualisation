from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from itertools import cycle

def fraction_bar(counts,labels,ax=None,cmap_name="Dark2",
                 legend=True,horizontal=True,title="",number=False):
    
    # Get an axis
    if ax is None:
        figsize = (10,1)
        if not horizontal:
            figsize = (1,10)
            fig,ax = plt.subplots(figsize=figsize)
            
    # Assign colours
    colors = plt.get_cmap(cmap_name).colors
    
    # Make the bars
    x0 = 0
    for n,lab,col in zip(counts,labels,cycle(colors)):
        if horizontal:
            rect = Rectangle((x0,0),x0+n,1,facecolor=col,label=lab)
        else:
            rect = Rectangle((0,x0),1,x0+n,facecolor=col,label=lab)
        ax.add_patch(rect)
        x0 += n
            
    # Set axis limits and set the legend
    ax.axis('off')
    if horizontal:
        ax.set_ylim(0,1)
        ax.set_xlim(0,x0)
        if legend:
            leg = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),title=title)
        else:
            ax.set_xlim(0,1)
            ax.set_ylim(0,x0)
            if legend:
                word_height = 0.012
                n_words = len(counts) + int(title != "")
                box_height = 1 + (word_height*n_words) + word_height*2
                leg = ax.legend(loc='center left', bbox_to_anchor=(-0.15,box_height),title=title)
    # Return
    return ax

# Examples
if __name__ == "__main__":
    fraction_bar([1,2,3,4],("cat","dog","sheep","dinosaur"),title="Animals")
    fraction_bar([1,2,3],("cat","dog","sheep"),title="",horizontal=False,cmap_name="Accent")
