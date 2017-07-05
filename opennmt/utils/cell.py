"""RNN cells helpers."""

import tensorflow as tf


def build_cell(num_layers,
               num_units,
               mode,
               dropout_keep_prob=1.0,
               residual_connections=False,
               cell_class=tf.contrib.rnn.LSTMCell):
  """Convenience function to build a multi-layer RNN cell.

  Args:
    num_layers: The number of layers.
    num_units: The number of units in each layer.
    mode: A `tf.estimator.ModeKeys` mode.
    dropout_keep_prob: The probability to keep units in each layer output.
    residual_connections: If `True`, each layer input will be added to its output.
    cell_class: The inner cell class.

  Returns:
    A `tf.contrib.rnn.RNNCell`.
  """
  cells = []

  for i in range(num_layers):
    cell = cell_class(num_units=num_units)
    if residual_connections and i > 0:
      cell = tf.contrib.rnn.ResidualWrapper(cell)
    if mode == tf.estimator.ModeKeys.TRAIN and dropout_keep_prob < 1.0:
      cell = tf.contrib.rnn.DropoutWrapper(cell, output_keep_prob=dropout_keep_prob)
    cells.append(cell)

  if len(cells) == 1:
    return cells[0]
  else:
    return tf.contrib.rnn.MultiRNNCell(cells)
