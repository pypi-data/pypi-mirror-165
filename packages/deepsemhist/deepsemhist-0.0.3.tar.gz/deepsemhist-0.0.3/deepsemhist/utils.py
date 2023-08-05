import numpy as np
import copy
from skimage import color

def colorlabel(subimg: np.ndarray,
               ) -> np.ndarray:
        """Create color coded (RGB) image from 2-dimensitonal class matrix.

        Args:
                subimg (np.ndarray): input 2-dimensional class matrix.

        Returns:
                np.ndarray: color coded (RGB) image.
        """
        cmap2 = np.array([(136, 139, 161),
                (255, 122, 252),
                (0, 121, 50),
                (252, 189, 3),
                (59, 181, 255),
                (240, 3, 20),
                (245, 255, 18),
                (150, 15, 252),
                (120, 240, 41),])/255
        
        climg = copy.deepcopy(subimg)
        climg = np.insert(climg, 0, 0, axis=0)
        climg[0,:10] = [0,1,2,3,4,5,6,7,8,9]
        climg = color.label2rgb(climg, bg_label=0, colors=cmap2)
        return (climg[1:,:,:]*255).astype(np.uint8)