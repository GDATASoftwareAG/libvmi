import os

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
from conan.tools.files import collect_libs, rm, rmdir
from conan.tools.files.symlinks import absolute_to_relative_symlinks


class Libvmi(ConanFile):
    name = "libvmi"
    version = "0.1"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    exports_sources = "CMakeLists.txt", "libvmi.pc.in", "cmake/*", "libvmi/*", "doc/*", "examples/*", "tools/*"

    def requirements(self):
        self.requires("glib/2.76.3")
        self.requires("json-c/0.16")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["BUILD_EXAMPLES"] = False
        tc.cache_variables["ENABLE_STATIC"] = not self.options.shared
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))
        rm(self, "libvmi.la", os.path.join(self.package_folder, "lib"))
        if self.options.shared:
            absolute_to_relative_symlinks(self, self.package_folder)
        else:
            rm(self, "libvmi.so*", os.path.join(self.package_folder, "lib"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "libvmi")
        self.cpp_info.set_property("pkg_config_name", "libvmi")
        self.cpp_info.libs = collect_libs(self)
        # self.cpp_info.components["libvmi"].libs.append("glib::glib")
        # self.cpp_info.components["libvmi"].libs.append("json-c::json-c")
