#include "../lib/platform/file"

#include <stdio.h>
#include <iostream>
#include "../lib/os"

void os::mkdir(Any name, bool exist_ok = false)
{
	const char* dir = std::any_cast<const char*>(name);
	struct stat statBuf;
	int result = 1;
	if (stat(dir, &statBuf) != 0) {
		result = platform::mkdir(dir);
	} else if (exist_ok == true && stat(dir, &statBuf) == 0) {
		result = platform::mkdir(dir);
	}
	if (result == 1) {
		throw OSError("Cannot rely on checking for EEXIST, since the operating system could give priority to other errors like EACCES or EROFS");
	}
}

void os::rmdir(Any name)
{
	int result = platform::rmdir(name.toString());
	if (result == 1) {
		throw;
	}
}

void os::renames(Any _old, Any __new)
{
	const char* old=_old.toString();
	const char* _new=__new.toString();
	os os;
	if (!platform::exist(old)) {
		platform::mkdir(_new);
	} else {
		if (platform::rename(old,_new) != 0) {
			return;
		}
	}
	os.rmdir(old);
}