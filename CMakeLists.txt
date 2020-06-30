cmake_minimum_required(VERSION 2.8.3)
project(talos_bauzil)

find_package(catkin REQUIRED)

catkin_package()

FOREACH(dir launch models rviz src urdf worlds scripts)
  INSTALL(DIRECTORY ${dir}
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
ENDFOREACH(dir)
