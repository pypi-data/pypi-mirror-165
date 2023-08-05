#----------------------------------------------------------------
# Generated CMake target import file for configuration "RELEASE".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "hipo4" for configuration "RELEASE"
set_property(TARGET hipo4 APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(hipo4 PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libhipo4.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libhipo4.dylib"
  )

list(APPEND _IMPORT_CHECK_TARGETS hipo4 )
list(APPEND _IMPORT_CHECK_FILES_FOR_hipo4 "${_IMPORT_PREFIX}/lib/libhipo4.dylib" )

# Import target "hipo4_static" for configuration "RELEASE"
set_property(TARGET hipo4_static APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(hipo4_static PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libhipo4.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS hipo4_static )
list(APPEND _IMPORT_CHECK_FILES_FOR_hipo4_static "${_IMPORT_PREFIX}/lib/libhipo4.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
