# coding: utf-8
import os
import numpy as np
from PIL import Image
import tensorflow as tf
from PIL import ImageFilter


def load_images_new(input_dir, csv_file, index, batch_shape):
    images = np.zeros(batch_shape)
    # sharpen_images = np.zeros(batch_shape)
    filenames = []
    truelabel = []
    targetlabel = []
    idx = 0
    for i in range(index, min(index + batch_shape[0], 10000)):
        img_obj = csv_file.loc[i]
        name = str(img_obj['name']).split('_')[-1]
        file = str(img_obj['name']).split('_')[0]
        ImageID = name + '.png'
        # TargetClass = img_obj['TargetClass']
        img_path = os.path.join(os.path.join(input_dir, file), ImageID)

        images[idx, ...] = np.array(Image.open(img_path)).astype(np.float) / 255.0
        # sharpen_images[idx, ...] = np.array(Image.open(img_path).filter(ImageFilter.BLUR)).astype(np.float) / 255.0
        # Image.open(img_path).filter(ImageFilter.BLUR).show()
        # exit()
        filenames.append(ImageID)
        truelabel.append(img_obj['label'] + 1)
        # targetlabel.append(img_obj['TargetClass'])
        idx += 1
    images = images * 2.0 - 1.0
    # sharpen_images = sharpen_images * 2.0 - 1.0
    return images, filenames, truelabel, targetlabel


def load_images(input_dir, csv_file, index, batch_shape):
    images = np.zeros(batch_shape)
    # sharpen_images = np.zeros(batch_shape)
    filenames = []
    truelabel = []
    targetlabel = []
    idx = 0
    for i in range(index, min(index + batch_shape[0], 1000)):
        img_obj = csv_file.loc[i]
        ImageID = img_obj['ImageId'] + '.png'
        # TargetClass = img_obj['TargetClass']
        img_path = os.path.join(input_dir, ImageID)
        images[idx, ...] = np.array(Image.open(img_path)).astype(np.float) / 255.0
        # sharpen_images[idx, ...] = np.array(Image.open(img_path).filter(ImageFilter.BLUR)).astype(np.float) / 255.0
        # Image.open(img_path).filter(ImageFilter.BLUR).show()
        # exit()
        filenames.append(ImageID)
        truelabel.append(img_obj['TrueLabel'])
        targetlabel.append(img_obj['TargetClass'])
        idx += 1
    images = images * 2.0 - 1.0
    # sharpen_images = sharpen_images * 2.0 - 1.0
    return images, filenames, truelabel, targetlabel


def save_images(images, filenames, output_dir):
    """Saves images to the output directory.

    Args:
        images: array with minibatch of images
        filenames: list of filenames without path
            If number of file names in this list less than number of images in
            the minibatch then only first len(filenames) images will be saved.
        output_dir: directory where to save images
    """
    for i, filename in enumerate(filenames):
        # Images for inception classifier are normalized to be in [-1, 1] interval,
        # so rescale them back to [0, 1].
        with tf.gfile.Open(os.path.join(output_dir, filename), 'w') as f:
            image = (images[i, :, :, :] + 1.0) * 0.5
            img = Image.fromarray((image * 255).astype('uint8')).convert('RGB')
            img.save(output_dir + filename)

def save_images_new(images, filenames, output_dir):
    """Saves images to the output directory.

    Args:
        images: array with minibatch of images
        filenames: list of filenames without path
            If number of file names in this list less than number of images in
            the minibatch then only first len(filenames) images will be saved.
        output_dir: directory where to save images
    """
    for i, filename in enumerate(filenames):
        # Images for inception classifier are normalized to be in [-1, 1] interval,
        # so rescale them back to [0, 1].
        with tf.gfile.Open(os.path.join(output_dir, filename), 'w') as f:
            image = images[i, :, :, :]
            img = Image.fromarray((image * 255).astype('uint8')).convert('RGB')
            img.save(output_dir + filename)


def load_labels(file_name):
    # map image id to true label as f2l and map image id to target class as f2t
    import pandas as pd
    dev = pd.read_csv(file_name)
    label_map = {dev.iloc[i]['ImageId']: dev.iloc[i]['TrueLabel'] for i in range(len(dev))}
    return label_map