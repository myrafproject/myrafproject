from myraflib import FitsArray

fa = FitsArray.from_pattern("PATTERN/OF/FILES/*.fits")
fa.hedit(
    ["Ke1y", "Key2"], ["Value1", "Value2"], ["Comment1", "Comment2"]
)

aligned_fa = fa.align(reference=0)

