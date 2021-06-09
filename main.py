from src.lcm_algorithm import Lcm
import time
start_time = time.time()
c = Lcm()
map = c.populate_from_file(filename='test.txt')
test = c.lcm(map, 3)
print(test)
result = {}
for i in test:
    result[':'.join(i)] = []
print("--- %s seconds ---" % (time.time() - start_time))
f = open("result.txt", "a")
for key in result.keys():
    f.write(key + '\t' + ' '.join([str(elem) for elem in result[key]]) + '\n')
f.close()
