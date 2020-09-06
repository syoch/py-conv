#include "../lib/genericpath"
#include <sys/stat.h>
#include <iostream>
#include <vector>
#include <sstream>
//#include <regex>

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

#ifdef DEBUG
std::vector<std::string> ssplit(const std::string& s, char delim)
{
	std::vector<std::string> elems;
	std::stringstream ss(s);
	std::string item;
	while (getline(ss, item, delim)) {
		if (!item.empty()) {
			elems.push_back(item);
		}
	}
	return elems;
}
std::vector<std::string> path::split(Any path)
{
	std::regex re("\\");
	std::string _path = std::regex_replace(std::any_cast<std::string>(path), re, "/");
	std::string dir;
	std::string file;
	std::vector<std::string> in_path = ssplit(_path, '/');
	std::vector<std::string> out_path;
	for (std::string i : in_path) {
		if (i.find(".") != std::string::npos) {
			file = i;
		} else {
			dir += i + "/";
		}
	}
	out_path.push_back(dir);
	out_path.push_back(file);
	return std::vector<std::string>(out_path);
}
#endif // DEBUG