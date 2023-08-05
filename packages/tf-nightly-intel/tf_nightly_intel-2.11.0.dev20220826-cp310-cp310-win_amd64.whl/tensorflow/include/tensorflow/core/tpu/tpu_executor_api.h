/* Copyright 2020 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#ifndef TENSORFLOW_CORE_TPU_TPU_EXECUTOR_API_H_
#define TENSORFLOW_CORE_TPU_TPU_EXECUTOR_API_H_

#include "tensorflow/compiler/xla/stream_executor/tpu/tpu_executor_c_api.h"
#include "tensorflow/core/tpu/libtftpu.h"

namespace tensorflow {
namespace tpu {

TfTpu_ExecutorApiFn* ExecutorApiFn();

// Returns whether function pointers in `executor_api_fn` have been set and
// stream_executor is enabled.
bool IsStreamExecutorEnabled(TfTpu_ExecutorApiFn* executor_api_fn);

// Returns whether function pointers in `executor_api_fn` have been set.  If
// false, it probably means an appropriate initializer needs to be linked in.
bool IsInitialized(TfTpu_ExecutorApiFn* executor_api_fn);

}  // namespace tpu
}  // namespace tensorflow

#endif  // TENSORFLOW_CORE_TPU_TPU_EXECUTOR_API_H_
