from .utils import *
from typing import Any, List, Union
import matplotlib.pyplot as plt
import h5py
import tifffile as t
import zarr

class WSI_Base:
    def __init__(self,
                 h5file: str,
                 wsifile: Union[str, None] = None,
                 ) -> None:
        """Initialize an object

        Args:
            h5file (str): H5 file output by segslide.
            wsifile (Union[str, None], optional): Corresponding WSI file (e.g. ndpi or svs). Defaults to None.
        """
        self.h5file = h5file
        self.h5obj = h5py.File(self.h5file,'r')
        self.segdata = self.h5obj['segmentation_result']

        self.wsifile = wsifile
        if wsifile is not None:
            self.read_wsi(wsifile)

        self.cmap2 = np.array([(136, 139, 161),
                (255, 122, 252),
                (0, 121, 50),
                (252, 189, 3),
                (59, 181, 255),
                (240, 3, 20),
                (245, 255, 18),
                (150, 15, 252),
                (120, 240, 41),])/255

    def read_wsi(self, 
                 wsifile: str,
                 ):
        """read WSI file corresponding to segmentation result. 

        Args:
            wsifile (str): WSI file (e.g. ndpi or svs)
        """
        self.wsifile = wsifile
        self._OpenSlide_zarr()
        self.dim = self.wsi[0].shape[:2]
        self.zl = self.wsi[0].shape[0]//self.wsi[1].shape[0]
        self.maxl = len(self.wsi) - 1

    def _OpenSlide_zarr(self):
        obj = t.imread(self.wsifile, aszarr=True)
        self.wsi = zarr.open(obj, mode='r')

    def _read_region_zarr(self, region, size, level=0):
        if len(self.wsi[0].shape) == 3:
            return self.wsi[level][region[0]:(region[0]+size[0]),region[1]:(region[1]+size[1]),:]
        elif len(self.wsi[0].shape) == 4:
            focus = int(self.wsi[0].shape[0] // 2)
            return self.wsi[level][focus, region[0]:(region[0]+size[0]),region[1]:(region[1]+size[1]),:]

    def _read_thumb(self):
        return self.wsi[self.maxl]
