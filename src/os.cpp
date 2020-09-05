#include <direct.h>
#include <sys/stat.h>
#include <stdio.h>
#include <iostream>
#include "../lib/os"

void os::mkdir(Any name, bool exist_ok = false)
{
	const char* dir = std::any_cast<const char*>(name);
	struct stat statBuf;
	int result = 1;
	if (stat(dir, &statBuf) != 0) {
		result = _mkdir(dir);
	} else if (exist_ok == true && stat(dir, &statBuf) == 0) {
		result = _mkdir(dir);
	}
	if (result == 1) {
		throw OSError("Cannot rely on checking for EEXIST, since the operating system could give priority to other errors like EACCES or EROFS");
	}
}

void os::rmdir(Any name)
{
	int result = _rmdir(std::any_cast<const char*>(name));
	if (result == 1) {
		throw;
	}
}

void os::renames(Any old, Any _new)
{
	os os;
	struct stat statBuf;
	if (stat(std::any_cast<const char*>(old), &statBuf) != 0) {
		os.mkdir(_new);
	} else {
		if (rename(std::any_cast<const char*>(old), std::any_cast<const char*>(_new)) != 0) {
			return;
		}
	}
	os.rmdir(old);
}