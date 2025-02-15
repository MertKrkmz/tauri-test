# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/emre/denemeler/tauri-test

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/emre/denemeler/tauri-test/build

# Include any dependencies generated for this target.
include CMakeFiles/color_converter.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/color_converter.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/color_converter.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/color_converter.dir/flags.make

CMakeFiles/color_converter.dir/src/color/ColorConverter.cpp.o: CMakeFiles/color_converter.dir/flags.make
CMakeFiles/color_converter.dir/src/color/ColorConverter.cpp.o: ../src/color/ColorConverter.cpp
CMakeFiles/color_converter.dir/src/color/ColorConverter.cpp.o: CMakeFiles/color_converter.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/emre/denemeler/tauri-test/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/color_converter.dir/src/color/ColorConverter.cpp.o"
	/usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/color_converter.dir/src/color/ColorConverter.cpp.o -MF CMakeFiles/color_converter.dir/src/color/ColorConverter.cpp.o.d -o CMakeFiles/color_converter.dir/src/color/ColorConverter.cpp.o -c /home/emre/denemeler/tauri-test/src/color/ColorConverter.cpp

CMakeFiles/color_converter.dir/src/color/ColorConverter.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/color_converter.dir/src/color/ColorConverter.cpp.i"
	/usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/emre/denemeler/tauri-test/src/color/ColorConverter.cpp > CMakeFiles/color_converter.dir/src/color/ColorConverter.cpp.i

CMakeFiles/color_converter.dir/src/color/ColorConverter.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/color_converter.dir/src/color/ColorConverter.cpp.s"
	/usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/emre/denemeler/tauri-test/src/color/ColorConverter.cpp -o CMakeFiles/color_converter.dir/src/color/ColorConverter.cpp.s

# Object files for target color_converter
color_converter_OBJECTS = \
"CMakeFiles/color_converter.dir/src/color/ColorConverter.cpp.o"

# External object files for target color_converter
color_converter_EXTERNAL_OBJECTS =

libcolor_converter.a: CMakeFiles/color_converter.dir/src/color/ColorConverter.cpp.o
libcolor_converter.a: CMakeFiles/color_converter.dir/build.make
libcolor_converter.a: CMakeFiles/color_converter.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/emre/denemeler/tauri-test/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX static library libcolor_converter.a"
	$(CMAKE_COMMAND) -P CMakeFiles/color_converter.dir/cmake_clean_target.cmake
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/color_converter.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/color_converter.dir/build: libcolor_converter.a
.PHONY : CMakeFiles/color_converter.dir/build

CMakeFiles/color_converter.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/color_converter.dir/cmake_clean.cmake
.PHONY : CMakeFiles/color_converter.dir/clean

CMakeFiles/color_converter.dir/depend:
	cd /home/emre/denemeler/tauri-test/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/emre/denemeler/tauri-test /home/emre/denemeler/tauri-test /home/emre/denemeler/tauri-test/build /home/emre/denemeler/tauri-test/build /home/emre/denemeler/tauri-test/build/CMakeFiles/color_converter.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/color_converter.dir/depend

