cmake_minimum_required(VERSION 3.20)

project(MyCProject LANGUAGES C CXX)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

include(FetchContent)

FetchContent_Declare(
    webview
    GIT_REPOSITORY https://github.com/webview/webview.git
    GIT_TAG 0.12.0
)

FetchContent_MakeAvailable(webview)

add_executable(app
    main.c
    typing.h

    input_f/sets_input.c
    input_f/expression_input.c
    input_f/basis_input.c
    input_f/total_input.c

    core/normal_form.c

    string_process/string_process.c

    gui/gui.c
)

target_include_directories(app PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/input_f
    ${CMAKE_CURRENT_SOURCE_DIR}/string_process
    ${CMAKE_CURRENT_SOURCE_DIR}/core
    ${CMAKE_CURRENT_SOURCE_DIR}/gui
)

target_link_libraries(app PRIVATE
    webview::core_static
)

set_target_properties(app PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}
    LINKER_LANGUAGE CXX
)

if(MSVC)
    target_compile_options(app PRIVATE /W4)
else()
    target_compile_options(app PRIVATE -Wall -Wextra -Wpedantic)
endif()
