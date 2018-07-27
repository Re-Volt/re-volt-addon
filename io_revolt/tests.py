import os
import rvstruct
import shutil

rvgl_dir = "/mnt/Kalahari/RVGL"

if os.path.isdir("tests"):
	shutil.rmtree("tests")

os.makedirs("tests")

# read .rim
test_path = os.path.join(rvgl_dir, "levels/muse1/muse1.rim")
print("Reading", test_path)

with open(test_path, "rb") as f:
	try:
		rim = rvstruct.RIM(f)
	except Exception as e:
		print("That did not work:\n",e)

	print("Mirror planes:", rim.num_mirror_planes)


# write rim
test_path = "tests/test.rim"
print("writing", test_path)

with open(test_path, "wb") as f:
	try:
		rim.write(f)
	except Exception as e:
		print("That did not work:\n",e)