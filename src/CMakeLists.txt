if(X86)
    add_executable(main main_x86.cpp)
    target_link_libraries(main ${OpenCV_LIBS} ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})
endif(X86)

if(PI)
    include_directories(/opt/vc/include)

    include_directories(/home/pi/Desktop/Work/userland/interface/vcos)
    include_directories(/home/pi/Desktop/Work/userland)
    include_directories(/home/pi/Desktop/Work/userland/interface/vcos/pthreads)
    include_directories(/home/pi/Desktop/Work/userland/interface/vmcs_host/linux)
    include_directories(/home/pi/Desktop/Work/userland/host_applications/linux/libs/bcm_host/include)
    link_directories(/opt/vc/lib)

    add_library(picam picam/picam.cpp picam/camera.cpp picam/cameracontrol.cpp picam/graphics.cpp)
    target_link_libraries(picam libmmal_core.so libmmal_util.so libmmal_vc_client.so libvcos.so libbcm_host.so GLESv2 EGL ${OpenCV_LIBS})

	add_executable(main main_pi.cpp)
	add_library(main_pi SHARED main_pi.cpp)
	target_link_libraries(main_pi libmmal_core.so libmmal_util.so libmmal_vc_client.so libvcos.so libbcm_host.so GLESv2 EGL ${OpenCV_LIBS} picam ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})
    target_link_libraries(main libmmal_core.so libmmal_util.so libmmal_vc_client.so libvcos.so libbcm_host.so GLESv2 EGL ${OpenCV_LIBS} picam ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})
endif(PI)

