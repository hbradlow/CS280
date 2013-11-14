if(X86)
    add_executable(main main_x86.cpp)
endif(X86)

target_link_libraries(main ${OpenCV_LIBS})
