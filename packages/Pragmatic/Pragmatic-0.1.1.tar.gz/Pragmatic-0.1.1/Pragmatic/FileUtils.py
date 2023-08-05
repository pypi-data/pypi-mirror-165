import sys
import hashlib
import os


def hash_file(file_path: str) -> str:
	BLOCK_SIZE = 65536
	hasher = hashlib.sha1()
	with open(file_path, 'rb') as file_handle:
		buf = file_handle.read(BLOCK_SIZE)
		while len(buf) > 0:
			hasher.update(buf)
			buf = file_handle.read(BLOCK_SIZE)
	return hasher.hexdigest()

def hash_str(str: str) -> str:
	hasher = hashlib.sha1()
	hasher.update(str.encode('utf-8'))
	return hasher.hexdigest()

def GetDataDir():
	dir = os.path.dirname(os.path.realpath(__file__))
	return os.path.join(dir, 'data')
