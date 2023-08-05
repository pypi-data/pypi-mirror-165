# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Compatibility functions.

The `tf.compat` module contains two sets of compatibility functions.

## Tensorflow 1.x and 2.x APIs

The `compat.v1` and `compat.v2` submodules provide a complete copy of both the
`v1` and `v2` APIs for backwards and forwards compatibility across TensorFlow
versions 1.x and 2.x. See the
[migration guide](https://www.tensorflow.org/guide/migrate) for details.

## Utilities for writing compatible code

Aside from the `compat.v1` and `compat.v2` submodules, `tf.compat` also contains
a set of helper functions for writing code that works in both:

* TensorFlow 1.x and 2.x
* Python 2 and 3


## Type collections

The compatibility module also provides the following aliases for common
sets of python types:

* `bytes_or_text_types`
* `complex_types`
* `integral_types`
* `real_types`

"""

import sys as _sys

from tensorflow.python.compat.compat import forward_compatibility_horizon
from tensorflow.python.compat.compat import forward_compatible
from tensorflow.python.framework.tensor_shape import dimension_at_index
from tensorflow.python.framework.tensor_shape import dimension_value
from tensorflow.python.util.compat import as_bytes
from tensorflow.python.util.compat import as_str
from tensorflow.python.util.compat import as_str_any
from tensorflow.python.util.compat import as_text
from tensorflow.python.util.compat import bytes_or_text_types
from tensorflow.python.util.compat import complex_types
from tensorflow.python.util.compat import integral_types
from tensorflow.python.util.compat import path_to_str
from tensorflow.python.util.compat import real_types