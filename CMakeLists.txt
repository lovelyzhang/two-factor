cmake_minimum_required(VERSION 3.5.1)
project(2ndfactor VERSION 1.0.0 DESCRIPTION "2nd-Factor Authentication" LANGUAGES C)

set(CMAKE_C_STANDARD 11)


find_path(PAM_INCLUDE_DIR NAMES security/pam_appl.h security/pam_modules.h REQUIRED)
find_library(PAM_LIBRARY pam REQUIRED)
find_package(CURL REQUIRED)


if (PAM_INCLUDE_DIR AND PAM_LIBRARY)
    set(PAM_FOUND TRUE)
endif (PAM_INCLUDE_DIR AND PAM_LIBRARY)

if (PAM_FOUND)
    message(STATUS "Found PAM: ${PAM_LIBRARY}")
else (PAM_FOUND)
    message(FATAL_ERROR "PAM not found")
endif (PAM_FOUND)


if (CURL_FOUND)
    MESSAGE(STATUS "Find curl")
else (CURL_FOUND)
    MESSAGE(FATAL_ERROR "curl not found")
endif (CURL_FOUND)


include_directories(${PAM_INCLUDE_DIR})
include_directories(${CURL_INCLUDE_DIR})

# shared library
add_library(2ndfactor SHARED 2ndfactor.c)
set_target_properties(2ndfactor PROPERTIES
        VERSION ${PROJECT_VERSION}
        SOVERSION 1)
target_link_libraries(2ndfactor curl pam)
