cmake_minimum_required(VERSION 3.16)
project(MyApp)

set(CMAKE_CXX_STANDARD 17)

# Вкажи шлях до встановленого wxWidgets
set(wxWidgets_ROOT_DIR "C:/wxWidgets-3.3.1/build_msvc/install")
set(wxWidgets_LIB_DIR "C:/wxWidgets-3.3.1/build_msvc/install/lib")

# Знайди бібліотеки
find_package(wxWidgets REQUIRED COMPONENTS core base)

include(${wxWidgets_USE_FILE})

add_executable(MyApp main.cpp)
target_link_libraries(MyApp ${wxWidgets_LIBRARIES})