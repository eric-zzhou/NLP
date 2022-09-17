import re
regex = re.compile('\d+')
t = "10 Hello NewYork.   Weather is awesome 002"
print(regex.findall(t))

regex = re.compile('\D+')
print(regex.findall(t))

regex = re.compile('\w+')
print(regex.findall(t))

regex = re.compile('[a-zA-Z]+')
print(regex.findall(t))

print(re.findall(r'Weath?er', t))
