// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/core/protobuf/fingerprint.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fprotobuf_2ffingerprint_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fprotobuf_2ffingerprint_2eproto

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
#include "tensorflow/core/framework/versions.pb.h"
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_tensorflow_2fcore_2fprotobuf_2ffingerprint_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_tensorflow_2fcore_2fprotobuf_2ffingerprint_2eproto {
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTableField entries[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::AuxillaryParseTableField aux[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTable schema[1]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::FieldMetadata field_metadata[];
  static const ::PROTOBUF_NAMESPACE_ID::internal::SerializationTable serialization_table[];
  static const ::PROTOBUF_NAMESPACE_ID::uint32 offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_tensorflow_2fcore_2fprotobuf_2ffingerprint_2eproto;
namespace tensorflow {
class FingerprintDef;
class FingerprintDefDefaultTypeInternal;
extern FingerprintDefDefaultTypeInternal _FingerprintDef_default_instance_;
}  // namespace tensorflow
PROTOBUF_NAMESPACE_OPEN
template<> ::tensorflow::FingerprintDef* Arena::CreateMaybeMessage<::tensorflow::FingerprintDef>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace tensorflow {

// ===================================================================

class FingerprintDef :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.FingerprintDef) */ {
 public:
  FingerprintDef();
  virtual ~FingerprintDef();

  FingerprintDef(const FingerprintDef& from);
  FingerprintDef(FingerprintDef&& from) noexcept
    : FingerprintDef() {
    *this = ::std::move(from);
  }

  inline FingerprintDef& operator=(const FingerprintDef& from) {
    CopyFrom(from);
    return *this;
  }
  inline FingerprintDef& operator=(FingerprintDef&& from) noexcept {
    if (GetArenaNoVirtual() == from.GetArenaNoVirtual()) {
      if (this != &from) InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  inline ::PROTOBUF_NAMESPACE_ID::Arena* GetArena() const final {
    return GetArenaNoVirtual();
  }
  inline void* GetMaybeArenaPointer() const final {
    return MaybeArenaPtr();
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
  static const FingerprintDef& default_instance();

  static void InitAsDefaultInstance();  // FOR INTERNAL USE ONLY
  static inline const FingerprintDef* internal_default_instance() {
    return reinterpret_cast<const FingerprintDef*>(
               &_FingerprintDef_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(FingerprintDef& a, FingerprintDef& b) {
    a.Swap(&b);
  }
  inline void Swap(FingerprintDef* other) {
    if (other == this) return;
    if (GetArenaNoVirtual() == other->GetArenaNoVirtual()) {
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(FingerprintDef* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetArenaNoVirtual() == other->GetArenaNoVirtual());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  inline FingerprintDef* New() const final {
    return CreateMaybeMessage<FingerprintDef>(nullptr);
  }

  FingerprintDef* New(::PROTOBUF_NAMESPACE_ID::Arena* arena) const final {
    return CreateMaybeMessage<FingerprintDef>(arena);
  }
  void CopyFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void MergeFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void CopyFrom(const FingerprintDef& from);
  void MergeFrom(const FingerprintDef& from);
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
  void InternalSwap(FingerprintDef* other);
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.FingerprintDef";
  }
  protected:
  explicit FingerprintDef(::PROTOBUF_NAMESPACE_ID::Arena* arena);
  private:
  static void ArenaDtor(void* object);
  inline void RegisterArenaDtor(::PROTOBUF_NAMESPACE_ID::Arena* arena);
  private:
  inline ::PROTOBUF_NAMESPACE_ID::Arena* GetArenaNoVirtual() const {
    return _internal_metadata_.arena();
  }
  inline void* MaybeArenaPtr() const {
    return _internal_metadata_.raw_arena_ptr();
  }
  public:

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;
  private:
  static ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadataStatic() {
    ::PROTOBUF_NAMESPACE_ID::internal::AssignDescriptors(&::descriptor_table_tensorflow_2fcore_2fprotobuf_2ffingerprint_2eproto);
    return ::descriptor_table_tensorflow_2fcore_2fprotobuf_2ffingerprint_2eproto.file_level_metadata[kIndexInFileMessages];
  }

  public:

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kVersionFieldNumber = 6,
    kGraphDefChecksumFieldNumber = 1,
    kGraphDefProgramHashFieldNumber = 2,
    kSignatureDefHashFieldNumber = 3,
    kSavedObjectGraphHashFieldNumber = 4,
    kCheckpointHashFieldNumber = 5,
  };
  // .tensorflow.VersionDef version = 6;
  bool has_version() const;
  void clear_version();
  const ::tensorflow::VersionDef& version() const;
  ::tensorflow::VersionDef* release_version();
  ::tensorflow::VersionDef* mutable_version();
  void set_allocated_version(::tensorflow::VersionDef* version);
  void unsafe_arena_set_allocated_version(
      ::tensorflow::VersionDef* version);
  ::tensorflow::VersionDef* unsafe_arena_release_version();

  // uint64 graph_def_checksum = 1;
  void clear_graph_def_checksum();
  ::PROTOBUF_NAMESPACE_ID::uint64 graph_def_checksum() const;
  void set_graph_def_checksum(::PROTOBUF_NAMESPACE_ID::uint64 value);

  // uint64 graph_def_program_hash = 2;
  void clear_graph_def_program_hash();
  ::PROTOBUF_NAMESPACE_ID::uint64 graph_def_program_hash() const;
  void set_graph_def_program_hash(::PROTOBUF_NAMESPACE_ID::uint64 value);

  // uint64 signature_def_hash = 3;
  void clear_signature_def_hash();
  ::PROTOBUF_NAMESPACE_ID::uint64 signature_def_hash() const;
  void set_signature_def_hash(::PROTOBUF_NAMESPACE_ID::uint64 value);

  // uint64 saved_object_graph_hash = 4;
  void clear_saved_object_graph_hash();
  ::PROTOBUF_NAMESPACE_ID::uint64 saved_object_graph_hash() const;
  void set_saved_object_graph_hash(::PROTOBUF_NAMESPACE_ID::uint64 value);

  // uint64 checkpoint_hash = 5;
  void clear_checkpoint_hash();
  ::PROTOBUF_NAMESPACE_ID::uint64 checkpoint_hash() const;
  void set_checkpoint_hash(::PROTOBUF_NAMESPACE_ID::uint64 value);

  // @@protoc_insertion_point(class_scope:tensorflow.FingerprintDef)
 private:
  class _Internal;

  ::PROTOBUF_NAMESPACE_ID::internal::InternalMetadataWithArena _internal_metadata_;
  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  ::tensorflow::VersionDef* version_;
  ::PROTOBUF_NAMESPACE_ID::uint64 graph_def_checksum_;
  ::PROTOBUF_NAMESPACE_ID::uint64 graph_def_program_hash_;
  ::PROTOBUF_NAMESPACE_ID::uint64 signature_def_hash_;
  ::PROTOBUF_NAMESPACE_ID::uint64 saved_object_graph_hash_;
  ::PROTOBUF_NAMESPACE_ID::uint64 checkpoint_hash_;
  mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  friend struct ::TableStruct_tensorflow_2fcore_2fprotobuf_2ffingerprint_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// FingerprintDef

// uint64 graph_def_checksum = 1;
inline void FingerprintDef::clear_graph_def_checksum() {
  graph_def_checksum_ = PROTOBUF_ULONGLONG(0);
}
inline ::PROTOBUF_NAMESPACE_ID::uint64 FingerprintDef::graph_def_checksum() const {
  // @@protoc_insertion_point(field_get:tensorflow.FingerprintDef.graph_def_checksum)
  return graph_def_checksum_;
}
inline void FingerprintDef::set_graph_def_checksum(::PROTOBUF_NAMESPACE_ID::uint64 value) {
  
  graph_def_checksum_ = value;
  // @@protoc_insertion_point(field_set:tensorflow.FingerprintDef.graph_def_checksum)
}

// uint64 graph_def_program_hash = 2;
inline void FingerprintDef::clear_graph_def_program_hash() {
  graph_def_program_hash_ = PROTOBUF_ULONGLONG(0);
}
inline ::PROTOBUF_NAMESPACE_ID::uint64 FingerprintDef::graph_def_program_hash() const {
  // @@protoc_insertion_point(field_get:tensorflow.FingerprintDef.graph_def_program_hash)
  return graph_def_program_hash_;
}
inline void FingerprintDef::set_graph_def_program_hash(::PROTOBUF_NAMESPACE_ID::uint64 value) {
  
  graph_def_program_hash_ = value;
  // @@protoc_insertion_point(field_set:tensorflow.FingerprintDef.graph_def_program_hash)
}

// uint64 signature_def_hash = 3;
inline void FingerprintDef::clear_signature_def_hash() {
  signature_def_hash_ = PROTOBUF_ULONGLONG(0);
}
inline ::PROTOBUF_NAMESPACE_ID::uint64 FingerprintDef::signature_def_hash() const {
  // @@protoc_insertion_point(field_get:tensorflow.FingerprintDef.signature_def_hash)
  return signature_def_hash_;
}
inline void FingerprintDef::set_signature_def_hash(::PROTOBUF_NAMESPACE_ID::uint64 value) {
  
  signature_def_hash_ = value;
  // @@protoc_insertion_point(field_set:tensorflow.FingerprintDef.signature_def_hash)
}

// uint64 saved_object_graph_hash = 4;
inline void FingerprintDef::clear_saved_object_graph_hash() {
  saved_object_graph_hash_ = PROTOBUF_ULONGLONG(0);
}
inline ::PROTOBUF_NAMESPACE_ID::uint64 FingerprintDef::saved_object_graph_hash() const {
  // @@protoc_insertion_point(field_get:tensorflow.FingerprintDef.saved_object_graph_hash)
  return saved_object_graph_hash_;
}
inline void FingerprintDef::set_saved_object_graph_hash(::PROTOBUF_NAMESPACE_ID::uint64 value) {
  
  saved_object_graph_hash_ = value;
  // @@protoc_insertion_point(field_set:tensorflow.FingerprintDef.saved_object_graph_hash)
}

// uint64 checkpoint_hash = 5;
inline void FingerprintDef::clear_checkpoint_hash() {
  checkpoint_hash_ = PROTOBUF_ULONGLONG(0);
}
inline ::PROTOBUF_NAMESPACE_ID::uint64 FingerprintDef::checkpoint_hash() const {
  // @@protoc_insertion_point(field_get:tensorflow.FingerprintDef.checkpoint_hash)
  return checkpoint_hash_;
}
inline void FingerprintDef::set_checkpoint_hash(::PROTOBUF_NAMESPACE_ID::uint64 value) {
  
  checkpoint_hash_ = value;
  // @@protoc_insertion_point(field_set:tensorflow.FingerprintDef.checkpoint_hash)
}

// .tensorflow.VersionDef version = 6;
inline bool FingerprintDef::has_version() const {
  return this != internal_default_instance() && version_ != nullptr;
}
inline const ::tensorflow::VersionDef& FingerprintDef::version() const {
  const ::tensorflow::VersionDef* p = version_;
  // @@protoc_insertion_point(field_get:tensorflow.FingerprintDef.version)
  return p != nullptr ? *p : *reinterpret_cast<const ::tensorflow::VersionDef*>(
      &::tensorflow::_VersionDef_default_instance_);
}
inline ::tensorflow::VersionDef* FingerprintDef::release_version() {
  // @@protoc_insertion_point(field_release:tensorflow.FingerprintDef.version)
  
  ::tensorflow::VersionDef* temp = version_;
  if (GetArenaNoVirtual() != nullptr) {
    temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  }
  version_ = nullptr;
  return temp;
}
inline ::tensorflow::VersionDef* FingerprintDef::unsafe_arena_release_version() {
  // @@protoc_insertion_point(field_unsafe_arena_release:tensorflow.FingerprintDef.version)
  
  ::tensorflow::VersionDef* temp = version_;
  version_ = nullptr;
  return temp;
}
inline ::tensorflow::VersionDef* FingerprintDef::mutable_version() {
  
  if (version_ == nullptr) {
    auto* p = CreateMaybeMessage<::tensorflow::VersionDef>(GetArenaNoVirtual());
    version_ = p;
  }
  // @@protoc_insertion_point(field_mutable:tensorflow.FingerprintDef.version)
  return version_;
}
inline void FingerprintDef::set_allocated_version(::tensorflow::VersionDef* version) {
  ::PROTOBUF_NAMESPACE_ID::Arena* message_arena = GetArenaNoVirtual();
  if (message_arena == nullptr) {
    delete reinterpret_cast< ::PROTOBUF_NAMESPACE_ID::MessageLite*>(version_);
  }
  if (version) {
    ::PROTOBUF_NAMESPACE_ID::Arena* submessage_arena =
      reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(version)->GetArena();
    if (message_arena != submessage_arena) {
      version = ::PROTOBUF_NAMESPACE_ID::internal::GetOwnedMessage(
          message_arena, version, submessage_arena);
    }
    
  } else {
    
  }
  version_ = version;
  // @@protoc_insertion_point(field_set_allocated:tensorflow.FingerprintDef.version)
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__

// @@protoc_insertion_point(namespace_scope)

}  // namespace tensorflow

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fprotobuf_2ffingerprint_2eproto
