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

r'''Benchmark for embedding lookup.
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
def build_bench_emb(params):
  with tf.device('/cpu:0'):
    params_data_initializer = tf.random.uniform(
      [params.batch_size, params.dim_size], minval=0.0,
      maxval=1.0, dtype=tf.float32)
    params_data = [
      tf.get_variable(
        f'params_data_{c}',
        use_resource=False,
        dtype=tf.float32,
        initializer=params_data_initializer)
      for c in xrange(params.num_columns)]

  with tf.device('/gpu:0'):
    indices_initializer = tf.random.uniform(
      [params.batch_size, 3], minval=0,
      maxval=params.num_slot, dtype=tf.int64)
    indices = [
      tf.get_variable(
        f'indices_{c}',
        use_resource=False,
        dtype=tf.int64,
        initializer=indices_initializer)
      for c in xrange(params.num_columns)]
    values_initializer = tf.random.uniform(
      [params.batch_size], minval=0,
      maxval=params.column_ids, dtype=tf.int64)
    values = [
      tf.get_variable(
        f'values_{c}',
        use_resource=False,
        dtype=tf.int64,
        initializer=values_initializer)
      for c in xrange(params.num_columns)]
    sp_ids = [
      tf.sparse.SparseTensor(
        indices[c], values[c],
        dense_shape=[params.num_slot, params.num_slot, params.num_slot])
      for c in xrange(params.num_columns)]
    bench_emb_cnt_ops = []
    bench_emb_ops = []
    for c in xrange(params.num_columns):
      if params.dual_seg:
        emb_cnt_ones = tf.expand_dims(
          tf.ones(tf.shape(params_data[c])[0:-1], dtype=tf.int64), -1)
        segment_ids = tf.cast(
          sp_ids[c].indices[:, 0] * sp_ids[c].dense_shape[1]
          + sp_ids[c].indices[:, 1], dtype=tf.int32)
        num_seg = sp_ids[c].dense_shape[0] * sp_ids[c].dense_shape[1]
        sg_idx = tf.argsort(segment_ids)
        segment_ids = tf.sort(segment_ids)
        bench_emb_ops.append(
          tf.reshape(tf.sparse.segment_sum(
            params_data[c], sg_idx, segment_ids,
            num_segments=num_seg), [-1, params.num_slot, params.dim_size]))
        bench_emb_cnt_ops.append(
          tf.reshape(tf.sparse.segment_sum(
            emb_cnt_ones, sg_idx, segment_ids,
            num_segments=num_seg), [-1, params.num_slot]))
      else:
        segment_ids = tf.cast(
          sp_ids[c].indices[:, 0] * sp_ids[c].dense_shape[1]
          + sp_ids[c].indices[:, 1], dtype=tf.int32)
        num_seg = sp_ids[c].dense_shape[0] * sp_ids[c].dense_shape[1]
        sg_idx = tf.argsort(segment_ids)
        segment_ids = tf.sort(segment_ids)
        bench_emb_ops.append(
          tf.reshape(tf.sparse.segment_sum(
            params_data[c], sg_idx, segment_ids,
            num_segments=num_seg), [-1, params.num_slot, params.dim_size]))
        bench_emb_cnt_ops.append(
          tf.reshape(tf.math.count_nonzero(
            tf.sparse.to_dense(
              tf.sparse.reorder(sp_ids[c])),
            axis=-1, dtype=tf.int64), [-1, params.num_slot]))

    bench_emb_cnt_ops = [tf.math.reduce_sum(o) for o in bench_emb_cnt_ops]
    bench_emb_ops = [tf.math.reduce_sum(o) for o in bench_emb_ops]
    loss = tf.math.add_n(bench_emb_ops)
    opt = tf.train.AdamOptimizer(learning_rate=1.)
    step = tf.train.get_or_create_global_step()
    bench_ops = [tf.cast(step.assign_add(1), tf.int64)]
    bench_ops.append(tf.math.add_n(bench_emb_cnt_ops))
    bench_ops.append(opt.minimize(loss, global_step=step))
  return bench_ops


def benchmark(params):
  bench_op = build_bench_emb(params)
  hooks = [tf.train.StopAtStepHook(params.num_steps)]
  hooks.append(
    hb.train.StepStatHook(
      count=params.column_ids
      * params.dim_size
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
  parser.add_argument('--column-ids', type=int, default=5000)
  parser.add_argument('--dim-size', type=int, default=8)
  parser.add_argument('--batch-size', type=int, default=5000)
  parser.add_argument('--num-slot', type=int, default=10)
  parser.add_argument('--num-columns', type=int, default=100)
  parser.add_argument('--dual-seg', default=False, action='store_true')
  parser.add_argument('--num-steps', type=int, default=10000)
  benchmark(parser.parse_args())
