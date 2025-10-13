project(parallel-bfs)

CMAKE_MINIMUM_REQUIRED(VERSION 3.20)

set(CMAKE_CXX_STANDARD 20)

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    add_compile_options(-fsanitize=thread)
    add_link_options(-fsanitize=thread)
endif()

add_executable(${PROJECT_NAME}
    main.cpp
    RandomGraphGenerator.cpp
    Graph.cpp
)
