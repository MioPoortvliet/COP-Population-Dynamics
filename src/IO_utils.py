"""
Helper functions for input/output.
Authors: Mio Poortvliet, Jonah Post
"""
import numpy as np
import os
import json
import shutil
import unicodedata
import re


def ensure_dir(file_path: str) -> None:
	"""Makes sure dir exists."""
	if not os.path.exists(file_path):
		os.makedirs(file_path)


def del_dir(path: str) -> None:
	"""
	REMOVES SPECIFIED DIR!
	:param path: dir to be removed
	:type path: str
	:return: None
	:rtype: None
	"""
	print(f"Removing {path}.")
	shutil.rmtree(path)


def load_and_concat(fpath: str, file_identifier:str) -> np.ndarray:
	"""
	Load files in filepath that contain file_identifier in order, then concatenate them to one large array.
	:param fpath: filepath of dir containing files
	:type fpath: str
	:param file_identifier: identifier of specific files
	:type file_identifier: str
	:return: array of loaded files
	:rtype: np.ndarray
	"""
	arrays = []
	files = [f for f in os.listdir(fpath) if f[:len(file_identifier)] == file_identifier]
	file_numbers = np.array([int(f.replace(file_identifier, '').replace('-', '').replace('.npy', '')) for f in files])
	files = [files[i] for i in file_numbers.argsort()]

	for file in files:
		arrays.append(np.load(fpath+file, allow_pickle=True))

	return np.concatenate(arrays)


def load_json(fpath: str, fname="00-header.json") -> dict:
	"""
	Loads a json file from fpath with fname
	:param fpath: path to dir where file is located
	:type fpath: str
	:param fname: filename of json file
	:type fname: str
	:return: contents of json file as a nestled dict
	:rtype: dict
	"""
	with open(fpath+fname) as json_file:
		data = json.load(json_file)

	return data


def to_file(fpath: str, data: object) -> None:
	"""
	Save data to file in fpath
	:param fpath: filepath of file to be written
	:type fpath: str
	:param data: data to be saved
	:type data: object
	:return: None
	:rtype: None
	"""
	with open(fpath + ".npy", 'wb') as file:
		np.save(file, data)



def cleanup_paths(paths):
	"""Deletes dirs in the list paths."""
	for path in paths:
		del_dir(path)


def slugify(value, allow_unicode=False):
	"""
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
	value = str(value)
	if allow_unicode:
		value = unicodedata.normalize('NFKC', value)
	else:
		value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
	value = re.sub(r'[^\w\s-]', '', value.lower())
	return re.sub(r'[-\s]+', '-', value).strip('-_')


def to_json(fpath, dict_to_write) -> None:
	"""
	This function writes all used parameters to a header file '00-header.json' in the output dir.
	:return: None
	:rtype: None
	"""
	#for key in dict_to_write.keys():
	#	dict_to_write[key] = float(dict_to_write[key])

	with open(fpath, "w") as file:
		json.dump(dict_to_write, file)