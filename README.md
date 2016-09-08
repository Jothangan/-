1.各种模块的编译方式的定义文件
文件名                  说明
host_static_library.mk  定义了如何编译主机上的静态库。
host_shared_library.mk  定义了如何编译主机上的共享库。
static_library.mk       定义了如何编译设备上的静态库。
shared_library.mk       定义了如何编译设备上的共享库。
executable.mk           定义了如何编译设备上的可执行文件。
host_executable.mk      定义了如何编译主机上的可执行文件。
package.mk              定义了如何编译 APK 文件。
prebuilt.mk             定义了如何处理一个已经编译好的文件 ( 例如 Jar 包 )。
multi_prebuilt.mk       定义了如何处理一个或多个已编译文件，该文件的实现依赖 prebuilt.mk。
host_prebuilt.mk        处理一个或多个主机上使用的已编译文件，该文件的实现依赖 multi_prebuilt.mk。
java_library.mk         定义了如何编译设备上的共享 Java 库。
static_java_library.mk  定义了如何编译设备上的静态 Java 库。
host_java_library.mk    定义了如何编译主机上的共享 Java 库。
