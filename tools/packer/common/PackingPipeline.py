import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from time import sleep
from appdirs import user_data_dir

def message_and_die(message):
	print('\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
	print(message)
	print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
	sys.exit(1)

def read_parameters():
	parser = argparse.ArgumentParser()
	parser.add_argument('-pf', '--packs_file', required=True, help='Path to packs definitions')

	args = parser.parse_args()

	return args.packs_file

class PackGenerator:
	def __init__(self, packs_file_path):
		self.packs_file_path = Path(packs_file_path)

		if self.packs_file_path.is_file() == False:
			message_and_die("{} doesn't exists!".format(self.packs_file_path))

		with open(self.packs_file_path.absolute()._str) as packs_file:
			self.packs_info = json.load(packs_file)

		# resources root path. Root of ALL game resources
		self.res_root_path = self.__get_config_path(Path(self.packs_info["resourcesRootPath"]))
		print("-- res_root path path set to {}".format(self.res_root_path))

		self.res_output_path = self.__get_config_path(Path(self.packs_info["outputDestinationPath"]))
		print("-- res_output path set to {}".format(self.res_output_path))

		user_data_dir_path = user_data_dir(self.res_root_path.parts[-2], "LouEngine")

		# Intermediate folder to store processed files
		self.res_build_path = Path(user_data_dir_path)
		self.res_build_path /= "build"
		self.res_build_path.mkdir(parents=True, exist_ok=True)
		print("-- res_build_path path set to {}".format(self.res_build_path))

		# Timestamp files to check modified files since last execution
		self.res_cache_path = Path(user_data_dir_path)
		self.res_cache_path /= "cache"
		self.res_cache_path.mkdir(parents=True, exist_ok=True)
		print("-- res_cache_path path set to {}".format(self.res_cache_path))

		self.files_needing_new_cache_file = []

		self.__generate_pack_definitions()
		#self.__generate_packs()

		self.__update_cache_files()


	def __get_config_path(self, res_path):
		if res_path.is_absolute():
			return res_path
		else:
			return Path(self.__get_relative_to_absolute(res_path, self.packs_file_path))


	def __get_relative_to_absolute(self, relative, absolute):
		final_path = absolute.parent.joinpath(relative)
		if not final_path.exists():
			final_path.mkdir(parents=True, exist_ok=True)
		return final_path.resolve()


	def __generate_pack_definitions(self):
		print("\n-- Current packs version is {}\n".format(self.packs_info["version"]))
		self.pack_definitions = {"version":self.packs_info["version"], "packs":[]}
		for pack_definition in self.packs_info["packs"]:
			if self.__any_file_modified(pack_definition):
				self.current_pack_definition = {}
				self.__generate_pack_definition(pack_definition)
				self.pack_definitions["packs"].append(self.current_pack_definition)
			else:
				print("-- Skipping. Nothing modified in pack '{}'.".format(pack_definition["packName"]))

		if len(self.pack_definitions["packs"]) > 0:
			final_pack_def_file_path = Path(self.res_cache_path)
			final_pack_def_file_path /= "pack_defs.json"
			with open(str(final_pack_def_file_path), "w+") as file:
				json.dump(self.pack_definitions, file, indent=4)


	def __any_file_modified(self, pack_definition):
		any_modified = False
		for path in pack_definition["sourcePaths"]:
			root_path = self.res_root_path / path["path"]
			data_modified = self.__check_modified_files(root_path, self.packs_info["dataPackFileTypes"])
			res_modified = self.__check_modified_files(root_path, self.packs_info["resourcePackFileTypes"])
			any_modified = data_modified or res_modified
		return any_modified


	def __check_modified_files(self, root_path, pack_file_types):
		any_modified = False
		for pack_file_type in pack_file_types:
			files_by_extension = list(root_path.glob("**/*.{}".format(pack_file_type["extension"])))
			if len(files_by_extension) > 0:
				any_modified = self.__check_files_timestamp(files_by_extension, self.res_root_path) or any_modified
		return any_modified


	def __check_files_timestamp(self, files, root):
		any_modified = False
		for file in files:
			relative = file.relative_to(self.res_root_path)
			src_file = root / relative
			cache_file = Path(self.res_cache_path / relative).with_suffix(".txt")
			if not cache_file.exists() or os.path.getmtime(str(src_file)) > os.path.getmtime(str(cache_file)):
				self.files_needing_new_cache_file.append(relative)
				any_modified = True
		return any_modified


	def __generate_pack_definition(self, pack_definition):
		self.current_pack_definition = {"packName":pack_definition["packName"], "separatedPacks":pack_definition["separatedPacks"]}
		print("-- Processing pack: {}".format(pack_definition["packName"]))
		print("- separatedPacks: {}".format(pack_definition["separatedPacks"]))

		for path in pack_definition["sourcePaths"]:
			try:
				# Pack content paths should be relative to res_root_path
				root_path = self.res_root_path / path["path"]
				self.__add_files(root_path)
			except FileNotFoundError as err:
				message_and_die("Error while gathering pack folders! {}".format(err))
		print("\n")


	def __add_files(self, root_path):
		self.__add_pak_specific_files(root_path, self.packs_info["dataPackFileTypes"], "dataFiles")
		self.__add_pak_specific_files(root_path, self.packs_info["resourcePackFileTypes"], "resourceFiles")


	def __add_pak_specific_files(self, root_path, pack_file_types, pack_files_name):
		self.current_pack_definition[pack_files_name] = []
		current_pack_definition_paths = []
		for pack_file_type in pack_file_types:
			tmp_data_files = list(root_path.glob("**/*.{}".format(pack_file_type["extension"])))
			if("rule" in pack_file_type and len(pack_file_type["rule"]) > 0 and len(tmp_data_files) > 0):
				for i in range(len(tmp_data_files)):
					tmp_data_files[i] = self.__process_rule(pack_file_type["rule"], tmp_data_files[i])
			current_pack_definition_paths.extend(tmp_data_files)
		for path in current_pack_definition_paths:
			# strings, because of the json serialization
			self.current_pack_definition[pack_files_name].append(str(path.absolute()))
			print("\t- Added {}".format(str(path.absolute())))


	def __process_rule(self, rule_params, file_path):
		tmp_rule_params = list(rule_params)
		intermediate_folder = file_path
		for i in range(len(tmp_rule_params)):
			if tmp_rule_params[i] == "##IN_FILE_PATH##":
				tmp_rule_params[i] = str(file_path.absolute())
			elif tmp_rule_params[i] == "##OUT_FILE_PATH##":
				intermediate_folder = self.res_build_path / self.__get_relative_res_folder(file_path)
				tmp_rule_params[i] = str(intermediate_folder.absolute())

		if self.__has_file_been_modified(self.__get_relative_res_folder(file_path)):
			if subprocess.call(" ".join(tmp_rule_params), shell=True, cwd=r"{}".format(str(self.packs_file_path.parent.absolute()))) != 0:
				message_and_die('CMake executable "cmake" not in your path')

		return intermediate_folder


	def __get_relative_res_folder(self, path):
		return path.relative_to(self.res_root_path)


	def __has_file_been_modified(self, path):
		for file in self.files_needing_new_cache_file:
			if file == path:
				return True
		return False


	def __update_cache_files(self):
		print("\n")
		for file in self.files_needing_new_cache_file:
			cache_file_path = self.res_cache_path / file
			print("- Creating cache file for {}".format(str(cache_file_path)))
			cache_file_path = cache_file_path.with_suffix(".txt")
			cache_file_path.parent.mkdir(parents=True, exist_ok=True)
			cache_file_path.touch(exist_ok=True)
			cache_file_path.write_text(str(os.path.getmtime(str(cache_file_path))))


if __name__ == '__main__':
	packs_file = read_parameters()
	packGenerator = PackGenerator(packs_file)

	#cd C:\my_projects\PTyledGame\tools\packer\common
	#python PackingPipeline.py -pf C:\my_projects\PTyledGame\res\packerTool\packsDefinition.json