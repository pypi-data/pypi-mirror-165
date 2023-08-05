/* Copyright 2015 The TensorFlow Authors. All Rights Reserved.

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

// This module provides routines for encoding a sequence of typed
// entities into a string.  The resulting strings can be
// lexicographically compared to yield the same comparison value that
// would have been generated if the encoded items had been compared
// one by one according to their type.
//
// More precisely, suppose:
//  1. string A is generated by encoding the sequence of items [A_1..A_n]
//  2. string B is generated by encoding the sequence of items [B_1..B_n]
//  3. The types match; i.e., for all i: A_i was encoded using
//     the same routine as B_i
// Then:
//    Comparing A vs. B lexicographically is the same as comparing
//    the vectors [A_1..A_n] and [B_1..B_n] lexicographically.
//
// Furthermore, if n < m, the encoding of [A_1..A_n] is a strict prefix of
// [A_1..A_m] (unless m = n+1 and A_m is the empty string encoded with
// WriteTrailingString, in which case the encodings are equal).
//
// This module is often useful when generating multi-part sstable
// keys that have to be ordered in a particular fashion.

#ifndef TENSORFLOW_LIB_STRINGS_ORDERED_CODE_H__
#define TENSORFLOW_LIB_STRINGS_ORDERED_CODE_H__

#include <string>

#include "tensorflow/core/platform/macros.h"
#include "tensorflow/core/platform/stringpiece.h"
#include "tensorflow/core/platform/types.h"

namespace tensorflow {

namespace strings {

class OrderedCode {
 public:
  // -------------------------------------------------------------------
  // Encoding routines: each one of the following routines append
  // one item to "*dest" in an encoding where larger values are
  // ordered lexicographically after smaller values.
  static void WriteString(string* dest, StringPiece str);
  static void WriteNumIncreasing(string* dest, uint64 num);
  static void WriteSignedNumIncreasing(string* dest, int64_t num);

  // -------------------------------------------------------------------
  // Decoding routines: these extract an item earlier encoded using
  // the corresponding WriteXXX() routines above.  The item is read
  // from "*src"; "*src" is modified to point past the decoded item;
  // and if "result" is non-NULL, "*result" is modified to contain the
  // result.  In case of string result, the decoded string is appended to
  // "*result".  Returns true if the next item was read successfully, false
  // otherwise.
  static bool ReadString(StringPiece* src, string* result);
  static bool ReadNumIncreasing(StringPiece* src, uint64* result);
  static bool ReadSignedNumIncreasing(StringPiece* src, int64_t* result);

  // Helper for testing: corrupt "*str" by changing the kth item separator
  // in the string.
  static void TEST_Corrupt(string* str, int k);

  // Helper for testing.
  // SkipToNextSpecialByte is an internal routine defined in the .cc file
  // with the following semantics. Return a pointer to the first byte
  // in the range "[start..limit)" whose value is 0 or 255.  If no such
  // byte exists in the range, returns "limit".
  static const char* TEST_SkipToNextSpecialByte(const char* start,
                                                const char* limit);

 private:
  // This has only static methods, so disallow construction entirely
  OrderedCode();
  TF_DISALLOW_COPY_AND_ASSIGN(OrderedCode);
};

}  // namespace strings
}  // namespace tensorflow

#endif  // TENSORFLOW_LIB_STRINGS_ORDERED_CODE_H__
