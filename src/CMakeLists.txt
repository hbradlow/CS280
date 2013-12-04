if(X86)
    add_executable(main main_x86.cpp)
    target_link_libraries(main ${OpenCV_LIBS} ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})

	add_library(main_py SHARED main_x86.cpp)
    set_target_properties(main_py PROPERTIES SUFFIX ".so")
    set_target_properties(main_py PROPERTIES 
        LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/python)
    target_link_libraries(main_py ${OpenCV_LIBS} ${Boost_LIBRARIES} 
                            ${PYTHON_LIBRARIES})
endif(X86)

if(PI)
    include_directories(/opt/vc/include)

    include_directories(/home/pi/Desktop/Work/userland/interface/vcos)
    include_directories(/home/pi/Desktop/Work/userland)
    include_directories(/home/pi/Desktop/Work/userland/interface/vcos/pthreads)
    include_directories(/home/pi/Desktop/Work/userland/interface/vmcs_host/linux)
    include_directories(/home/pi/Desktop/Work/userland/host_applications/linux/libs/bcm_host/include)
    link_directories(/opt/vc/lib)

    add_library(picam picam/picam.cpp picam/camera.cpp picam/cameracontrol.cpp
                            picam/graphics.cpp)
    target_link_libraries(picam libmmal_core.so libmmal_util.so 
                            libmmal_vc_client.so libvcos.so libbcm_host.so
                            GLESv2 EGL ${OpenCV_LIBS})

	add_executable(main main_pi.cpp)
    target_link_libraries(main libmmal_core.so libmmal_util.so 
                            libmmal_vc_client.so libvcos.so 
                            libbcm_host.so GLESv2 EGL ${OpenCV_LIBS}
                            picam ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})

	add_library(main_py SHARED main_pi.cpp)
    set_target_properties(main_py PROPERTIES 
        LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/python)
	target_link_libraries(main_py libmmal_core.so libmmal_util.so
                            libmmal_vc_client.so libvcos.so
                            libbcm_host.so GLESv2 EGL ${OpenCV_LIBS}
                            picam ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})
endif(PI)
