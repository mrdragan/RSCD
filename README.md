# RSCD (BS-RSCD & JCD)

**[CVPR2021]** [Towards Rolling Shutter Correction and Deblurring in Dynamic Scenes](https://arxiv.org/abs/2104.01601) ([CVF Link](https://openaccess.thecvf.com/content/CVPR2021/papers/Zhong_Towards_Rolling_Shutter_Correction_and_Deblurring_in_Dynamic_Scenes_CVPR_2021_paper.pdf))

by [Zhihang Zhong](https://zzh-tech.github.io/), Yinqiang Zheng, Imari Sato

We contributed the first real-world dataset ([BS-RSCD](https://drive.google.com/file/d/1hgzibaez7EipmPSN-3GzQO0_mlyruKGa/view?usp=sharing)) and end-to-end model (JCD) for joint rolling shutter correction and deblurring tasks.

We collected the data samples using the proposed beam-splitter acquisition system as below:

![image](https://drive.google.com/uc?export=view&id=1JkAsNkiaWZ5eZ8KSQdMENrxTBPEfrFen)

In the near future, we will add more data samples with larger distortion to the dataset ...

If you are interested in real-world datasets for pure deblurring tasks, please refer to [ESTRNN & BSD](https://github.com/zzh-tech/ESTRNN).


## Prerequisites (Updated for Toyon)
The repository is now setup to be run in a devcontainer. A `Dockerfile` an `environment.yaml` are included in the `docker` directory that can be used to define the environment. The process to setup the environment is given here:

1. Update the `Dockerfile` to include the appropriate cuda compute capability number based on your GPU. Line 59 in the snippet below is where you need up update the compute capability (next to `+PTX`). The instructions on where to find the compute capability number are given in the comments on lines 54 to 57 of the snippet below.

```bash
  54 # This is kind of annoying, but you need to put your gpu compute capability (the number by +PTX)
  55 # This information can be found here: https://developer.nvidia.com/cuda-gpus
  56 # Find your gpu and find the compute capability then copy the number next to the +PTX
  57 # NOTE: this can also be found by running this command: nvidia-smi --query-gpu=compute_cap --format=csv
  58 ENV FORCE_CUDA="1"
  59 ARG TORCH_CUDA_ARCH_LIST="7.5+PTX"
  60 ENV TORCH_CUDA_ARCH_LIST="${TORCH_CUDA_ARCH_LIST}"
  61 ADD ./docker/packages_from_deepunrollnet packages_from_deepunrollnet
  62 RUN pip install packages_from_deepunrollnet/package_core/
  63 RUN pip install packages_from_deepunrollnet/package_correlation/
  64 RUN pip install packages_from_deepunrollnet/package_forward_warp/
  65 RUN python -m pip install "git+https://github.com/facebookresearch/detectron2.git"
```

2. Update the `devcontainer.json` located at `.devcontainer/devcontainer.json` to include your local volume mounts. 

```bash
 10   "mounts": [
 11         "source=/path/to/data,target=/data,type=bind,consistency=cached"],
```

3. Open VisualStudioCode and select the green icon in the bottom left corner. If you have the correct dependencies installed then an option should pop up that says `Open folder in container`. Select that option then navigate to the root of the `RSCD-main` repository. If you do not have the proper dependencies installed then follow this tutorial: https://code.visualstudio.com/docs/devcontainers/tutorial


## Setup instructions from the original repository. These instructions did not work for me
Install the dependent packages:

```bash
conda create -n rscd python=3.8
conda activate rscd
sh install.sh
```

Download lmdb files of [BS-RSCD](https://drive.google.com/file/d/1j4gxN28KmDA7Yl1W37i87n3nFIgmZh2_/view?usp=sharing)
(or [Fastec-RS](https://drive.google.com/file/d/1JGzY_8tVVP-oy7jFL1TL84gt3yz1bry3/view?usp=sharing) for RSC tasks).

(PS, for how to create lmdb file, you can refer to ./data/create_rscd_lmdb.ipynb)
## Training

Please specify the *\<path\>* (e.g. "./dataset/ ") where you put the dataset file or change the default value in "
./para/paramter.py".

Train JCD on BS-RSCD:

```bash
python main.py --data_root <path> --model JCD --dataset rscd_lmdb --video
```

Train JCD on Fastec-RS:

```bash
python main.py --data_root <path> --model JCD --dataset fastec_rs_lmdb --video
```

## Testing

Please download [checkpoints](https://drive.google.com/file/d/1bGFHNjoqTGk78UTF-7qDm6hVU4Oqe7N3/view?usp=sharing) and
unzip it under the main directory.

Run the pre-trained model on BS-RSCD:

```bash
python main.py --test_only --dataset rscd_lmdb --test_checkpoint ./checkpoints/JCD_BS-RSCD.tar --video
```

Inference for video file:
```bash
python video_inference.py --src <input_path> --dst <output_path> --checkpoint ./checkpoints/JCD_BS-RSCD.tar
```

## Citing

If BS-RSCD and JCD are useful for your research, please consider citing:

```bibtex
@InProceedings{Zhong_2021_Towards,
  title={Towards Rolling Shutter Correction and Deblurring in Dynamic Scenes},
  author={Zhong, Zhihang and Zheng, Yinqiang and Sato, Imari},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  month = {June},
  year={2021}
}
```
