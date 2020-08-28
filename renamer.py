from directories import Directory

working_dir = input("Enter a directory: ")
print("Now, wait a bit...")
Directory(working_dir).rename_dir()

print("Done!")