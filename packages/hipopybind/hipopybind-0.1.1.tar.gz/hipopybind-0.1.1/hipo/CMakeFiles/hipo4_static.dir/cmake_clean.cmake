file(REMOVE_RECURSE
  "libhipo4.a"
  "libhipo4.pdb"
)

# Per-language clean rules from dependency scanning.
foreach(lang CXX)
  include(CMakeFiles/hipo4_static.dir/cmake_clean_${lang}.cmake OPTIONAL)
endforeach()
