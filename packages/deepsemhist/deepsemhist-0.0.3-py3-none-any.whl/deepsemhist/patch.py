from .utils import *
from typing import Any, List, Union, Dict
from .wsi_class import *

import os

class WSI_Patch:
    def __init__(self,
                 h5file: str,
                 wsifile: Union[str, None] = None,
                 ) -> None:
        """Initialize an object for analysis of segentation results.

        Args:
            h5file (str): H5 file output by segslide.
            wsifile (Union[str, None], optional): Corresponding WSI file (e.g. ndpi or svs). Defaults to None.
        """
        super().__init__(h5file, wsifile)

    def save_patch(self,
                   outdir, 
                   patch_size: int = 1024, 
                   filter_less: Union[Dict, None] = None, 
                   filter_more: Union[Dict, None] = None,
                   ):
        h, w = self.segdata.shape
        for x in range(0, w, patch_size):
            for y in range(0, h, patch_size):
                d = self.segdata[y:y+patch_size:2, x:x+patch_size:2]
                filter = self._filter(filter_less, filter_more)
                epi_area = np.sum(d==3)/d.size #上皮の量
                if epi_area >= 0.2: # patch切り出し
                    outhe = os.path.join(outdir, f"{x}_{y}_{patch_size}.png")
                    if not os.path.exists(outhe):
                        he = wsi.read_region((x,y),1,(patch_size//2,patch_size//2))
                        he_npy = np.array(he)
                        he_npy[d!=3] = 0
                        he = Image.fromarray(he_npy)
                        he.save(outhe)
    
    
