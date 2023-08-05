#モジュールのimport
import os

import numpy as np
import click
import h5py

from .data import *
from .predict import *
from .utils import *

from typing import Union

@click.command()
@click.argument('wsifiles', nargs=-1)
@click.argument('outdir', nargs=1)
@click.option('-s','--scale', type=float, default=1.0)
@click.option('-b','--bg_th', type=float, default=0.05)
@click.option('-m','--modelpath', type=str, default="/wsi/analysis/CellType/work/komura/wisteria/model")
@click.option('-i', '--imgout', is_flag=True)
def main(wsifiles: Union[str, list],
         outdir: str,
         scale: float,
         bg_th: float,
         modelpath: str,
         imgout: bool,
         ):
    """apply segmentation model to patch images

    Args:
        wsifiles (Union[str, list]): WSI file(s) to be analyzed.
        outdir (str): output directory.
        scale (float, optinal): scale factor for the input images. Default to 1.0.
        bg_th (float, optinal): If foreground rate is less than this value, the patch is considered as background and skipped. Default to 0.05.
        modelpath (str, optinal): Diretory of the model files. Default to /wsi/analysis/CellType/work/komura/wisteria/model.
        imgout (bool, optional): Output thumbnail file as well as h5. Default to False.
    """

    models = init_models(modelpath)

    imgsize = 960 * 4

    for wsifile in wsifiles:

        dataset_pos, _ = get_loader(wsifile, imgsize, bg_th, posonly=True)
        dataset, n = get_loader(wsifile, imgsize, bg_th)
        # 推論
        poss = [x[1] for x in dataset_pos]
        xmax, ymax = np.max([x[0]+imgsize for x in poss]) , np.max([x[1]+imgsize for x in poss])
        results = np.zeros((xmax,ymax), np.uint8)

        #予め結果を入れる配列を作って高速化(appendは遅い)
        pr_logits = [np.empty((imgsize, imgsize, len(layer)), 
                            dtype=np.float16) for layer in models]

        print ("# of patch: ", n)
        for k in range(n):
            #画像と位置を取得
            x_tensor, pos, fg = dataset[k]
            x, y = pos
            
            if x_tensor is None:
                results[x:x+imgsize,y:y+imgsize] = 0
            else:
                xsize = x_tensor.shape[2]
                ysize = x_tensor.shape[3]
                pr_final = predict_each_wsi(x_tensor, models, pr_logits, imgsize, fg)
                results[x:x+xsize,y:y+ysize] = pr_final

        print  ("saving h5 file...")
        outfile = os.path.basename(wsifile)

        with h5py.File(f"{outdir}/{outfile}_segout.h5", "w") as h5:
            h5.create_dataset('segmentation_result', data=results) #保存
        print ("done")
        
if __name__ == '__main__':
    main()