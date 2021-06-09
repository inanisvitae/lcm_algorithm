import copy


class Lcm():
    def __init__(self):
        pass

    def populate_from_file(self, filename='test.txt'):
        f = open(filename, "r")
        map = dict()
        for line in f.readlines():
            key = line.split('\t')[0]
            values = set()
            for value in line.split('\t')[1].split(','):
                values.add(int(value))
            map[key] = values

        result = dict()
        for key in sorted(map):
            result[key] = map[key]
        return result

    def getTransactionsFromNd(self, nd: dict):
        resultMap = {} # Map of id to items
        for i in nd.keys():
            for j in nd[i]:
                if j in resultMap:
                    resultMap[j].append(i)
                else:
                    resultMap[j] = [i]
        return resultMap


    def lcm(self, nodes: dict, minSup: int):
        nd = copy.deepcopy(nodes)
        for key in nodes.keys():
            if len(nodes[key]) < minSup:
                nd.pop(key, None)
        print(nd)
        allItems = list(nd.keys())
        allItems.sort()
        print(allItems)
        print(self.getTransactionsFromNd(nd))
        self.transactions = self.populate_from_file()
        self.flippedTransactions = self.getTransactionsFromNd(nd)
        print('=====transaction and flipped transactions====')
        print(self.transactions)
        print(self.flippedTransactions)
        self.result = []
        self.minSup = minSup
        self.backtrackingLCM(None, self.flippedTransactions, allItems, -1) # nd isn't a list


        for i in range(len(self.result)):
            self.result[i] = list(set(self.result[i]))
        self.result.sort(key=len, reverse=True)
        return self.result

    def backtrackingLCM(self, p:list, transactionsOfP:dict, frequentItems:list, tailPosInP:int):
        # ========  for each frequent item  e  =============
        for j in range(len(frequentItems)):
            e = frequentItems[j]
            if p and e in p:
                continue
            # transactionsPe = transactionsOfP[e] # [] = {{}}[]
            transactionsPe = self.intersectTransactions(transactionsOfP, e)

            # ====== Check if PU{e...} is a ppc extension  ======
            if self.isPPCExtension(p, transactionsPe, e):
                itemset = []
                if p:
                    for m in p: # Simplication made
                        itemset.append(m)
                itemset.append(e)
                itemset.sort()
                tailPositionInPe = len(itemset) - 1

                for k in range(j + 1, len(frequentItems)):
                    itemk = frequentItems[k]
                    if self.isItemInAllTransactions(transactionsPe, itemk):
                        itemset.append(itemk)
                itemset.sort()

                # finish here
                # print('Closed Item Set is: ')
                # print(itemset)
                self.result.append(itemset)
                # Performs database reduction
                self.anyTimeDatabaseReductionClosed(transactionsPe, j, frequentItems, p, e)

                newFrequentItems = []
                for k in range(j + 1, len(frequentItems)):
                    itemK = frequentItems[k]
                    if len(self.transactions[itemK]) >= self.minSup:
                        newFrequentItems.append(itemK)

                self.backtrackingLCM(itemset, transactionsPe, newFrequentItems, tailPositionInPe)

        return None

    def isPPCExtension(self, p:list, transactionsPe: list, e):
        firstTrans = transactionsPe[0]
        firstTransaction = self.flippedTransactions[firstTrans]
        for item in firstTransaction:
            if item < e and ((not p) or (item not in p)) and self.isItemInAllTransactionsExceptFirst(transactionsPe, item):
                return False
        return True

    def isItemInAllTransactions(self, transactions:list, item):
        for i in transactions:
            if item not in self.flippedTransactions[i]:
                return False
        return True

    def anyTimeDatabaseReductionClosed(self, transactionsPe, j, frequentItems, p, e):
        for i in range(j + 1, len(frequentItems)):
            item = frequentItems[i]
            self.transactions[item] = []

        for t in transactionsPe:
            for i in range(len(self.flippedTransactions[t])-1, 0, -1):
                item = self.flippedTransactions[t][i]
                if item > e and item in frequentItems:
                    self.transactions[item].append(t)


    def isItemInAllTransactionsExceptFirst(self, transactions, item):
        for i in range(1, len(transactions)):
            if item not in self.flippedTransactions[transactions[i]]:
                return False
        return True

    def intersectTransactions(self, transactionsOfP, e):
        transactionsPe = []

        for i in transactionsOfP:
            if e in self.flippedTransactions[i]:
                transactionsPe.append(i)
        transactionsPe.sort()
        return transactionsPe