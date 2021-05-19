# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""Contains the factory method to create decoders."""

from typing import Mapping, Optional

# Import libraries

import tensorflow as tf

from official.modeling import hyperparams
from official.vision.beta.modeling import decoders


def build_decoder(
    input_specs: Mapping[str, tf.TensorShape],
    model_config: hyperparams.Config,
    l2_regularizer: Optional[tf.keras.regularizers.Regularizer] = None
) -> tf.keras.Model:
  """Builds decoder from a config.

  Args:
    input_specs: A `dict` of input specifications. A dictionary consists of
      {level: TensorShape} from a backbone.
    model_config: A OneOfConfig. Model config.
    l2_regularizer: A `tf.keras.regularizers.Regularizer` instance. Default to
      None.

  Returns:
    A `tf.keras.Model` instance of the decoder.
  """
  decoder_type = model_config.decoder.type
  decoder_cfg = model_config.decoder.get()
  norm_activation_config = model_config.norm_activation

  if decoder_type == 'identity':
    decoder = None
  elif decoder_type == 'fpn':
    decoder = decoders.FPN(
        input_specs=input_specs,
        min_level=model_config.min_level,
        max_level=model_config.max_level,
        num_filters=decoder_cfg.num_filters,
        use_separable_conv=decoder_cfg.use_separable_conv,
        activation=norm_activation_config.activation,
        use_sync_bn=norm_activation_config.use_sync_bn,
        norm_momentum=norm_activation_config.norm_momentum,
        norm_epsilon=norm_activation_config.norm_epsilon,
        kernel_regularizer=l2_regularizer)
  elif decoder_type == 'nasfpn':
    decoder = decoders.NASFPN(
        input_specs=input_specs,
        min_level=model_config.min_level,
        max_level=model_config.max_level,
        num_filters=decoder_cfg.num_filters,
        num_repeats=decoder_cfg.num_repeats,
        use_separable_conv=decoder_cfg.use_separable_conv,
        activation=norm_activation_config.activation,
        use_sync_bn=norm_activation_config.use_sync_bn,
        norm_momentum=norm_activation_config.norm_momentum,
        norm_epsilon=norm_activation_config.norm_epsilon,
        kernel_regularizer=l2_regularizer)
  elif decoder_type == 'aspp':
    decoder = decoders.ASPP(
        level=decoder_cfg.level,
        dilation_rates=decoder_cfg.dilation_rates,
        num_filters=decoder_cfg.num_filters,
        pool_kernel_size=decoder_cfg.pool_kernel_size,
        dropout_rate=decoder_cfg.dropout_rate,
        use_sync_bn=norm_activation_config.use_sync_bn,
        norm_momentum=norm_activation_config.norm_momentum,
        norm_epsilon=norm_activation_config.norm_epsilon,
        activation=norm_activation_config.activation,
        kernel_regularizer=l2_regularizer)
  elif decoder_type == 'mrfm':
    decoder = decoders.MRFM(
        input_specs=input_specs,
        feature_map_layout={
            decoders.mrfm.FROM_LAYER: decoder_cfg.fml_from_layer,
            decoders.mrfm.LAYER_DEPTH: decoder_cfg.fml_layer_depth
        },
        depth_multiplier=decoder_cfg.depth_multiplier,
        min_depth=decoder_cfg.min_depth,
        insert_1x1_conv=decoder_cfg.insert_1x1_conv,
        kernel_size=decoder_cfg.kernel_size,
        use_explicit_padding=decoder_cfg.use_explicit_padding,
        use_depthwise=decoder_cfg.use_depthwise,
        activation=norm_activation_config.activation,
        use_sync_bn=norm_activation_config.use_sync_bn,
        norm_momentum=norm_activation_config.norm_momentum,
        norm_epsilon=norm_activation_config.norm_epsilon,
        kernel_regularizer=l2_regularizer
    )
  else:
    raise ValueError('Decoder {!r} not implement'.format(decoder_type))

  return decoder
