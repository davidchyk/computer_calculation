cmake_minimum_required(VERSION 3.16)
project(KarnaughMap)

set(CMAKE_CXX_STANDARD 17)

find_package(Qt6 REQUIRED COMPONENTS Widgets)
qt_wrap_ui(UI_HEADERS)
qt_wrap_cpp(MOC_SOURCES)

add_executable(KarnaughMap main.cpp)
target_link_libraries(KarnaughMap Qt6::Widgets)