cmake_minimum_required(VERSION 3.8)
project(james_moveit_config)

find_package(ament_cmake REQUIRED)

install(DIRECTORY
  config
  launch
  DESTINATION share/${PROJECT_NAME}
)

install(FILES
  .setup_assistant
  LICENSE-APACHE-2.0
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
