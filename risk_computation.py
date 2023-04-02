import math
import multiprocessing as ml
import random
from itertools import combinations
import pickle
from operator import itemgetter

#at user level, we select h, the length of the background knowledge (given the total number of
# points of that user).
#given h, we select the actual points over the dataset of the user, there could be holes
#we only respect the partial order among the points

class RiskEvaluation:

    def __init__(self, complete_dataset, dataset, data):
        #complete dataset has users identifiers as keys and users' locations as values (a list)
        self.complete_dataset = complete_dataset
        #dataset is the actual data for this distributed process
        self.dataset = dataset
        self.users = list()
        for user in self.dataset.keys():
            self.users.append(user)
        #it helps handling the workers, every time a worker is born we add it to the list
        #we remove it when it finishes
        self.processes = list()
        self.results = dict()
        self.data = data

    #workers is the number of workers available to parallelize the code
    def master(self, workers):
        #it splits the work among workers
        #each worker has a sub set of users to handle

        #split the work among workers
        total = len(self.dataset.keys())

        items_for_worker = math.ceil(total/float(workers))
        start = 0
        end = int(items_for_worker)

        #create workers
        print("Dispatching jobs to workers...\n")
        for i in range(0, workers):
            process = ml.Process(target=self.worker, args=(i, start, end,))
            self.processes.append(process)
            process.start()
            start = end
            end += int(items_for_worker)

        #join workers
        for i in range(0, workers):
            self.processes[i].join()
        print("All workers joint.\n")





    def worker(self, process, start, end):
        #check per vedere se il chunck e piu corto degli elementi effettivi (per la divisione in chunk)
        if end > len(self.users):
            end = len(self.users)
        #it evaluates the risk for each user in the chunk
        risks = dict()
        log = open('worker_'+str(process)+'.txt','w')
        #dizionario del worker specifico
        worker_users = dict()
        for index in range(start, end):
            user = self.users[index]
            worker_users[user] = self.dataset[user]
        #ordered by the length
        users_order_evaluation = list()
        for u in sorted(worker_users, key=lambda u: len(worker_users[u])):
            users_order_evaluation.append(u)
        log.write('Indexes: '+ str(start)+ ' '+ str(end))
        #apro il pickle file per salvare incrementalmente i risultati
        title = "../results/risks"+str(self.data)+str(process)+".p"
        with open(title, "ab") as pickle_file:
            #valuto ogni h
            for user in users_order_evaluation:
                user_sequence = self.dataset[user]
                risks[user] = dict()
                risks[user]['risk'] = list()
                risks[user]['seq'] = list()
                log.write('----------------------------------\n')
                log.write('Evaluating user '+ str(user)+'\n')
                log.write(' with sequence '+ str(user_sequence)+'\n')
                log.write('length '+ str(len(user_sequence))+'\n')
                if len(user_sequence) < 6:
                    result = self.risk_evaluation(user_sequence, user)
                    risks[user]['risk'].append(result)
                    risks[user]['seq'].append(user_sequence)
                for h in range(5, 7):
                    #all the seqs length h
                    seqs = combinations(user_sequence, h)
                    if not seqs:
                        break
                    temp = list()
                    flag = True
                    for seq in seqs:
                        result = self.risk_evaluation(seq, user)
                        if result == 1.0:
                            flag = False
                            risks[user]['risk'].append(result)
                            risks[user]['seq'].append(seq)
                            break
                        else:
                            temp.append((result, seq))
                    if flag and len(temp) > 1:
                        t = max(temp,key=itemgetter(0))
                        risks[user]['risk'].append(t[0])
                        risks[user]['seq'].append(t[1])
                #dump del risultato dell'utente
                pickle.dump(risks, pickle_file)

    def risk_evaluation(self, seq, user_eval):
        #it evaluates the risk as 1/the number of people having seq
        count = 0
        result = 0
        for user in self.complete_dataset.keys():
            flag = True
            start_at = -1
            locs = []
            for element in seq:
                try:
                    loc = self.complete_dataset[user].index(element,start_at+1)
                except ValueError:
                    flag = False
                    break
                else:
                    locs.append(loc)
                    start_at = loc
            if flag is True:
                count += 1
        if count > 0:
            result = 1/float(count)
        else:
            print('utente ', user_eval)
            print('seq ', seq)
            print(self.complete_dataset[user_eval])
        return result


