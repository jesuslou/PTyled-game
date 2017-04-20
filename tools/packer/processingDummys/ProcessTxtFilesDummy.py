import sys
import os
import argparse

def message_and_die(message):
	print('\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
	print(message)
	print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
	sys.exit(1)

def read_parameters():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', required=True, help="Path to file to be processed")
	parser.add_argument('-o', '--output', required=True, help="Path to place the modified file")

	args = parser.parse_args()

	return args.file, args.output

def process_file(file_path, output):
	if os.path.isfile(file_path) and file_path.endswith(".txt"):
		with open(file_path, "r") as file:
			lines = file.readlines()

		os.makedirs(os.path.dirname(output), exist_ok=True)
		with open(output, "w+") as file:
			file.write("---- DUMMY LINE BIATCH ----\n")
			for line in lines:
				file.write(line)
	else:
		message_and_die("File {} doesn't exists or is not a txt file!".format(file_path))

if __name__ == '__main__':
	file, output = read_parameters()
	process_file(file, output)