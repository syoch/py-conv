#include "../lib/genericpath"
#include <sys/stat.h>
#include<iostream>

bool _path::exists(Any path)
{
    struct stat st;
    const char* file = std::any_cast<const char*>(path);
    int ret = stat(file, &st);
    if (ret == 0) {
        return true;
    } else {
        return false;
    }
}
