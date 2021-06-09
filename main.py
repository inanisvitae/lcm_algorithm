from src.lcm_algorithm import Lcm

c = Lcm()
map = c.populate_from_file(filename='test.txt')
test = c.lcm(map, 1)

f = open("result.txt", "a")
for key in test.keys():
    f.write(key + '\t' + ' '.join([str(elem) for elem in test[key]]) + '\n')
f.close()
