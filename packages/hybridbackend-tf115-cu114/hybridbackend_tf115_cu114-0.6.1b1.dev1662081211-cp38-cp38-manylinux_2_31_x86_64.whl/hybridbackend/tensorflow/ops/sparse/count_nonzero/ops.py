# Copyright 2021 Alibaba Group Holding Limited. All Rights Reserved.
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
# =============================================================================

r'''Count nonzeros along specified axis.
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow.python.framework import dtypes
from tensorflow.python.framework import ops

from hybridbackend.tensorflow.common import oplib as _ops


def sparse_count_nonzero(input_tensor,
                         axis=-1,
                         dtype=dtypes.int64,
                         name=None):
  r'''Count nonzeros along specified axis.

  Args:
    input_tensor: A SparseTensor to reduce. Should be of numeric type, `bool`,
      or `string`
    axis: The dimensions to reduce (count nonzeros)
    dtype: The output dtype; defaults to `tf.int64`.
    name: A name for the operation (optional).

  Returns:
    The reduced tensor (number of nonzero values).
  '''
  with ops.name_scope(name, 'sparse_count_nonzero'):
    indices = input_tensor.indices
    values = input_tensor.values
    shape = input_tensor.dense_shape
    return _ops.hb_sparse_count_nonzero(
      indices, values, shape, axis=axis, Tout=dtype)


def sparse_count_nonzero_n(input_tensors,
                           axis=-1,
                           dtype=dtypes.int64,
                           name=None):
  r'''Count nonzeros along specified axis.

  Args:
    input_tensors: A list of SparseTensor to reduce.
      Should be of numeric type, `bool`, or `string`
    axis: The dimensions to reduce (count nonzeros)
    dtype: The output dtype; defaults to `tf.int64`.
    name: A name for the operation (optional).

  Returns:
    The reduced tensors (number of nonzero values).
  '''
  with ops.name_scope(name, 'sparse_count_nonzero'):
    indices = [t.indices for t in input_tensors]
    values = [t.values for t in input_tensors]
    shape = [t.dense_shape for t in input_tensors]
    return _ops.hb_sparse_count_nonzero_n(
      indices, values, shape, axis=axis, Tout=dtype)
