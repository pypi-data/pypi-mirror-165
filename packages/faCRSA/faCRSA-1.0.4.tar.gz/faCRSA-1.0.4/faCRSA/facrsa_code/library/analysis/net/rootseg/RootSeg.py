#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Author: Ruinan Zhang
Version: v1.2
LastEditTime: 2022-07-06 16:14:06
E-mail: 2020801253@stu.njau.edu.cn
Copyright (c) 2022 by Ruinan Zhang, All Rights Reserved. Licensed under the GPL v3.0.
'''
import tensorflow as tf
import tensorflow.keras.backend as K
from tensorflow.keras.layers import *
from tensorflow.keras.models import *
from .attention import cbam_module


tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


def relu6(x):
    return K.relu(x, max_value=6)


def _conv_block(inputs, filters, alpha, kernel=(3, 3), strides=(1, 1)):
    filters = int(filters * alpha)
    x = ZeroPadding2D(padding=(1, 1), name='conv1_pad')(inputs)
    x = Conv2D(filters, kernel, padding='valid',
               use_bias=False,
               strides=strides,
               name='conv1')(x)
    x = BatchNormalization(name='conv1_bn')(x)
    return Activation(relu6, name='conv1_relu')(x)


def _depthwise_conv_block(inputs, pointwise_conv_filters, alpha, depth_multiplier=1, strides=(1, 1), block_id=1):
    pointwise_conv_filters = int(pointwise_conv_filters * alpha)

    x = ZeroPadding2D((1, 1), name='conv_pad_%d' % block_id)(inputs)
    x = DepthwiseConv2D((3, 3), padding='valid',
                        depth_multiplier=depth_multiplier,
                        strides=strides,
                        use_bias=False,
                        name='conv_dw_%d' % block_id)(x)
    x = BatchNormalization(name='conv_dw_%d_bn' % block_id)(x)
    x = Activation(relu6, name='conv_dw_%d_relu' % block_id)(x)

    x = Conv2D(pointwise_conv_filters, (1, 1),
               padding='same',
               use_bias=False,
               strides=(1, 1),
               name='conv_pw_%d' % block_id)(x)
    x = BatchNormalization(name='conv_pw_%d_bn' % block_id)(x)
    return Activation(relu6, name='conv_pw_%d_relu' % block_id)(x)


def RootSeg(n_classes=2, input_height=512, input_width=512):
    alpha = 1.0
    depth_multiplier = 1

    img_input = Input(shape=(input_height, input_width, 3))

    x = _conv_block(img_input, 32, alpha, strides=(2, 2))
    x = _depthwise_conv_block(x, 64, alpha, depth_multiplier, block_id=1)
    f1 = x

    x = _depthwise_conv_block(x, 128, alpha, depth_multiplier, strides=(2, 2), block_id=2)
    x = _depthwise_conv_block(x, 128, alpha, depth_multiplier, block_id=3)
    f2 = x

    x = _depthwise_conv_block(x, 256, alpha, depth_multiplier, strides=(2, 2), block_id=4)
    x = _depthwise_conv_block(x, 256, alpha, depth_multiplier, block_id=5)
    x = cbam_module(x)
    f3 = x

    x = _depthwise_conv_block(x, 512, alpha, depth_multiplier, strides=(2, 2), block_id=6)
    x = _depthwise_conv_block(x, 512, alpha, depth_multiplier, block_id=7)
    x = _depthwise_conv_block(x, 512, alpha, depth_multiplier, block_id=8)
    x = _depthwise_conv_block(x, 512, alpha, depth_multiplier, block_id=9)
    x = _depthwise_conv_block(x, 512, alpha, depth_multiplier, block_id=10)
    x = _depthwise_conv_block(x, 512, alpha, depth_multiplier, block_id=11)
    f4 = x

    x = _depthwise_conv_block(x, 1024, alpha, depth_multiplier, strides=(2, 2), block_id=12)
    x = _depthwise_conv_block(x, 1024, alpha, depth_multiplier, block_id=13)
    f5 = x

    o = f5
    o = ZeroPadding2D((1, 1))(o)
    o = DepthwiseConv2D((3, 3), padding='valid')(o)
    o = Conv2D(512, (1, 1), padding='valid')(o)
    o = BatchNormalization()(o)

    o = UpSampling2D((2, 2))(o)
    o = concatenate([o, f4])
    o = ZeroPadding2D((1, 1))(o)
    o = DepthwiseConv2D((3, 3), padding='valid')(o)
    o = Conv2D(256, (1, 1), padding='valid')(o)
    o = BatchNormalization()(o)

    o = UpSampling2D((2, 2))(o)
    o = concatenate([o, f3])
    o = ZeroPadding2D((1, 1))(o)
    o = DepthwiseConv2D((3, 3), padding='valid')(o)
    o = Conv2D(256, (1, 1), padding='valid')(o)
    o = BatchNormalization()(o)

    o = UpSampling2D((2, 2))(o)
    o = concatenate([o, f2])
    o = ZeroPadding2D((1, 1))(o)
    o = DepthwiseConv2D((3, 3), padding='valid')(o)
    o = Conv2D(128, (1, 1), padding='valid')(o)
    o = BatchNormalization()(o)
    o = cbam_module(o)

    o = UpSampling2D((2, 2))(o)
    o = concatenate([o, f1])
    o = ZeroPadding2D((1, 1))(o)
    o = DepthwiseConv2D((3, 3), padding='valid')(o)
    o = Conv2D(64, (1, 1), padding='valid')(o)
    o = BatchNormalization()(o)
    o = UpSampling2D((2, 2))(o)

    o = Conv2D(n_classes, (3, 3), padding='same')(o)

    o = Reshape((int(input_height) * int(input_width), -1))(o)
    o = Softmax()(o)
    model = Model(img_input, o)

    return model
