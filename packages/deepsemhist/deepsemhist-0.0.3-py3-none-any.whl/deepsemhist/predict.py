import torch
import numpy as np
import os
from typing import List, Any, Union

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
print("device name", torch.cuda.get_device_name(0))

## 各細胞種のsegmentation modelをloadして返す
def load_model(ab: str, 
               run_uuid: str, 
               modelpath: str,
               ) -> Any:
    """load CNN for segmentation.

    Args:
        ab (str): Antibody (tissue/cell type).
        run_uuid (str): UUID in MLFlow.
        modelpath (str): Model file path.

    Returns:
        Any: model.
    """
    best_model = torch.load(os.path.join(modelpath, f"{ab}_{run_uuid}.pth")).half().to(DEVICE)

    return best_model


def get_pred(x_tensor: torch.HalfTensor, 
             best_model: torch.nn.Module , 
             transform: Any = None,
             ) -> List[Union[torch.HalfTensor, None]]:
    """Prediction by one segmentation model.

    Args:
        x_tensor (torch.HalfTensor): input data tensor.
        best_model (torch.nn.Module): segmentation model.
        transform (Any, optional): transform function applied after prediction. Defaults to None.

    Returns:
        List[torch.HalfTensor, None]: Prediction result and None.
    """
    best_model.eval()
    with torch.no_grad():
        pr_mask = best_model.predict(x_tensor)
        if transform is not None:
            pr_mask = transform(pr_mask)
    #best_model = best_model.cpu()
    pr_logit = (pr_mask.squeeze().cpu().numpy())
    return (pr_logit, None)

def get_encoding(pr_logits: torch.HalfTensor, 
                 layer: Any, 
                 axis: int = 3, 
                 offset: int = 0,
                 ) -> torch.HalfTensor:
    """If the logit is the largest for n models and exceeds 0.5, insert the number corresponding to that model.

    Args:
        pr_logits (torch.HalfTensor): Prediction results by n models.
        layer (Any): Cell/Tissue layer.
        axis (int, optional): Axis for max. 2 for WSI segmentation and 3 for patch image segmentation. Defaults to 3.
        offset (int, optional): offset to specify the cell/tissue type. Defaults to 0.

    Returns:
        torch.HalfTensor: Updated prediction result.
    """
    maxcellvalues = np.max(pr_logits, axis=axis) #各細胞について最も大きな予測値を取得

    #最も大きな予測値を持つ場合のみTrue、それ以外はFalseにする
    pr_logit_layer = (pr_logits - np.stack([maxcellvalues]*len(layer), axis=axis) ) == 0
    
    #最も大きな予測値のみ残して、それ以外は0にする
    pr_logit_onlymax = pr_logits * pr_logit_layer
    #最も大きな予測値が >0 (prob >50%)ならTrue、それ以外はFalse
    pr_logit_onlymax = pr_logit_onlymax > 0 

    #pr_finalは最終的な予測結果(最大値かつprob >.5の細胞種の値(k+1+offset)を格納)
    pr_final = np.zeros(pr_logit_onlymax.shape[:-1], dtype=np.int64)
    for k in range(pr_logit_onlymax.shape[-1]): #iteration over channels
        if axis == 3:
            pr_final += (k+1+offset)*pr_logit_onlymax[:,:,:,k]
        else:
            pr_final += (k+1+offset)*pr_logit_onlymax[:,:,k]
    return pr_final

# 予測結果を上書きする
def update_pr(pr_final: torch.HalfTensor,
              pr_final_tmp: torch.HalfTensor,
              ) -> torch.HalfTensor:
    """Overwrite prediction result.

    Args:
        pr_final (torch.HalTensor): Current prediction result.
        pr_final_tmp (torch.HalfTensor): Prediction result for new cell/tissue type.

    Returns:
        torch.HalfTensor: Updated prediction result.
    """
    pr_final[pr_final_tmp>0] = pr_final_tmp[pr_final_tmp>0]
    
    return pr_final

def predict_each(x_tensor: torch.HalfTensor,
                 models: List[Any],
                 ox: int,
                 oy: int,
                 transform: Any,
                 ) -> torch.HalfTensor:
    """Prediction by all the models.

    Args:
        x_tensor (torch.HalfTensor): input data tensor.
        models (List[Any]): list of models.
        ox (int): (expanded) image height.
        oy (int): (expanded) image width.
        transform (Any): transform function applied after prediction.

    Returns:
        torch.HalfTensor: Final prediction result.
    """
    #まず大津でforegroundを1にする
    #pr_final = fg
    #細胞種グループ(layer)ごとに予測 
    #予め結果を入れる配列を作って高速化(appendは遅い)
    celltypes = []
    offset = 1

    ds = x_tensor.shape[0]

    pr_logits = [np.empty((ds, ox, oy, len(layer)), 
                        dtype=np.float16) for layer in models]

    pr_final = np.zeros((ds, ox, oy), dtype=np.uint8)
    for i, layer in enumerate(models):
        for j, (cell, ens_models) in enumerate(layer): 
            celltypes.append(cell) #細胞種名
            for q, model in enumerate(ens_models):
                if q == 0:
                    pr_logit, _ = get_pred(x_tensor, model, transform) #予測
                else:
                    pr_logit_tmp, _ = get_pred(x_tensor, model, transform) #予測
                    pr_logit = pr_logit + pr_logit_tmp
            pr_logits[i][:,:,:,j] = pr_logit
        pr_final_tmp = get_encoding(pr_logits[i], layer, offset = offset)
        offset += len(layer)

        pr_final = update_pr(pr_final, pr_final_tmp)

    return pr_final

def predict_each_wsi(x_tensor: torch.HalfTensor,
                     models: List[Any],
                     pr_logits: np.ndarray,
                     imgsize: int,
                     fg: Any,
                     ) -> torch.HalfTensor:
    """Prediction by all the models (for WSI analysis.)

    Args:
        x_tensor (torch.HalfTensor): input data tensor.
        models (List[Any]): list of models.
        pr_logits (np.ndarray): current prediction results (logit.)
        imgsize (int): image size.
        fg (Any): foreground.

    Returns:
        torch.HalfTensor: Final result.
    """
    celltypes = []
    offset = 1

    xsize = x_tensor.shape[2]
    ysize = x_tensor.shape[3]
    #まず大津でforegroundを1にする
    pr_final = fg
    #細胞種グループ(layer)ごとに予測 
    for i, layer in enumerate(models):
        for j, (cell, ens_models) in enumerate(layer): 
            celltypes.append(cell) #細胞種名
            for q, model in enumerate(ens_models):
                if q == 0:
                    pr_logit, _ = get_pred(x_tensor, model) #予測
                else:
                    pr_logit_tmp, _ = get_pred(x_tensor, model) #予測
                    pr_logit = pr_logit + pr_logit_tmp
            pr_logits[i][:xsize,:ysize,j] = pr_logit
            if xsize != imgsize or ysize != imgsize:
                pr_logits[i][xsize:,ysize:,j] = -1.0
        pr_final_tmp = get_encoding(pr_logits[i], layer, axis = 2, offset = offset)
        offset += len(layer)

        pr_final = update_pr(pr_final, pr_final_tmp[:xsize,:ysize]) 

    return pr_final

def init_models(modelpath: str,
                ) -> list:
    """load all the models.

    Args:
        modelpath (str): path for model files.

    Returns:
        list: list of models.
    """
    groups = [
        [
        ["Smooth muscle","SMA", ["5f60141440414f6dbf2daeb0a1bff900","72cfd4399091498cbb4cd7fb29cf23cd"]],
        ],
        [
        ["Epithelium","AE13", ["21ec5213245f4ca5a11c434e3d2ceb92","b6efdf259f7b457db0dd8acc7f485e60","a8a81248986e457e9d128218781fb8fe"]],
        ],
        [
        ["Leukocyte", "CD45_cellpose", ["7156519f78014a3389933efbd23b7408","ce04777c54b54804957dce8d68788ad6","50be89bc83024a788d79321aa7e095d6"]],
        ["Endothelium", "ERG_cellpose", ["805d0a5d50134fe29ea581ac339776e9","1d4be6c3fc214a2bbc536529d6630c1b"]],
        ["RBC", "GLPA", ["ca378a666ab5440dbc3ec4d602bfa041"]],
        ],
        [
        ["Lymphocytes","CD3_CD20_cellpose", ["57ade74cd3be4461a919c9203c91f5a1","8a5459dc3be5403e934b3ee4afb645ca"]],
        ["Plasma cells","MIST1_cellpose", ["e2b1337cc211431f9595e4092d508658"]],        
        ["Myeloid","MNDA_cellpose", ["60ca96bc32734007afd98d623631218c", "a1f32a1c0cb3418cba07f450965ff244"]],        
        ],
    ]

    print ("loading models...")

    models = []
    for layer in groups:
        models.append([])
        for cell, ab, uuids in layer:
            best_models = []
            for uuid in uuids:
                print(ab, uuid)
                best_models.append(load_model(ab, uuid, modelpath))
            models[-1].append([cell, best_models])

    print("done")
    return models
