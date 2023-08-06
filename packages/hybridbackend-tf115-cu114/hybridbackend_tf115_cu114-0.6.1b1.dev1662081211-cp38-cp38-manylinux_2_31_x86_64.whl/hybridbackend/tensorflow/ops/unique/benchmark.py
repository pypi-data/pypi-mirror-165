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

r'''Unique benchmark.
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
@hb.function()
def build_bench_op(params):
  with tf.device(params.device):
    value_limit = 3 * params.num_columns * params.column_ids
    initializer = tf.random_uniform(
      [params.column_ids], 0, value_limit, dtype=tf.int64)
    inputs = [
      tf.get_variable(f'input{c}', dtype=tf.int64, initializer=initializer)
      for c in xrange(params.num_columns)]
    bench_ops = [
      tf.unique(tf.identity(inputs[c]))[0]
      for c in xrange(params.num_columns)]
  with tf.device('/gpu:0'):
    bench_ops = [tf.math.reduce_sum(o) for o in bench_ops]
    step = tf.train.get_or_create_global_step()
    bench_ops.append(step.assign_add(1))
    bench_op = tf.math.add_n(bench_ops)
  return bench_op


def benchmark(params):
  bench_op = build_bench_op(params)
  hooks = [tf.train.StopAtStepHook(params.num_steps)]
  hooks.append(
    hb.train.StepStatHook(
      count=params.column_ids * params.num_columns / 1000000.,
      unit='Mquery'))
  with hb.train.monitored_session(hooks=hooks) as sess:
    while not sess.should_stop():
      sess.run(bench_op)


if __name__ == '__main__':
  os.environ['CUDA_VISIBLE_DEVICES'] = '0'
  tf.logging.set_verbosity(tf.logging.INFO)
  parser = argparse.ArgumentParser()
  parser.add_argument('--device', type=str, default='/gpu:0')
  parser.add_argument('--column-ids', type=int, default=100000)
  parser.add_argument('--num-columns', type=int, default=100)
  parser.add_argument('--num-steps', type=int, default=10)
  benchmark(parser.parse_args())
