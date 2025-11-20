from functions.get_files_info import get_files_info

print(f"Results from current directory: \n{get_files_info("calculator", ".")}")
print(f"Results from 'pkg' directory: \n{get_files_info("calculator", "pkg")}")
print(f"Results from '/bin' directory: \n{get_files_info("calculator", "/bin")}")
print(f"Results from '../' directory: \n{get_files_info("calculator", "../")}")