#include "../lib/genericpath"
#include <sys/stat.h>
#include <iostream>

bool path::exists(Any path)
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

bool path::isdir(Any path)
{
    struct stat st;
    int result;
    result = stat(std::any_cast<const char*>(path), &st);
    if (result != 0) {
        return false;
    } else if ((st.st_mode & S_IFMT) == S_IFDIR) {
        return true;
    } else {
        return false;
    }
}

bool path::isfile(Any path)
{
    struct stat st;
    int result;
    result = stat(std::any_cast<const char*>(path), &st);
    if (result != 0) {
        return false;
    } else if ((st.st_mode & S_IFMT) != S_IFDIR) {
        return true;
    } else {
        return false;
    }
}
