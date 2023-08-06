"""
 Author: yican.yc
 Date: 2022-08-23 19:24:12
 Last Modified by:   yican.yc
 Last Modified time: 2022-08-23 19:24:12
"""
import numpy as np
import albumentations as A

# randaugment
# vit-torchvision doc : https://github.com/kentaroy47/vision-transformers-cifar10/blob/main/randomaug.py
# google-public : https://github.com/google-research/uda/blob/master/image/randaugment/policies.py#L57
# migrating_from_torchvision_to_albumentations : https://albumentations.ai/docs/examples/migrating_from_torchvision_to_albumentations/
# albumentations implement : https://towardsdatascience.com/augmentation-methods-using-albumentations-and-pytorch-35cd135382f8
# 知乎blog : https://zhuanlan.zhihu.com/p/293065153
# paper : https://arxiv.org/abs/1805.09501


def randAugment(N, M, p, mode="all", cut_out=False):
    # Magnitude(M) search space
    shift_x = np.linspace(0, 150, 10)
    shift_y = np.linspace(0, 150, 10)
    rot = np.linspace(0, 30, 10)
    shear = np.linspace(0, 10, 10)
    sola = np.linspace(0, 256, 10)
    post = [4, 4, 5, 5, 6, 6, 7, 7, 8, 8]
    cont = [np.linspace(-0.8, -0.1, 10), np.linspace(0.1, 2, 10)]
    bright = np.linspace(0.1, 0.7, 10)
    shar = np.linspace(0.1, 0.9, 10)
    cut = np.linspace(0, 60, 10)
    # Transformation search space
    Aug = [  # 0 - geometrical
        A.ShiftScaleRotate(shift_limit_x=shift_x[M], rotate_limit=0, shift_limit_y=0, shift_limit=shift_x[M], p=p),
        A.ShiftScaleRotate(shift_limit_y=shift_y[M], rotate_limit=0, shift_limit_x=0, shift_limit=shift_y[M], p=p),
        A.IAAAffine(rotate=rot[M], p=p),
        A.IAAAffine(shear=shear[M], p=p),
        A.InvertImg(p=p),
        # 5 - Color Based
        A.Equalize(p=p),
        A.Solarize(threshold=sola[M], p=p),
        A.Posterize(num_bits=post[M], p=p),
        A.RandomContrast(limit=[cont[0][M], cont[1][M]], p=p),
        A.RandomBrightness(limit=bright[M], p=p),
        A.IAASharpen(alpha=shar[M], lightness=shar[M], p=p),
    ]
    # Sampling from the Transformation search space
    if mode == "geo":
        ops = np.random.choice(Aug[0:5], N)
    elif mode == "color":
        ops = np.random.choice(Aug[5:], N)
    else:
        ops = np.random.choice(Aug, N)

    if cut_out:
        ops.append(A.Cutout(num_holes=8, max_h_size=int(cut[M]), max_w_size=int(cut[M]), p=p))
    transforms = A.Compose(ops)
    return transforms, ops
