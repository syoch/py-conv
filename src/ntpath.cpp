#include "../lib/ntpath"

path::path()
{
	/*strings representing various path-related bits and pieces
	* Should beprimarily for export; internally, they are hardcoded.
	* These are set before imports for resolving cyclic dependency. */
	curdir = ".";
	pardir = "..";
	extsep = ".";
	sep = "\\";
	pathsep = ";";
	altsep = "/";
	defpath = ".;C:\\bin";
	devnull = "nul";
}

str path::_get_bothseps(str path)
{
	return "\\/";
}