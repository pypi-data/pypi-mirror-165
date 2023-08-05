#ifndef TSL_PLATFORM_STACK_FRAME_H_
#define TSL_PLATFORM_STACK_FRAME_H_

/* Copyright 2020 Google LLC. All Rights Reserved.

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

#include <string>

namespace tsl {

// A struct representing a frame in a stack trace.
struct StackFrame {
  std::string file_name;
  int line_number;
  std::string function_name;

  bool operator==(const StackFrame& other) const {
    return line_number == other.line_number &&
           function_name == other.function_name && file_name == other.file_name;
  }

  bool operator!=(const StackFrame& other) const { return !(*this == other); }
};

}  // namespace tsl

#endif  // TSL_PLATFORM_STACK_TRACE_H_
