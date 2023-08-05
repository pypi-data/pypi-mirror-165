#モジュールのimport
import os
from tkinter import W
from PIL import Image

import numpy as np
import click

from .data import *
from .predict import *
from .utils import *


from torchvision import transforms
from torch.utils.data import DataLoader

from typing import Union

@click.command()
@click.argument('inputfiles', nargs=-1)
@click.argument('outdir', nargs=1)
@click.option('-s','--scale', type=float, default=1.0)
@click.option('-m','--modelpath', type=str, default="/wsi/analysis/CellType/work/komura/wisteria/model")
@click.option('-i', '--imgout', is_flag=True)
def main(inputfiles: Union[str, list],
         outdir: str,
         scale: float,
         modelpath: str,
         imgout: bool,
         ):
    """apply segmentation model to patch images

    Args:
        inputfiles (Union[str, list]): image file(s) to be analyzed.
        outdir (str): output directory.
        scale (float, optinal): scale factor for the input images. Default to 1.0.
        modelpath (str, optinal): Diretory of the model files. Default to /wsi/analysis/CellType/work/komura/wisteria/model.
        imgout (bool, optional): Output image file as well as npy. Default to False.
    """

    models = init_models(modelpath)

    bs=1

    # 推論
    dataset = PatchDataset(inputfiles, scale)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=False)

    orgimgsize = dataset.get_orgimagesize()
    ox = int(orgimgsize[0]*scale)
    oy = int(orgimgsize[1]*scale)
    back_transform = transforms.Compose([
        transforms.CenterCrop((ox, oy)),
    ])

    for i in range(int(np.ceil(len(inputfiles)/bs))):
        print("process", inputfiles[i])
        x_tensor = next(iter(dataloader))
        ds = x_tensor.shape[0]
        ifiles = inputfiles[(i*bs):(i*bs+ds)]

        pr_final = predict_each(x_tensor, models, ox, oy, back_transform)

        print ("writing results...")
        for j in range(pr_final.shape[0]):
            if imgout:
                cfile = outdir+"/"+os.path.basename(ifiles[j])+"_mask.png"
                assert cfile != ifiles[j]
                cimg = colorlabel(pr_final[j])
                Image.fromarray(cimg).save(cfile)

            ofile = outdir+"/"+os.path.basename(ifiles[j])+"_mask.npy"
            assert ofile != ifiles[j]
            np.save(ofile, pr_final[j]) #保存

        
if __name__ == '__main__':
    main()