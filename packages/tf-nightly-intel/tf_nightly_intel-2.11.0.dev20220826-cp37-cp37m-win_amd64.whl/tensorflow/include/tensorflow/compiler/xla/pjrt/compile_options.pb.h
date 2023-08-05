// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/compiler/xla/pjrt/compile_options.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcompiler_2fxla_2fpjrt_2fcompile_5foptions_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcompiler_2fxla_2fpjrt_2fcompile_5foptions_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3009000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3009002 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_table_driven.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/inlined_string_field.h>
#include <google/protobuf/metadata.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/unknown_field_set.h>
#include "tensorflow/compiler/xla/xla.pb.h"
#include "tensorflow/compiler/xla/xla_data.pb.h"
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_tensorflow_2fcompiler_2fxla_2fpjrt_2fcompile_5foptions_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_tensorflow_2fcompiler_2fxla_2fpjrt_2fcompile_5foptions_2eproto {
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTableField entries[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::AuxillaryParseTableField aux[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTable schema[2]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::FieldMetadata field_metadata[];
  static const ::PROTOBUF_NAMESPACE_ID::internal::SerializationTable serialization_table[];
  static const ::PROTOBUF_NAMESPACE_ID::uint32 offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_tensorflow_2fcompiler_2fxla_2fpjrt_2fcompile_5foptions_2eproto;
namespace xla {
class CompileOptionsProto;
class CompileOptionsProtoDefaultTypeInternal;
extern CompileOptionsProtoDefaultTypeInternal _CompileOptionsProto_default_instance_;
class ExecutableBuildOptionsProto;
class ExecutableBuildOptionsProtoDefaultTypeInternal;
extern ExecutableBuildOptionsProtoDefaultTypeInternal _ExecutableBuildOptionsProto_default_instance_;
}  // namespace xla
PROTOBUF_NAMESPACE_OPEN
template<> ::xla::CompileOptionsProto* Arena::CreateMaybeMessage<::xla::CompileOptionsProto>(Arena*);
template<> ::xla::ExecutableBuildOptionsProto* Arena::CreateMaybeMessage<::xla::ExecutableBuildOptionsProto>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace xla {

// ===================================================================

class ExecutableBuildOptionsProto :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:xla.ExecutableBuildOptionsProto) */ {
 public:
  ExecutableBuildOptionsProto();
  virtual ~ExecutableBuildOptionsProto();

  ExecutableBuildOptionsProto(const ExecutableBuildOptionsProto& from);
  ExecutableBuildOptionsProto(ExecutableBuildOptionsProto&& from) noexcept
    : ExecutableBuildOptionsProto() {
    *this = ::std::move(from);
  }

  inline ExecutableBuildOptionsProto& operator=(const ExecutableBuildOptionsProto& from) {
    CopyFrom(from);
    return *this;
  }
  inline ExecutableBuildOptionsProto& operator=(ExecutableBuildOptionsProto&& from) noexcept {
    if (GetArenaNoVirtual() == from.GetArenaNoVirtual()) {
      if (this != &from) InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return GetMetadataStatic().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return GetMetadataStatic().reflection;
  }
  static const ExecutableBuildOptionsProto& default_instance();

  static void InitAsDefaultInstance();  // FOR INTERNAL USE ONLY
  static inline const ExecutableBuildOptionsProto* internal_default_instance() {
    return reinterpret_cast<const ExecutableBuildOptionsProto*>(
               &_ExecutableBuildOptionsProto_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(ExecutableBuildOptionsProto& a, ExecutableBuildOptionsProto& b) {
    a.Swap(&b);
  }
  inline void Swap(ExecutableBuildOptionsProto* other) {
    if (other == this) return;
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  inline ExecutableBuildOptionsProto* New() const final {
    return CreateMaybeMessage<ExecutableBuildOptionsProto>(nullptr);
  }

  ExecutableBuildOptionsProto* New(::PROTOBUF_NAMESPACE_ID::Arena* arena) const final {
    return CreateMaybeMessage<ExecutableBuildOptionsProto>(arena);
  }
  void CopyFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void MergeFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void CopyFrom(const ExecutableBuildOptionsProto& from);
  void MergeFrom(const ExecutableBuildOptionsProto& from);
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  #if GOOGLE_PROTOBUF_ENABLE_EXPERIMENTAL_PARSER
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  #else
  bool MergePartialFromCodedStream(
      ::PROTOBUF_NAMESPACE_ID::io::CodedInputStream* input) final;
  #endif  // GOOGLE_PROTOBUF_ENABLE_EXPERIMENTAL_PARSER
  void SerializeWithCachedSizes(
      ::PROTOBUF_NAMESPACE_ID::io::CodedOutputStream* output) const final;
  ::PROTOBUF_NAMESPACE_ID::uint8* InternalSerializeWithCachedSizesToArray(
      ::PROTOBUF_NAMESPACE_ID::uint8* target) const final;
  int GetCachedSize() const final { return _cached_size_.Get(); }

  private:
  inline void SharedCtor();
  inline void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(ExecutableBuildOptionsProto* other);
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "xla.ExecutableBuildOptionsProto";
  }
  private:
  inline ::PROTOBUF_NAMESPACE_ID::Arena* GetArenaNoVirtual() const {
    return nullptr;
  }
  inline void* MaybeArenaPtr() const {
    return nullptr;
  }
  public:

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;
  private:
  static ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadataStatic() {
    ::PROTOBUF_NAMESPACE_ID::internal::AssignDescriptors(&::descriptor_table_tensorflow_2fcompiler_2fxla_2fpjrt_2fcompile_5foptions_2eproto);
    return ::descriptor_table_tensorflow_2fcompiler_2fxla_2fpjrt_2fcompile_5foptions_2eproto.file_level_metadata[kIndexInFileMessages];
  }

  public:

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kResultLayoutFieldNumber = 2,
    kDebugOptionsFieldNumber = 3,
    kDeviceAssignmentFieldNumber = 9,
    kDeviceOrdinalFieldNumber = 1,
    kNumReplicasFieldNumber = 4,
    kNumPartitionsFieldNumber = 5,
    kUseSpmdPartitioningFieldNumber = 6,
    kUseAutoSpmdPartitioningFieldNumber = 7,
    kDeduplicateHloFieldNumber = 8,
    kAliasPassthroughParamsFieldNumber = 10,
    kRunBackendOnlyFieldNumber = 11,
    kAllowSpmdShardingPropagationToOutputFieldNumber = 12,
  };
  // .xla.ShapeProto result_layout = 2;
  bool has_result_layout() const;
  void clear_result_layout();
  const ::xla::ShapeProto& result_layout() const;
  ::xla::ShapeProto* release_result_layout();
  ::xla::ShapeProto* mutable_result_layout();
  void set_allocated_result_layout(::xla::ShapeProto* result_layout);

  // .xla.DebugOptions debug_options = 3;
  bool has_debug_options() const;
  void clear_debug_options();
  const ::xla::DebugOptions& debug_options() const;
  ::xla::DebugOptions* release_debug_options();
  ::xla::DebugOptions* mutable_debug_options();
  void set_allocated_debug_options(::xla::DebugOptions* debug_options);

  // .xla.DeviceAssignmentProto device_assignment = 9;
  bool has_device_assignment() const;
  void clear_device_assignment();
  const ::xla::DeviceAssignmentProto& device_assignment() const;
  ::xla::DeviceAssignmentProto* release_device_assignment();
  ::xla::DeviceAssignmentProto* mutable_device_assignment();
  void set_allocated_device_assignment(::xla::DeviceAssignmentProto* device_assignment);

  // int64 device_ordinal = 1;
  void clear_device_ordinal();
  ::PROTOBUF_NAMESPACE_ID::int64 device_ordinal() const;
  void set_device_ordinal(::PROTOBUF_NAMESPACE_ID::int64 value);

  // int64 num_replicas = 4;
  void clear_num_replicas();
  ::PROTOBUF_NAMESPACE_ID::int64 num_replicas() const;
  void set_num_replicas(::PROTOBUF_NAMESPACE_ID::int64 value);

  // int64 num_partitions = 5;
  void clear_num_partitions();
  ::PROTOBUF_NAMESPACE_ID::int64 num_partitions() const;
  void set_num_partitions(::PROTOBUF_NAMESPACE_ID::int64 value);

  // bool use_spmd_partitioning = 6;
  void clear_use_spmd_partitioning();
  bool use_spmd_partitioning() const;
  void set_use_spmd_partitioning(bool value);

  // bool use_auto_spmd_partitioning = 7;
  void clear_use_auto_spmd_partitioning();
  bool use_auto_spmd_partitioning() const;
  void set_use_auto_spmd_partitioning(bool value);

  // bool deduplicate_hlo = 8;
  void clear_deduplicate_hlo();
  bool deduplicate_hlo() const;
  void set_deduplicate_hlo(bool value);

  // bool alias_passthrough_params = 10;
  void clear_alias_passthrough_params();
  bool alias_passthrough_params() const;
  void set_alias_passthrough_params(bool value);

  // bool run_backend_only = 11;
  void clear_run_backend_only();
  bool run_backend_only() const;
  void set_run_backend_only(bool value);

  // bool allow_spmd_sharding_propagation_to_output = 12;
  void clear_allow_spmd_sharding_propagation_to_output();
  bool allow_spmd_sharding_propagation_to_output() const;
  void set_allow_spmd_sharding_propagation_to_output(bool value);

  // @@protoc_insertion_point(class_scope:xla.ExecutableBuildOptionsProto)
 private:
  class _Internal;

  ::PROTOBUF_NAMESPACE_ID::internal::InternalMetadataWithArena _internal_metadata_;
  ::xla::ShapeProto* result_layout_;
  ::xla::DebugOptions* debug_options_;
  ::xla::DeviceAssignmentProto* device_assignment_;
  ::PROTOBUF_NAMESPACE_ID::int64 device_ordinal_;
  ::PROTOBUF_NAMESPACE_ID::int64 num_replicas_;
  ::PROTOBUF_NAMESPACE_ID::int64 num_partitions_;
  bool use_spmd_partitioning_;
  bool use_auto_spmd_partitioning_;
  bool deduplicate_hlo_;
  bool alias_passthrough_params_;
  bool run_backend_only_;
  bool allow_spmd_sharding_propagation_to_output_;
  mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  friend struct ::TableStruct_tensorflow_2fcompiler_2fxla_2fpjrt_2fcompile_5foptions_2eproto;
};
// -------------------------------------------------------------------

class CompileOptionsProto :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:xla.CompileOptionsProto) */ {
 public:
  CompileOptionsProto();
  virtual ~CompileOptionsProto();

  CompileOptionsProto(const CompileOptionsProto& from);
  CompileOptionsProto(CompileOptionsProto&& from) noexcept
    : CompileOptionsProto() {
    *this = ::std::move(from);
  }

  inline CompileOptionsProto& operator=(const CompileOptionsProto& from) {
    CopyFrom(from);
    return *this;
  }
  inline CompileOptionsProto& operator=(CompileOptionsProto&& from) noexcept {
    if (GetArenaNoVirtual() == from.GetArenaNoVirtual()) {
      if (this != &from) InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return GetMetadataStatic().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return GetMetadataStatic().reflection;
  }
  static const CompileOptionsProto& default_instance();

  static void InitAsDefaultInstance();  // FOR INTERNAL USE ONLY
  static inline const CompileOptionsProto* internal_default_instance() {
    return reinterpret_cast<const CompileOptionsProto*>(
               &_CompileOptionsProto_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    1;

  friend void swap(CompileOptionsProto& a, CompileOptionsProto& b) {
    a.Swap(&b);
  }
  inline void Swap(CompileOptionsProto* other) {
    if (other == this) return;
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  inline CompileOptionsProto* New() const final {
    return CreateMaybeMessage<CompileOptionsProto>(nullptr);
  }

  CompileOptionsProto* New(::PROTOBUF_NAMESPACE_ID::Arena* arena) const final {
    return CreateMaybeMessage<CompileOptionsProto>(arena);
  }
  void CopyFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void MergeFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void CopyFrom(const CompileOptionsProto& from);
  void MergeFrom(const CompileOptionsProto& from);
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  #if GOOGLE_PROTOBUF_ENABLE_EXPERIMENTAL_PARSER
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  #else
  bool MergePartialFromCodedStream(
      ::PROTOBUF_NAMESPACE_ID::io::CodedInputStream* input) final;
  #endif  // GOOGLE_PROTOBUF_ENABLE_EXPERIMENTAL_PARSER
  void SerializeWithCachedSizes(
      ::PROTOBUF_NAMESPACE_ID::io::CodedOutputStream* output) const final;
  ::PROTOBUF_NAMESPACE_ID::uint8* InternalSerializeWithCachedSizesToArray(
      ::PROTOBUF_NAMESPACE_ID::uint8* target) const final;
  int GetCachedSize() const final { return _cached_size_.Get(); }

  private:
  inline void SharedCtor();
  inline void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(CompileOptionsProto* other);
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "xla.CompileOptionsProto";
  }
  private:
  inline ::PROTOBUF_NAMESPACE_ID::Arena* GetArenaNoVirtual() const {
    return nullptr;
  }
  inline void* MaybeArenaPtr() const {
    return nullptr;
  }
  public:

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;
  private:
  static ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadataStatic() {
    ::PROTOBUF_NAMESPACE_ID::internal::AssignDescriptors(&::descriptor_table_tensorflow_2fcompiler_2fxla_2fpjrt_2fcompile_5foptions_2eproto);
    return ::descriptor_table_tensorflow_2fcompiler_2fxla_2fpjrt_2fcompile_5foptions_2eproto.file_level_metadata[kIndexInFileMessages];
  }

  public:

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kArgumentLayoutsFieldNumber = 1,
    kExecutableBuildOptionsFieldNumber = 3,
    kProfileVersionFieldNumber = 5,
    kParameterIsTupledArgumentsFieldNumber = 2,
    kCompilePortableExecutableFieldNumber = 4,
  };
  // repeated .xla.ShapeProto argument_layouts = 1;
  int argument_layouts_size() const;
  void clear_argument_layouts();
  ::xla::ShapeProto* mutable_argument_layouts(int index);
  ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::xla::ShapeProto >*
      mutable_argument_layouts();
  const ::xla::ShapeProto& argument_layouts(int index) const;
  ::xla::ShapeProto* add_argument_layouts();
  const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::xla::ShapeProto >&
      argument_layouts() const;

  // .xla.ExecutableBuildOptionsProto executable_build_options = 3;
  bool has_executable_build_options() const;
  void clear_executable_build_options();
  const ::xla::ExecutableBuildOptionsProto& executable_build_options() const;
  ::xla::ExecutableBuildOptionsProto* release_executable_build_options();
  ::xla::ExecutableBuildOptionsProto* mutable_executable_build_options();
  void set_allocated_executable_build_options(::xla::ExecutableBuildOptionsProto* executable_build_options);

  // int64 profile_version = 5;
  void clear_profile_version();
  ::PROTOBUF_NAMESPACE_ID::int64 profile_version() const;
  void set_profile_version(::PROTOBUF_NAMESPACE_ID::int64 value);

  // bool parameter_is_tupled_arguments = 2;
  void clear_parameter_is_tupled_arguments();
  bool parameter_is_tupled_arguments() const;
  void set_parameter_is_tupled_arguments(bool value);

  // bool compile_portable_executable = 4;
  void clear_compile_portable_executable();
  bool compile_portable_executable() const;
  void set_compile_portable_executable(bool value);

  // @@protoc_insertion_point(class_scope:xla.CompileOptionsProto)
 private:
  class _Internal;

  ::PROTOBUF_NAMESPACE_ID::internal::InternalMetadataWithArena _internal_metadata_;
  ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::xla::ShapeProto > argument_layouts_;
  ::xla::ExecutableBuildOptionsProto* executable_build_options_;
  ::PROTOBUF_NAMESPACE_ID::int64 profile_version_;
  bool parameter_is_tupled_arguments_;
  bool compile_portable_executable_;
  mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  friend struct ::TableStruct_tensorflow_2fcompiler_2fxla_2fpjrt_2fcompile_5foptions_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// ExecutableBuildOptionsProto

// int64 device_ordinal = 1;
inline void ExecutableBuildOptionsProto::clear_device_ordinal() {
  device_ordinal_ = PROTOBUF_LONGLONG(0);
}
inline ::PROTOBUF_NAMESPACE_ID::int64 ExecutableBuildOptionsProto::device_ordinal() const {
  // @@protoc_insertion_point(field_get:xla.ExecutableBuildOptionsProto.device_ordinal)
  return device_ordinal_;
}
inline void ExecutableBuildOptionsProto::set_device_ordinal(::PROTOBUF_NAMESPACE_ID::int64 value) {
  
  device_ordinal_ = value;
  // @@protoc_insertion_point(field_set:xla.ExecutableBuildOptionsProto.device_ordinal)
}

// .xla.ShapeProto result_layout = 2;
inline bool ExecutableBuildOptionsProto::has_result_layout() const {
  return this != internal_default_instance() && result_layout_ != nullptr;
}
inline const ::xla::ShapeProto& ExecutableBuildOptionsProto::result_layout() const {
  const ::xla::ShapeProto* p = result_layout_;
  // @@protoc_insertion_point(field_get:xla.ExecutableBuildOptionsProto.result_layout)
  return p != nullptr ? *p : *reinterpret_cast<const ::xla::ShapeProto*>(
      &::xla::_ShapeProto_default_instance_);
}
inline ::xla::ShapeProto* ExecutableBuildOptionsProto::release_result_layout() {
  // @@protoc_insertion_point(field_release:xla.ExecutableBuildOptionsProto.result_layout)
  
  ::xla::ShapeProto* temp = result_layout_;
  result_layout_ = nullptr;
  return temp;
}
inline ::xla::ShapeProto* ExecutableBuildOptionsProto::mutable_result_layout() {
  
  if (result_layout_ == nullptr) {
    auto* p = CreateMaybeMessage<::xla::ShapeProto>(GetArenaNoVirtual());
    result_layout_ = p;
  }
  // @@protoc_insertion_point(field_mutable:xla.ExecutableBuildOptionsProto.result_layout)
  return result_layout_;
}
inline void ExecutableBuildOptionsProto::set_allocated_result_layout(::xla::ShapeProto* result_layout) {
  ::PROTOBUF_NAMESPACE_ID::Arena* message_arena = GetArenaNoVirtual();
  if (message_arena == nullptr) {
    delete reinterpret_cast< ::PROTOBUF_NAMESPACE_ID::MessageLite*>(result_layout_);
  }
  if (result_layout) {
    ::PROTOBUF_NAMESPACE_ID::Arena* submessage_arena =
      reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(result_layout)->GetArena();
    if (message_arena != submessage_arena) {
      result_layout = ::PROTOBUF_NAMESPACE_ID::internal::GetOwnedMessage(
          message_arena, result_layout, submessage_arena);
    }
    
  } else {
    
  }
  result_layout_ = result_layout;
  // @@protoc_insertion_point(field_set_allocated:xla.ExecutableBuildOptionsProto.result_layout)
}

// .xla.DebugOptions debug_options = 3;
inline bool ExecutableBuildOptionsProto::has_debug_options() const {
  return this != internal_default_instance() && debug_options_ != nullptr;
}
inline const ::xla::DebugOptions& ExecutableBuildOptionsProto::debug_options() const {
  const ::xla::DebugOptions* p = debug_options_;
  // @@protoc_insertion_point(field_get:xla.ExecutableBuildOptionsProto.debug_options)
  return p != nullptr ? *p : *reinterpret_cast<const ::xla::DebugOptions*>(
      &::xla::_DebugOptions_default_instance_);
}
inline ::xla::DebugOptions* ExecutableBuildOptionsProto::release_debug_options() {
  // @@protoc_insertion_point(field_release:xla.ExecutableBuildOptionsProto.debug_options)
  
  ::xla::DebugOptions* temp = debug_options_;
  debug_options_ = nullptr;
  return temp;
}
inline ::xla::DebugOptions* ExecutableBuildOptionsProto::mutable_debug_options() {
  
  if (debug_options_ == nullptr) {
    auto* p = CreateMaybeMessage<::xla::DebugOptions>(GetArenaNoVirtual());
    debug_options_ = p;
  }
  // @@protoc_insertion_point(field_mutable:xla.ExecutableBuildOptionsProto.debug_options)
  return debug_options_;
}
inline void ExecutableBuildOptionsProto::set_allocated_debug_options(::xla::DebugOptions* debug_options) {
  ::PROTOBUF_NAMESPACE_ID::Arena* message_arena = GetArenaNoVirtual();
  if (message_arena == nullptr) {
    delete reinterpret_cast< ::PROTOBUF_NAMESPACE_ID::MessageLite*>(debug_options_);
  }
  if (debug_options) {
    ::PROTOBUF_NAMESPACE_ID::Arena* submessage_arena = nullptr;
    if (message_arena != submessage_arena) {
      debug_options = ::PROTOBUF_NAMESPACE_ID::internal::GetOwnedMessage(
          message_arena, debug_options, submessage_arena);
    }
    
  } else {
    
  }
  debug_options_ = debug_options;
  // @@protoc_insertion_point(field_set_allocated:xla.ExecutableBuildOptionsProto.debug_options)
}

// int64 num_replicas = 4;
inline void ExecutableBuildOptionsProto::clear_num_replicas() {
  num_replicas_ = PROTOBUF_LONGLONG(0);
}
inline ::PROTOBUF_NAMESPACE_ID::int64 ExecutableBuildOptionsProto::num_replicas() const {
  // @@protoc_insertion_point(field_get:xla.ExecutableBuildOptionsProto.num_replicas)
  return num_replicas_;
}
inline void ExecutableBuildOptionsProto::set_num_replicas(::PROTOBUF_NAMESPACE_ID::int64 value) {
  
  num_replicas_ = value;
  // @@protoc_insertion_point(field_set:xla.ExecutableBuildOptionsProto.num_replicas)
}

// int64 num_partitions = 5;
inline void ExecutableBuildOptionsProto::clear_num_partitions() {
  num_partitions_ = PROTOBUF_LONGLONG(0);
}
inline ::PROTOBUF_NAMESPACE_ID::int64 ExecutableBuildOptionsProto::num_partitions() const {
  // @@protoc_insertion_point(field_get:xla.ExecutableBuildOptionsProto.num_partitions)
  return num_partitions_;
}
inline void ExecutableBuildOptionsProto::set_num_partitions(::PROTOBUF_NAMESPACE_ID::int64 value) {
  
  num_partitions_ = value;
  // @@protoc_insertion_point(field_set:xla.ExecutableBuildOptionsProto.num_partitions)
}

// bool use_spmd_partitioning = 6;
inline void ExecutableBuildOptionsProto::clear_use_spmd_partitioning() {
  use_spmd_partitioning_ = false;
}
inline bool ExecutableBuildOptionsProto::use_spmd_partitioning() const {
  // @@protoc_insertion_point(field_get:xla.ExecutableBuildOptionsProto.use_spmd_partitioning)
  return use_spmd_partitioning_;
}
inline void ExecutableBuildOptionsProto::set_use_spmd_partitioning(bool value) {
  
  use_spmd_partitioning_ = value;
  // @@protoc_insertion_point(field_set:xla.ExecutableBuildOptionsProto.use_spmd_partitioning)
}

// bool use_auto_spmd_partitioning = 7;
inline void ExecutableBuildOptionsProto::clear_use_auto_spmd_partitioning() {
  use_auto_spmd_partitioning_ = false;
}
inline bool ExecutableBuildOptionsProto::use_auto_spmd_partitioning() const {
  // @@protoc_insertion_point(field_get:xla.ExecutableBuildOptionsProto.use_auto_spmd_partitioning)
  return use_auto_spmd_partitioning_;
}
inline void ExecutableBuildOptionsProto::set_use_auto_spmd_partitioning(bool value) {
  
  use_auto_spmd_partitioning_ = value;
  // @@protoc_insertion_point(field_set:xla.ExecutableBuildOptionsProto.use_auto_spmd_partitioning)
}

// bool deduplicate_hlo = 8;
inline void ExecutableBuildOptionsProto::clear_deduplicate_hlo() {
  deduplicate_hlo_ = false;
}
inline bool ExecutableBuildOptionsProto::deduplicate_hlo() const {
  // @@protoc_insertion_point(field_get:xla.ExecutableBuildOptionsProto.deduplicate_hlo)
  return deduplicate_hlo_;
}
inline void ExecutableBuildOptionsProto::set_deduplicate_hlo(bool value) {
  
  deduplicate_hlo_ = value;
  // @@protoc_insertion_point(field_set:xla.ExecutableBuildOptionsProto.deduplicate_hlo)
}

// .xla.DeviceAssignmentProto device_assignment = 9;
inline bool ExecutableBuildOptionsProto::has_device_assignment() const {
  return this != internal_default_instance() && device_assignment_ != nullptr;
}
inline const ::xla::DeviceAssignmentProto& ExecutableBuildOptionsProto::device_assignment() const {
  const ::xla::DeviceAssignmentProto* p = device_assignment_;
  // @@protoc_insertion_point(field_get:xla.ExecutableBuildOptionsProto.device_assignment)
  return p != nullptr ? *p : *reinterpret_cast<const ::xla::DeviceAssignmentProto*>(
      &::xla::_DeviceAssignmentProto_default_instance_);
}
inline ::xla::DeviceAssignmentProto* ExecutableBuildOptionsProto::release_device_assignment() {
  // @@protoc_insertion_point(field_release:xla.ExecutableBuildOptionsProto.device_assignment)
  
  ::xla::DeviceAssignmentProto* temp = device_assignment_;
  device_assignment_ = nullptr;
  return temp;
}
inline ::xla::DeviceAssignmentProto* ExecutableBuildOptionsProto::mutable_device_assignment() {
  
  if (device_assignment_ == nullptr) {
    auto* p = CreateMaybeMessage<::xla::DeviceAssignmentProto>(GetArenaNoVirtual());
    device_assignment_ = p;
  }
  // @@protoc_insertion_point(field_mutable:xla.ExecutableBuildOptionsProto.device_assignment)
  return device_assignment_;
}
inline void ExecutableBuildOptionsProto::set_allocated_device_assignment(::xla::DeviceAssignmentProto* device_assignment) {
  ::PROTOBUF_NAMESPACE_ID::Arena* message_arena = GetArenaNoVirtual();
  if (message_arena == nullptr) {
    delete reinterpret_cast< ::PROTOBUF_NAMESPACE_ID::MessageLite*>(device_assignment_);
  }
  if (device_assignment) {
    ::PROTOBUF_NAMESPACE_ID::Arena* submessage_arena =
      reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(device_assignment)->GetArena();
    if (message_arena != submessage_arena) {
      device_assignment = ::PROTOBUF_NAMESPACE_ID::internal::GetOwnedMessage(
          message_arena, device_assignment, submessage_arena);
    }
    
  } else {
    
  }
  device_assignment_ = device_assignment;
  // @@protoc_insertion_point(field_set_allocated:xla.ExecutableBuildOptionsProto.device_assignment)
}

// bool alias_passthrough_params = 10;
inline void ExecutableBuildOptionsProto::clear_alias_passthrough_params() {
  alias_passthrough_params_ = false;
}
inline bool ExecutableBuildOptionsProto::alias_passthrough_params() const {
  // @@protoc_insertion_point(field_get:xla.ExecutableBuildOptionsProto.alias_passthrough_params)
  return alias_passthrough_params_;
}
inline void ExecutableBuildOptionsProto::set_alias_passthrough_params(bool value) {
  
  alias_passthrough_params_ = value;
  // @@protoc_insertion_point(field_set:xla.ExecutableBuildOptionsProto.alias_passthrough_params)
}

// bool run_backend_only = 11;
inline void ExecutableBuildOptionsProto::clear_run_backend_only() {
  run_backend_only_ = false;
}
inline bool ExecutableBuildOptionsProto::run_backend_only() const {
  // @@protoc_insertion_point(field_get:xla.ExecutableBuildOptionsProto.run_backend_only)
  return run_backend_only_;
}
inline void ExecutableBuildOptionsProto::set_run_backend_only(bool value) {
  
  run_backend_only_ = value;
  // @@protoc_insertion_point(field_set:xla.ExecutableBuildOptionsProto.run_backend_only)
}

// bool allow_spmd_sharding_propagation_to_output = 12;
inline void ExecutableBuildOptionsProto::clear_allow_spmd_sharding_propagation_to_output() {
  allow_spmd_sharding_propagation_to_output_ = false;
}
inline bool ExecutableBuildOptionsProto::allow_spmd_sharding_propagation_to_output() const {
  // @@protoc_insertion_point(field_get:xla.ExecutableBuildOptionsProto.allow_spmd_sharding_propagation_to_output)
  return allow_spmd_sharding_propagation_to_output_;
}
inline void ExecutableBuildOptionsProto::set_allow_spmd_sharding_propagation_to_output(bool value) {
  
  allow_spmd_sharding_propagation_to_output_ = value;
  // @@protoc_insertion_point(field_set:xla.ExecutableBuildOptionsProto.allow_spmd_sharding_propagation_to_output)
}

// -------------------------------------------------------------------

// CompileOptionsProto

// repeated .xla.ShapeProto argument_layouts = 1;
inline int CompileOptionsProto::argument_layouts_size() const {
  return argument_layouts_.size();
}
inline ::xla::ShapeProto* CompileOptionsProto::mutable_argument_layouts(int index) {
  // @@protoc_insertion_point(field_mutable:xla.CompileOptionsProto.argument_layouts)
  return argument_layouts_.Mutable(index);
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::xla::ShapeProto >*
CompileOptionsProto::mutable_argument_layouts() {
  // @@protoc_insertion_point(field_mutable_list:xla.CompileOptionsProto.argument_layouts)
  return &argument_layouts_;
}
inline const ::xla::ShapeProto& CompileOptionsProto::argument_layouts(int index) const {
  // @@protoc_insertion_point(field_get:xla.CompileOptionsProto.argument_layouts)
  return argument_layouts_.Get(index);
}
inline ::xla::ShapeProto* CompileOptionsProto::add_argument_layouts() {
  // @@protoc_insertion_point(field_add:xla.CompileOptionsProto.argument_layouts)
  return argument_layouts_.Add();
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::xla::ShapeProto >&
CompileOptionsProto::argument_layouts() const {
  // @@protoc_insertion_point(field_list:xla.CompileOptionsProto.argument_layouts)
  return argument_layouts_;
}

// bool parameter_is_tupled_arguments = 2;
inline void CompileOptionsProto::clear_parameter_is_tupled_arguments() {
  parameter_is_tupled_arguments_ = false;
}
inline bool CompileOptionsProto::parameter_is_tupled_arguments() const {
  // @@protoc_insertion_point(field_get:xla.CompileOptionsProto.parameter_is_tupled_arguments)
  return parameter_is_tupled_arguments_;
}
inline void CompileOptionsProto::set_parameter_is_tupled_arguments(bool value) {
  
  parameter_is_tupled_arguments_ = value;
  // @@protoc_insertion_point(field_set:xla.CompileOptionsProto.parameter_is_tupled_arguments)
}

// .xla.ExecutableBuildOptionsProto executable_build_options = 3;
inline bool CompileOptionsProto::has_executable_build_options() const {
  return this != internal_default_instance() && executable_build_options_ != nullptr;
}
inline void CompileOptionsProto::clear_executable_build_options() {
  if (GetArenaNoVirtual() == nullptr && executable_build_options_ != nullptr) {
    delete executable_build_options_;
  }
  executable_build_options_ = nullptr;
}
inline const ::xla::ExecutableBuildOptionsProto& CompileOptionsProto::executable_build_options() const {
  const ::xla::ExecutableBuildOptionsProto* p = executable_build_options_;
  // @@protoc_insertion_point(field_get:xla.CompileOptionsProto.executable_build_options)
  return p != nullptr ? *p : *reinterpret_cast<const ::xla::ExecutableBuildOptionsProto*>(
      &::xla::_ExecutableBuildOptionsProto_default_instance_);
}
inline ::xla::ExecutableBuildOptionsProto* CompileOptionsProto::release_executable_build_options() {
  // @@protoc_insertion_point(field_release:xla.CompileOptionsProto.executable_build_options)
  
  ::xla::ExecutableBuildOptionsProto* temp = executable_build_options_;
  executable_build_options_ = nullptr;
  return temp;
}
inline ::xla::ExecutableBuildOptionsProto* CompileOptionsProto::mutable_executable_build_options() {
  
  if (executable_build_options_ == nullptr) {
    auto* p = CreateMaybeMessage<::xla::ExecutableBuildOptionsProto>(GetArenaNoVirtual());
    executable_build_options_ = p;
  }
  // @@protoc_insertion_point(field_mutable:xla.CompileOptionsProto.executable_build_options)
  return executable_build_options_;
}
inline void CompileOptionsProto::set_allocated_executable_build_options(::xla::ExecutableBuildOptionsProto* executable_build_options) {
  ::PROTOBUF_NAMESPACE_ID::Arena* message_arena = GetArenaNoVirtual();
  if (message_arena == nullptr) {
    delete executable_build_options_;
  }
  if (executable_build_options) {
    ::PROTOBUF_NAMESPACE_ID::Arena* submessage_arena = nullptr;
    if (message_arena != submessage_arena) {
      executable_build_options = ::PROTOBUF_NAMESPACE_ID::internal::GetOwnedMessage(
          message_arena, executable_build_options, submessage_arena);
    }
    
  } else {
    
  }
  executable_build_options_ = executable_build_options;
  // @@protoc_insertion_point(field_set_allocated:xla.CompileOptionsProto.executable_build_options)
}

// bool compile_portable_executable = 4;
inline void CompileOptionsProto::clear_compile_portable_executable() {
  compile_portable_executable_ = false;
}
inline bool CompileOptionsProto::compile_portable_executable() const {
  // @@protoc_insertion_point(field_get:xla.CompileOptionsProto.compile_portable_executable)
  return compile_portable_executable_;
}
inline void CompileOptionsProto::set_compile_portable_executable(bool value) {
  
  compile_portable_executable_ = value;
  // @@protoc_insertion_point(field_set:xla.CompileOptionsProto.compile_portable_executable)
}

// int64 profile_version = 5;
inline void CompileOptionsProto::clear_profile_version() {
  profile_version_ = PROTOBUF_LONGLONG(0);
}
inline ::PROTOBUF_NAMESPACE_ID::int64 CompileOptionsProto::profile_version() const {
  // @@protoc_insertion_point(field_get:xla.CompileOptionsProto.profile_version)
  return profile_version_;
}
inline void CompileOptionsProto::set_profile_version(::PROTOBUF_NAMESPACE_ID::int64 value) {
  
  profile_version_ = value;
  // @@protoc_insertion_point(field_set:xla.CompileOptionsProto.profile_version)
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__
// -------------------------------------------------------------------


// @@protoc_insertion_point(namespace_scope)

}  // namespace xla

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcompiler_2fxla_2fpjrt_2fcompile_5foptions_2eproto
