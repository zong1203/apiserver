import hashlib

data = 'test'
text = hashlib.sha256(data.encode('utf-8')).hexdigest()
print(text)