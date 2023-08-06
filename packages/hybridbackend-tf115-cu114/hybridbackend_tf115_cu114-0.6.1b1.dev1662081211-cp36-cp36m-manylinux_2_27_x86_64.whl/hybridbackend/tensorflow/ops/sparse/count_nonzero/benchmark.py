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

r'''Benchmark for sparse_count_nonzero.
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os
from six.moves import xrange  # pylint: disable=redefined-builtin

import tensorflow as tf

import hybridbackend.tensorflow as hb


# pylint: disable=missing-docstring
def build_bench_sparse_count_nonzero(params):

  vals_initializer = tf.random.uniform(
    [params.dense_shape_dim, params.dense_shape_dim], minval=0,
    maxval=params.sparsity, dtype=tf.int64)
  vals_initializer = tf.cast(
    tf.math.equal(vals_initializer, 0), dtype=tf.int64)
  vals = [
    tf.get_variable(
      f'params_val_{c}',
      use_resource=False,
      dtype=tf.int64,
      initializer=vals_initializer)
    for c in xrange(params.num_columns)]

  sp_tensors = [
    tf.sparse.from_dense(
      vals[c])
    for c in xrange(params.num_columns)]
  if params.reorder:
    with tf.device('/gpu:0'):
      bench_ops = [
        tf.math.count_nonzero(
          tf.sparse.to_dense(
            tf.sparse.reorder(sp_tensors[c])), axis=-1, dtype=tf.int64)
        for c in xrange(params.num_columns)
      ]
  else:
    with tf.device('/gpu:0'):
      bench_ops = [
        tf.math.count_nonzero(
          tf.sparse.to_dense(
            sp_tensors[c]), axis=-1, dtype=tf.int64)
        for c in xrange(params.num_columns)
      ]
  bench_ops = [tf.math.reduce_sum(o) for o in bench_ops]
  step = tf.train.get_or_create_global_step()
  bench_ops.append(tf.cast(step.assign_add(1), tf.int64))
  bench_op = tf.math.add_n(bench_ops)
  return bench_op


def benchmark(params):
  bench_op = build_bench_sparse_count_nonzero(params)
  hooks = [tf.train.StopAtStepHook(params.num_steps)]
  hooks.append(
    hb.train.StepStatHook(
      count=params.dense_shape_dim
      * params.dense_shape_dim
      * params.num_columns / 1000000.,
      unit='Mlookups'))
  with hb.train.monitored_session(hooks=hooks) as sess:
    while not sess.should_stop():
      sess.run(bench_op)


if __name__ == '__main__':
  os.environ['CUDA_VISIBLE_DEVICES'] = '0'
  tf.get_logger().propagate = False
  tf.logging.set_verbosity(tf.logging.INFO)
  parser = argparse.ArgumentParser()
  parser.add_argument('--num-columns', type=int, default=10)
  parser.add_argument('--num-steps', type=int, default=1000)
  parser.add_argument('--sparsity', type=int, default=10)
  parser.add_argument('--dense-shape-dim', type=int, default=1000)
  parser.add_argument('--reorder', default=False, action='store_true')
  benchmark(parser.parse_args())
