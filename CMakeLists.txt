#cmake verson，指定cmake版本 
cmake_minimum_required(VERSION 3.2)

#project name，指定项目的名称，一般和项目的文件夹名称对应
PROJECT(mesh_partition_tool)
if(UNIX AND NOT APPLE)
  # for Linux, BSD, Solaris, Minix
  #head file path，头文件目录
  INCLUDE_DIRECTORIES(
    include
  )
  
  #source directory，源文件目录
  AUX_SOURCE_DIRECTORY(src DIR_SRCS)

  #5.set environment variable，设置环境变量，编译用到的源文件全部都要放到这里，否则编译能够通过，但是执行的时候会出现各种问题，比如"symbol lookup error xxxxx , undefined symbol"
  SET(TEST_MATH
    ${DIR_SRCS}
  )
 
  #6.add executable file，添加要编译的可执行文件
  ADD_EXECUTABLE(${PROJECT_NAME} ${TEST_MATH})
 
  #7.add link library，添加可执行文件所需要的库，比如我们用到了libm.so（命名规则：lib+name+.so），就添加该库的名称
  TARGET_LINK_LIBRARIES(${PROJECT_NAME} m 
  /usr/local/lib 
  boost_regex
  boost_program_options
  boost_filesystem
  boost_system
  boost_thread
  yaml-cpp
  gmp
  mpfr
  )
endif()
if(APPLE)
  #head file path，头文件目录
  INCLUDE_DIRECTORIES(
    include
    /usr/local/include
  )
  
  #source directory，源文件目录
  AUX_SOURCE_DIRECTORY(src DIR_SRCS)

  #5.set environment variable，设置环境变量，编译用到的源文件全部都要放到这里，否则编译能够通过，但是执行的时候会出现各种问题，比如"symbol lookup error xxxxx , undefined symbol"
  SET(TEST_MATH
    ${DIR_SRCS}
  )
  
  #6.add executable file，添加要编译的可执行文件
  ADD_EXECUTABLE(${PROJECT_NAME} ${TEST_MATH})
  
  #7.add link library，添加可执行文件所需要的库，比如我们用到了libm.so（命名规则：lib+name+.so），就添加该库的名称
  TARGET_LINK_LIBRARIES(${PROJECT_NAME} m 
  # /opt/homebrew/Cellar/cgal
  /usr/local/lib/libboost_regex.a 
  /usr/local/lib/libboost_program_options.a
  /usr/local/lib/libboost_filesystem.a
  /usr/local/lib/libboost_system.a
  /usr/local/lib/libboost_thread.a
  /usr/local/lib/libyaml-cpp.a
  # gmp
  # mpfr
  )
endif()

