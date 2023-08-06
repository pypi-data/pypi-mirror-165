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

r'''Benchmark for segment_sum.
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
def build_bench_sparse_op(params):
  with tf.device(params.device):
    params_data_initializer = tf.random.uniform(
      [params.unique_ids, params.dim_size], minval=0.0,
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
      [params.column_ids], minval=0,
      maxval=params.unique_ids, dtype=tf.int32)
    indices = [
      tf.get_variable(
        f'indices_{c}',
        use_resource=False,
        dtype=tf.int32,
        initializer=indices_initializer)
      for c in xrange(params.num_columns)]
    segment_ids_initializer = tf.random.uniform(
      [params.column_ids], minval=0, maxval=params.num_segments, dtype=tf.int32)
    segment_ids = [
      tf.get_variable(
        f'segment_ids_{c}',
        use_resource=False,
        dtype=tf.int32,
        initializer=segment_ids_initializer)
      for c in xrange(params.num_columns)]
    bench_ops = [
      tf.sparse.segment_sum(
        params_data[c], indices[c], segment_ids[c])
      for c in xrange(params.num_columns)]
    bench_ops = [tf.math.reduce_sum(o) for o in bench_ops]
    step = tf.train.get_or_create_global_step()
    bench_ops.append(tf.cast(step.assign_add(1), tf.float32))
    bench_op = tf.math.add_n(bench_ops)
  return bench_op


def build_fused_bench_sparse_op(params):
  with tf.device(params.device):
    params_data_initializer = tf.random.uniform(
      [params.unique_ids, params.dim_size], minval=0.0,
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
      [params.column_ids], minval=0,
      maxval=params.unique_ids, dtype=tf.int32)
    indices = [
      tf.get_variable(
        f'indices_{c}',
        use_resource=False,
        dtype=tf.int32,
        initializer=indices_initializer)
      for c in xrange(params.num_columns)]
    segment_ids_initializer = tf.random.uniform(
      [params.column_ids], minval=0, maxval=params.num_segments, dtype=tf.int32)
    segment_ids = [
      tf.get_variable(
        f'segment_ids_{c}',
        use_resource=False,
        dtype=tf.int32,
        initializer=segment_ids_initializer)
      for c in xrange(params.num_columns)]
    bench_ops = [
      tf.sparse.segment_sum(params_data[i], indices[i], segment_ids[i])
      for i in xrange(params.num_columns)]
    bench_ops = [tf.math.reduce_sum(o) for o in bench_ops]
    step = tf.train.get_or_create_global_step()
    bench_ops.append(tf.cast(step.assign_add(1), tf.float32))
    bench_op = tf.math.add_n(bench_ops)
  return bench_op


def build_fused_bench_unsorted_op(params):
  with tf.device(params.device):
    params_data_initializer = tf.random.uniform(
      [params.unique_ids, params.dim_size], minval=0.0,
      maxval=1.0, dtype=tf.float32)
    params_data = [
      tf.get_variable(
        f'params_data_{c}',
        use_resource=False,
        dtype=tf.float32,
        initializer=params_data_initializer)
      for c in xrange(params.num_columns)]

  with tf.device('/gpu:0'):
    segment_ids_initializer = tf.random.uniform(
      [params.unique_ids], minval=0, maxval=params.num_segments, dtype=tf.int32)
    segment_ids = [
      tf.get_variable(
        f'segment_ids_{c}',
        use_resource=False,
        dtype=tf.int32,
        initializer=segment_ids_initializer)
      for c in xrange(params.num_columns)]

    num_segments_initializer = tf.constant(params.num_segments, dtype=tf.int32)
    num_segments = [
      tf.get_variable(
        f'num_segments_{c}',
        use_resource=False,
        dtype=tf.int32,
        initializer=num_segments_initializer)
      for c in xrange(params.num_columns)]
    bench_ops = [
      tf.math.unsorted_segment_sum(
        params_data[i], segment_ids[i], num_segments[i])
      for i in xrange(params.num_columns)]
    bench_ops = [tf.math.reduce_sum(o) for o in bench_ops]
    step = tf.train.get_or_create_global_step()
    bench_ops.append(tf.cast(step.assign_add(1), tf.float32))
    bench_op = tf.math.add_n(bench_ops)
  return bench_op


def benchmark(params):
  if params.grouping:
    if params.unsorted:
      bench_op = build_fused_bench_unsorted_op(params)
    else:
      bench_op = build_fused_bench_sparse_op(params)
  else:
    bench_op = build_bench_sparse_op(params)
  hooks = [tf.train.StopAtStepHook(params.num_steps)]
  hooks.append(
    hb.train.StepStatHook(
      count=params.column_ids * params.num_columns / 1000000., unit='Mlookups'))
  with hb.train.monitored_session(hooks=hooks) as sess:
    while not sess.should_stop():
      sess.run(bench_op)


if __name__ == '__main__':
  os.environ['CUDA_VISIBLE_DEVICES'] = '0'
  tf.get_logger().propagate = False
  tf.logging.set_verbosity(tf.logging.INFO)
  parser = argparse.ArgumentParser()
  parser.add_argument('--device', type=str, default='/gpu:0')
  parser.add_argument('--column-ids', type=int, default=100000)
  parser.add_argument('--unique-ids', type=int, default=1000)
  parser.add_argument('--dim-size', type=int, default=32)
  parser.add_argument('--num-segments', type=int, default=100)
  parser.add_argument('--num-columns', type=int, default=1)
  parser.add_argument('--grouping', default=False, action='store_true')
  parser.add_argument('--unsorted', default=False, action='store_true')
  parser.add_argument('--num-steps', type=int, default=10)
  benchmark(parser.parse_args())
