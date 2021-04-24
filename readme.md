# Staircase Sign Method for Boosting Adversarial Attacks 
This is the **Tensorflow code**  for our paper "[Staircase Sign Method for Boosting Adversarial Attacks](http://arxiv.org/abs/2104.09722)" (is under review now). Pytorch version can be found [here](https://github.com/qilong-zhang/CVPR2021-Competition-Unrestricted-Adversarial-Attacks-on-ImageNet).

In our paper, we rethink the limitation of **Sign method (SM)**, e.g., I-FGSM, and propose a novel **Staircase Sign Method (SSM)** to alleviate this issue, thus boosting  both **targeted** and **non-targeted** transfer-based attacks. Comparing with state-of-the-art targeted attacks, we significantly improve
the transferability (i.e. on average, **5.1%** for normally trained models and **11.2%** for adversarially trained defenses). 

✏ *We hope that our proposed method can completely replace the existing SM, not only in terms of transfer-based attacks (e.g. query-based attack). We encourage you to test our SSM and demonstrate the effectiveness of  this algorithm. If you have any questions, please feel free to contact me.*



## Implementation
- Requirement

  - Python 3.7
  - Tensorflow 1.14.0
  - pandas 1.1.3
  - matplotlib 3.3.4
  - tqdm 4.43.0

- Download the models

  - [Normlly trained models](https://github.com/tensorflow/models/tree/master/research/slim#Pretrained)
  - [Ensemble  adversarial trained models](https://github.com/tensorflow/models/tree/master/research/adv_imagenet_models?spm=5176.12282029.0.0.3a9e79b7cynrQf)
  
- Then put these models into `"models/"`

- Run the code

  ```python
  python attack_iter_SSM_NT.py   # if the victim's model is in normally trained models
  ```

  ```python
  python attack_iter_SSM_EAT.py   # if the victim's model is in ensemble adversarially trained models
  ```

- The output images are in `"output/"`

## Visualization
<p align="center">
<img src="https://github.com/qilong-zhang/Staircase-sign-method/blob/main/readme_img/illustration.png"/>
</p>

## Experimental Results
<p align="center">
<img src="https://github.com/qilong-zhang/Staircase-sign-method/blob/main/readme_img/result.png"/>
</p>

## Citing this work

If you find this work is useful in your research, please consider citing:

```
@inproceedings{Zhang2021SSM,
    title={Staircase Sign Method for Boosting Adversarial Attacks},
    author={Gao, Lianli and Zhang, Qilong and Zhu, Xiaosu and Song, Jingkuan and Shen, Hengtao},
    journal   = {CoRR},
    volume    = {abs/2104.09722},
    year      = {2021}
}
```
