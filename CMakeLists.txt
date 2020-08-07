cmake_minimum_required(VERSION 2.8.3)
project(talos_bauzil)

find_package(catkin REQUIRED)

catkin_package()

catkin_install_python(PROGRAMS 
                      src/odometry.py
                      src/publisher_world.py
                      src/odom_sot.py
                      DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

FOREACH(dir launch models rviz src urdf worlds scripts)
  INSTALL(DIRECTORY ${dir}
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
ENDFOREACH(dir)
