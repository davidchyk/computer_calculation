cmake_minimum_required(VERSION 3.10 FATAL_ERROR)
project(MyCProject C)

# Встановлюємо директорію для виконуваних файлів в поточну директорію
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

# Додаємо виконувану ціль
add_executable(app
    main.c
)

# Вказуємо директорії включення для цієї виконуваної цілі
target_include_directories(app PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)