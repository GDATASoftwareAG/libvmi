target_sources(vmi PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/bareflank.c
    ${CMAKE_CURRENT_SOURCE_DIR}/hypercall.S
)
