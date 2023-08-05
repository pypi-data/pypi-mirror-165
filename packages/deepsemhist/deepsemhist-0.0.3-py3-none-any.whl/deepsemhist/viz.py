from .utils import *
from typing import Any, List, Union
import matplotlib.pyplot as plt

from .wsi_class import *

class WSI_Viz(WSI_Base):
    def __init__(self,
                 h5file: str,
                 wsifile: Union[str, None] = None,
                 ) -> None:
        """Initialize an object for visualization of segentation results.

        Args:
            h5file (str): H5 file output by segslide.
            wsifile (Union[str, None], optional): Corresponding WSI file (e.g. ndpi or svs). Defaults to None.
        """
        super().__init__(h5file, wsifile)



    def show_thumb(self):
        """plot thumbnail of segmentation results (and H&E WSI if wsifile exists.)
        """
        seg_thumb = colorlabel(self.segdata[::100,::100])

        if self.wsifile is not None:
            he_thumb = self._read_thumb()
            plt.subplot(211)
            plt.imshow(he_thumb)
            plt.axis('off')

            plt.subplot(212)
            plt.imshow(seg_thumb)
            plt.axis('off')

        else:
            plt.imshow(seg_thumb)
            plt.axis('off')

    def show_legend(self, 
                    outfile: Union[str,None] = None,
                    ):
        """show correspondence between color and cell/tissue type.

        Args:
            outfile (Union[str,None], optional): output image file. Defaults to None.
        """
        plt.rcParams['figure.figsize'] = 20,1 #figure size 
        _, ax = plt.subplots()
        colorlist = self.cmap2
        cell = ["stroma", 
                "SM/MF", 
                "epithelium", 
                "leucocyte", 
                "endothelium", 
                "RBC", 
                "lymphocyte", 
                "plasma cell", 
                "myeloid cell"]
        x = np.arange(1, 10)
        height = np.repeat(1, 9)
        ax.bar(x, height, color=colorlist, tick_label=cell, align="center")
        plt.tick_params(labelsize=14)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_yaxis().set_ticks([])
        plt.subplots_adjust(bottom=0.4) 

        if outfile is not None:
            plt.savefig(outfile)

    def _read_thumb(self):
        return self.wsi[self.maxl]
