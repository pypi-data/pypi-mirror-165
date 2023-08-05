file(REMOVE_RECURSE
  "libhipo4.dylib"
  "libhipo4.pdb"
)

# Per-language clean rules from dependency scanning.
foreach(lang CXX)
  include(CMakeFiles/hipo4.dir/cmake_clean_${lang}.cmake OPTIONAL)
endforeach()
