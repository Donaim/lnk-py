This program is somewhat simmilar to usual file-system links.  
Each copy holds information about target file.  
But main differences are:
- lnk.py files store alternative paths to target
- if target file is not on disk, lnk.py downloads it from web paths
- lnk.py supports intermediate installators. so f.e if file does not exist on disk, lnk.py downloads its installator, and runs it

# Build
Because lnk.py file has to be a **single** file, building such file needs to be splitted, otherwise code will be really messy.  
For that purpos there is pyincluder.py

# To do
- [ ] git versioning
- [ ] installers
- [X] target argumets flags (like windows/linux)
- [ ] script arguments parsing (f.e. "$lnk-py:path" if only want to get path printed on stdout, or additionally download if not present)