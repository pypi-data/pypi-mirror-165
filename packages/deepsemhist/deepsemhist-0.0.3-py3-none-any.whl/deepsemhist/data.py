from typing import List, Any
import numpy as np
from PIL import Image

from skimage.filters import threshold_otsu, gaussian
from skimage import color

import tifffile as t
import zarr

import torch
from torch.utils.data import Dataset as BaseDataset
from torchvision import transforms

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

class PatchDataset(BaseDataset):
    ##初期化の関数
    def __init__(
            self,
            imgfiles,
            scale,
    ):
        div = 32
        self.scale = scale

        self.imgfiles = imgfiles
        self.origimgsize = np.array(Image.open(self.imgfiles[0])).shape
        self.ox = self.origimgsize[0]
        self.oy = self.origimgsize[1]
        resized = (int(self.ox * self.scale), int(self.oy * self.scale))
        pad_px = ((((resized[0]//div+1)*div-resized[0])%div)//2)
        pad_py = ((((resized[1]//div+1)*div-resized[1])%div)//2)

        self.aug = transforms.Compose([
            transforms.Resize(resized),
            transforms.Pad(padding=[pad_px, pad_py],
                        padding_mode="reflect"),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
        ])

    ## 呼び出されるとパッチ画像とその位置を返す
    def __getitem__(self, i):
        # read data
        x = Image.open(self.imgfiles[i]).convert('RGB')
        x = transforms.functional.to_tensor(x)
        x = x.to(DEVICE).half()
        x = self.aug(x)
        
        return x

    def __len__(self):
        return len(self.imgfiles)

    def get_orgimagesize(self):
        return self.origimgsize

class WSIDataset(BaseDataset):
    ##初期化の関数
    def __init__(
            self,
            wsifile,
            imgsize=960*6,
            bg_th=0.05,
            posonly=False,
    ):
        self.tops = []
        self.posonly=posonly
        self.bg_th = 0.05
        
        self.wsi = self.OpenSlide_zarr(wsifile)

        # WSIの画像サイズ。(横(x), 縦(y))になっていることに注意。
        dim = self.wsi[0].shape[:2]
        self.zl = self.wsi[0].shape[0]//self.wsi[1].shape[0]
        self.maxl = len(self.wsi) - 1
        print (f"WSI size: {dim}")
        
        # 推論を行う入力画像のサイズ(defaultは7680 x 7680px)
        self.sizes = (imgsize, imgsize)

        #確認用サムネイル
        self.sc = self.maxl
        
        thumb = self.read_region_zarr((0,0),(dim[0]//(self.zl**self.sc) , dim[1]//(self.zl**self.sc)), self.sc)

        #大津の二値化
        self.otsu_thresh = threshold_otsu(color.rgb2gray(thumb))
        print("Otsu threshold : ", self.otsu_thresh)
        
        ##切り出す入力画像のWSI内における座標(左上と右下）をself.topsに格納
        ## オーバーラップ無し => 1/2 overlapさせるならここを変更 > 遠藤君
        for x in range(0, dim[0] , self.sizes[0]):
            for y in range(0, dim[1], self.sizes[1]):
                self.tops.append([x, y])

        print (f"number of candidate regions : {len(self.tops)}")
        
        self.ids = self.tops
        self.aug = transforms.Compose([
            transforms.Normalize(mean=[124., 116., 104.],
                                std=[58.6, 57.3, 57.6])  #https://teratail.com/questions/234027
        ])       

    def OpenSlide_zarr(self, wsifile):
        obj = t.imread(wsifile, aszarr=True)
        z = zarr.open(obj, mode='r')
        return z

    def read_region_zarr(self, region, size, level=0):
        if len(self.wsi[0].shape) == 3:
            return self.wsi[level][region[0]:(region[0]+size[0]),region[1]:(region[1]+size[1]),:]
        elif len(self.wsi[0].shape) == 4:
            focus = int(self.wsi[0].shape[0] // 2)
            return self.wsi[level][focus, region[0]:(region[0]+size[0]),region[1]:(region[1]+size[1]),:]


    ## 呼び出されるとパッチ画像とその位置を返す
    def __getitem__(self, i):
        # read data
        pos = (self.tops[i][0], self.tops[i][1]) #__init__で計算したWSI内における座標

        if self.posonly:
            return None, pos, None

        # 背景判定用に縮小画像を利用
        sc = 4 if self.zl == 2 else 2
        small_image = self.read_region_zarr((self.tops[i][0]//(self.zl**sc), self.tops[i][1]//(self.zl**sc)), 
                                            [x//(self.zl**sc) for x in self.sizes], sc)  
        print(f"region size : {small_image.shape}")
        if small_image.shape[0] * small_image.shape[1] == 0:
            return None, pos, None
        
        #背景ならNone
        #backgroundは白なので不等号は逆になる
        fg = color.rgb2gray(small_image) < self.otsu_thresh

        fg_ratio = np.count_nonzero(fg) / fg.shape[0] / fg.shape[1]
        if  fg_ratio <= self.bg_th:
            print (f"skip background : {pos}:{fg_ratio}")
            return None, pos, None
        else:
            print (f"foreground : {pos}")
            image = self.read_region_zarr((self.tops[i][0], self.tops[i][1]), self.sizes, 0)       
            fg = gaussian(color.rgb2gray(image),(7,7), truncate=3.5) < self.otsu_thresh
            fg = np.array(fg,dtype = np.int64)
            image = self.preprocessing_fn(image.astype('float64')) #前処理
            return image, pos, fg

    def __len__(self):
        return len(self.ids)
    
    ## 入力画像の前処理関数
    def preprocessing_fn(self, x):

        ## Color normalization (訓練データと同じRGBの平均、分散になるように)
        #for i in range(3):
        #    x[:,:,i] *=  self.cstat['std'][i]  
        #    x[:,:,i] +=  self.cstat['mean'][i]

        ## 値を0 ~ 255におさめる
        #x[x>255] = 255
        #x[x<0] = 0    

        ## GPU => half precision (高速化のため)
        x = torch.from_numpy(x).to(DEVICE).half()
        x = x.permute(2,0,1)

        ## (px,py,rgb)の場合は(1,px,py,rgb)のように1次元目がbatchになるように変換
        if len(x.shape) == 3:
            x = x.unsqueeze(0)

        x = self.aug(x)
        
        return x
        

## ↑のデータセットを返す
def get_loader(wsifile, imgsize, bg_th, posonly=False):
    test_dataset = WSIDataset(
        wsifile, imgsize, bg_th=bg_th, posonly=posonly,
    )

    return test_dataset, len(test_dataset)