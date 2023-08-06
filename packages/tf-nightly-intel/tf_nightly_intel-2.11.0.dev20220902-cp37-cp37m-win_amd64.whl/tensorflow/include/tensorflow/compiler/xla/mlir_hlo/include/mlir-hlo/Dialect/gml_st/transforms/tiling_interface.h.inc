/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Declarations                                                     *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace gml_st {
class TilingInterface;
namespace detail {
struct TilingInterfaceInterfaceTraits {
  struct Concept {
    SmallVector<Value> (*getDestinationOperands)(const Concept *impl, ::mlir::Operation *, OpBuilder &);
    SmallVector<StringRef> (*getLoopIteratorTypes)(const Concept *impl, ::mlir::Operation *);
    SmallVector<Range> (*getIterationDomain)(const Concept *impl, ::mlir::Operation *, OpBuilder &);
    mlir::gml_st::TilingInterface (*getTiledImplementation)(const Concept *impl, ::mlir::Operation *, OpBuilder &, ValueRange, ArrayRef<OpFoldResult>, ArrayRef<OpFoldResult>, bool );
    FailureOr<Value> (*generateResultTileValue)(const Concept *impl, ::mlir::Operation *, OpBuilder &, unsigned, ValueRange, ArrayRef<OpFoldResult>, ArrayRef<OpFoldResult>, bool);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = ::mlir::gml_st::TilingInterface;
    Model() : Concept{getDestinationOperands, getLoopIteratorTypes, getIterationDomain, getTiledImplementation, generateResultTileValue} {}

    static inline SmallVector<Value> getDestinationOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b);
    static inline SmallVector<StringRef> getLoopIteratorTypes(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline SmallVector<Range> getIterationDomain(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b);
    static inline mlir::gml_st::TilingInterface getTiledImplementation(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b, ValueRange dest, ArrayRef<OpFoldResult> offsets, ArrayRef<OpFoldResult> sizes, bool  tileDestOperands);
    static inline FailureOr<Value> generateResultTileValue(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b, unsigned resultNumber, ValueRange dest, ArrayRef<OpFoldResult> offsets, ArrayRef<OpFoldResult> sizes, bool tileDestOperands);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = ::mlir::gml_st::TilingInterface;
    FallbackModel() : Concept{getDestinationOperands, getLoopIteratorTypes, getIterationDomain, getTiledImplementation, generateResultTileValue} {}

    static inline SmallVector<Value> getDestinationOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b);
    static inline SmallVector<StringRef> getLoopIteratorTypes(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline SmallVector<Range> getIterationDomain(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b);
    static inline mlir::gml_st::TilingInterface getTiledImplementation(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b, ValueRange dest, ArrayRef<OpFoldResult> offsets, ArrayRef<OpFoldResult> sizes, bool  tileDestOperands);
    static inline FailureOr<Value> generateResultTileValue(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b, unsigned resultNumber, ValueRange dest, ArrayRef<OpFoldResult> offsets, ArrayRef<OpFoldResult> sizes, bool tileDestOperands);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
    using ConcreteEntity = ConcreteOp;
  };
};template <typename ConcreteOp>
struct TilingInterfaceTrait;

} // namespace detail
class TilingInterface : public ::mlir::OpInterface<TilingInterface, detail::TilingInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<TilingInterface, detail::TilingInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::TilingInterfaceTrait<ConcreteOp> {};
  /// 
  ///           Returns a list of operands into which the result of the
  ///           tiled implementation is written into. With `tensor`
  ///           operands, this will be used as the initial tensor into which
  ///           the tiled results are inserted into. With `memref` operands,
  ///           this will be the operand into which the result of the tiled
  ///           operation is written into.
  SmallVector<Value> getDestinationOperands(OpBuilder & b);
  /// 
  ///           Returns a list of `StringRef`s that describe the number of
  ///           loops and the iterator types of the operation. The list is
  ///           expected to use
  ///           `getParallelIteratorTypeName()`/`getReductionIteratorTypeName()`
  ///           from MLIR Structured Op Utils.
  SmallVector<StringRef> getLoopIteratorTypes();
  /// 
  ///           Returns a list of ranges that describe the loop bounds and
  ///           step for the loops of the operation.
  SmallVector<Range> getIterationDomain(OpBuilder & b);
  /// 
  ///           Method to generate the tiled implementation of an operation.
  /// 
  ///           The iteration space of the operation is returned by
  ///           `getIterationDomain`. The caller provides the information of the
  ///           tile within this iteration space whose implementation the
  ///           caller needs.
  ///           - `dest` are the Value into which the result of the tiled
  ///             operation is to be inserted into. The type of the `dest`
  ///             Values is same as the types returned by
  ///             `getDestinationOperands` method.
  ///           - `offsets` provides the offset of the tile in the coordinate system
  ///             of the original iteration space, i.e., if an iteration space
  ///             dimension had non-zero offset, it must be included in the offset
  ///             provided here (as opposed to zero-based offset "relative" to the
  ///             iteration space).
  ///           - `sizes` provides the size of the tile.
  ///           - `tileDestOperands` specifies whether to also tile `dest` operands
  ///             or not. Avoiding tiling `dest` operands can be useful for
  ///             composition with various looping container ops.
  /// 
  ///           The method returns the operation that is the tiled
  ///           implementation.
  mlir::gml_st::TilingInterface getTiledImplementation(OpBuilder & b, ValueRange dest, ArrayRef<OpFoldResult> offsets, ArrayRef<OpFoldResult> sizes, bool  tileDestOperands);
  /// 
  ///           Generates the IR that computes the tile of a result of the
  ///           operation.  The `offsets` and `sizes` describe the tile of
  ///           the output required. This is different from
  ///           `getTiledImplementation` which generates the tiled
  ///           implementation of the operation given a tile of the
  ///           iteration space. This method generates a tiled
  ///           implementation of the operation based on the tile of the
  ///           result required. This method enables fusion by using tile
  ///           and fuse. The method returns failure if the operation can't be
  ///           tiled to generate the result tile. In practical terms this
  ///           implies it cannot be tiled and fused with its consumers.
  /// 
  ///           - `dest` are the Value into which the result of the tiled
  ///             operation is to be inserted into. The type of the `dest`
  ///             Values is same as the types returned by
  ///             `getDestinationOperands` method.
  ///           - `offsets` provides the offset of the tile in the coordinate system
  ///             of the original iteration space, i.e., if an iteration space
  ///             dimension had non-zero offset, it must be included in the offset
  ///             provided here (as opposed to zero-based offset "relative" to the
  ///             iteration space).
  ///           - `sizes` provides the size of the tile.
  ///           - `tileDestOperands` specifies whether to also tile `dest` operands
  ///             or not. Avoiding tiling `dest` operands can be useful for
  ///             composition with various looping container ops.
  FailureOr<Value> generateResultTileValue(OpBuilder & b, unsigned resultNumber, ValueRange dest, ArrayRef<OpFoldResult> offsets, ArrayRef<OpFoldResult> sizes, bool tileDestOperands);
};
namespace detail {
  template <typename ConcreteOp>
  struct TilingInterfaceTrait : public ::mlir::OpInterface<TilingInterface, detail::TilingInterfaceInterfaceTraits>::Trait<ConcreteOp> {
  };
}// namespace detail
template<typename ConcreteOp>
SmallVector<Value> detail::TilingInterfaceInterfaceTraits::Model<ConcreteOp>::getDestinationOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getDestinationOperands(b);
}
template<typename ConcreteOp>
SmallVector<StringRef> detail::TilingInterfaceInterfaceTraits::Model<ConcreteOp>::getLoopIteratorTypes(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getLoopIteratorTypes();
}
template<typename ConcreteOp>
SmallVector<Range> detail::TilingInterfaceInterfaceTraits::Model<ConcreteOp>::getIterationDomain(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getIterationDomain(b);
}
template<typename ConcreteOp>
mlir::gml_st::TilingInterface detail::TilingInterfaceInterfaceTraits::Model<ConcreteOp>::getTiledImplementation(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b, ValueRange dest, ArrayRef<OpFoldResult> offsets, ArrayRef<OpFoldResult> sizes, bool  tileDestOperands) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getTiledImplementation(b, dest, offsets, sizes, tileDestOperands);
}
template<typename ConcreteOp>
FailureOr<Value> detail::TilingInterfaceInterfaceTraits::Model<ConcreteOp>::generateResultTileValue(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b, unsigned resultNumber, ValueRange dest, ArrayRef<OpFoldResult> offsets, ArrayRef<OpFoldResult> sizes, bool tileDestOperands) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).generateResultTileValue(b, resultNumber, dest, offsets, sizes, tileDestOperands);
}
template<typename ConcreteOp>
SmallVector<Value> detail::TilingInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getDestinationOperands(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b) {
  return static_cast<const ConcreteOp *>(impl)->getDestinationOperands(tablegen_opaque_val, b);
}
template<typename ConcreteOp>
SmallVector<StringRef> detail::TilingInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getLoopIteratorTypes(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->getLoopIteratorTypes(tablegen_opaque_val);
}
template<typename ConcreteOp>
SmallVector<Range> detail::TilingInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getIterationDomain(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b) {
  return static_cast<const ConcreteOp *>(impl)->getIterationDomain(tablegen_opaque_val, b);
}
template<typename ConcreteOp>
mlir::gml_st::TilingInterface detail::TilingInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getTiledImplementation(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b, ValueRange dest, ArrayRef<OpFoldResult> offsets, ArrayRef<OpFoldResult> sizes, bool  tileDestOperands) {
  return static_cast<const ConcreteOp *>(impl)->getTiledImplementation(tablegen_opaque_val, b, dest, offsets, sizes, tileDestOperands);
}
template<typename ConcreteOp>
FailureOr<Value> detail::TilingInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::generateResultTileValue(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, OpBuilder & b, unsigned resultNumber, ValueRange dest, ArrayRef<OpFoldResult> offsets, ArrayRef<OpFoldResult> sizes, bool tileDestOperands) {
  return static_cast<const ConcreteOp *>(impl)->generateResultTileValue(tablegen_opaque_val, b, resultNumber, dest, offsets, sizes, tileDestOperands);
}
} // namespace gml_st
} // namespace mlir
