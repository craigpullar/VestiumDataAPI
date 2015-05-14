from hashlib import md5

def slugGenerator(id):
	return md5(image_path).digest().encode('base64')

def generate_file_path(slug):
	l = [1,4,7,10]
	base = 'user_images/profile_images/'
	j  =0
	for i in l:
		c = slug[j:i]
		j = i
		base +=  (c + '/')
	return base
