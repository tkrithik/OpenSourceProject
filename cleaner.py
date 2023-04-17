import shutil
import os
def clean():
  dir_path = r"Images"
  path = "Images"
  shutil.rmtree(dir_path, ignore_errors=False)
  print("Deleted '%s' directory successfully" % dir_path)
  isExist = os.path.exists(path)
  if not isExist:
    # Create a new directory because it does not exist
    os.makedirs(path)
    print("The new directory is created!")
  if os.path.exists("face_enc"):
    os.remove("face_enc")
  else:
    print("The file does not exist")


if __name__ == "__main__":
  clean()
