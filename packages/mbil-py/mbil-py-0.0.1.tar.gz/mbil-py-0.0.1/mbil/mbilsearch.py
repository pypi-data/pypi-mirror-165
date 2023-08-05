import collections
import csv
import math
from collections import defaultdict, Counter
import pandas as pd
from mbil import scores
from mbil import mbilscore
import matplotlib.pyplot as plt

import itertools

# Output: should be natural log of score


class directCause:
    def __init__(self, new_dataset,alpha,target,maximum_number_of_parents):
        self.new_dataset = new_dataset
        self.parent_list = list(self.new_dataset.columns)
        self.target = target
        self.alpha = alpha
        self.parent_list.remove(self.target)
        self.score = scores.BDeuScore(dataset_df=self.new_dataset, alpha=self.alpha, target=self.target)
        self.mbilscore = mbilscore.mbilscore(dataset_df=self.new_dataset, target=self.target, alpha = self.alpha)
        self.maximum_number_of_parents = maximum_number_of_parents
        self.direc_cause = self.detecting_direct_cause()


    def detecting_direct_cause(self):
        '''
        A function to detect the true parents according to the parent list, parent_list will be like B  ['B', 'C']  ['B', 'F']  ['C', 'D']  ['D', 'F']  ['C', 'F']

        :return float: a list including all direct cause according to the parent list
        '''


        def iterator(parent_list):
            for item in parent_list:
                yield item
        def getsubsets(input ,length):
            #print(input)
            def dfs(input, length, start_index, acc, sol):
                if (len(acc) == length):
                    sol.append(acc[:])
                    return
                if input and start_index == len(input):
                    return
                element = input[start_index]
                acc.append(element)
                dfs(input, length, start_index + 1, acc, sol)
                acc.remove(element)
                dfs(input, length, start_index + 1, acc,sol)
            res = []
            dfs(input, length, 0, [], res)
            return res

        def increaseScore(input):
            index = -1
            cur_list_score = self.score.calculate_BDeu(input)
            #print("Score computed for set "+ str(B) +" is: "+ str(cur_list_score))
            list_B = input[:]
            for item in list_B:
                copy_list = list_B[:]
                copy_list.remove(item)
                # if len(copy_list) == 0:
                #     #print("stop")
                new_score = self.score.calculate_BDeu(copy_list)
                #print("New score is " + str(copy_list) + str(new_score))
                if new_score > cur_list_score:
                    cur_list_score = new_score
                    index = list_B.index(item)
            if index != -1:
                input.remove(list_B[index])
        # parent_list =
        i = 0
        while (len(self.parent_list) > i) and (i <= self.maximum_number_of_parents):
            #self.parent_list = iterator(self.parent_list)
            for predictor in self.parent_list[:]:
                cur_parent = self.parent_list[:]
                cur_parent.remove(predictor)
                #print("cur_parent " + str(cur_parent) +" i " + str(i))
                blockersofsizeI = getsubsets(cur_parent,i)
                #print("blockersofsizeI " + str(blockersofsizeI))
                #print()
                for subset in blockersofsizeI:
                    B = []
                    if predictor in self.parent_list:
                        B = subset[:]
                        #print(predictor)
                        B.append(predictor)
                        increaseScore(B)
                        if predictor not in B:
                            self.parent_list.remove(predictor)
            i+=1
        return self.parent_list






class mbilsearch:
    # get top single predictors and top interaction predictors and transform dataset df and new_status_dataset
    def __init__(self, threshold, max_single_predictors, max_interaction_predictors, max_size_interaction,dataset_df, alpha, target):
        '''
        init function of search class,include functions "get_single_predictors_score", "get_interaction_predictors_score", "get_new_dataset_after_transform" and so on.

        :param single_list_score: A list to store the single predictor and their corresponding score after MBIL search process
        :param interaction_list_score: A list to store the interaction predictor and their corresponding score after MBIL search process
        :param transformed_dataset: A dictionary to store the transformed dataset

        '''
        self.alpha = alpha
        self.target = target
        self.threshold = threshold
        self.dataset = dataset_df
        self.max_single_predictors = max_single_predictors
        self.max_interaction_predictors = max_interaction_predictors
        self.max_size_interaction = max_size_interaction
        self.score = scores.BDeuScore(dataset_df=dataset_df, alpha=alpha, target=target)
        self.mbilscore = mbilscore.mbilscore(dataset_df=self.dataset, target=self.target, alpha = self.alpha)
        #self.interaction_list_score = collections.OrderedDict()
        self.interaction_list_score = self.get_interaction_predictors_score()
        self.single_list_score = self.get_single_predictors_score()
        # initialize the new dataset, kind of global variable
        self.new_dataset = {}
        # use get_new_dataset_after_transform to fill transform dataset
        self.transformed_dataset = self.get_new_dataset_after_transform()
        self.new_status_dataset = {}


    def get_single_predictors_score(self):
        '''
        A function to get all single predictors which the score is greater than null_score, the user can give the specific path to write it out.

        :return float: a list including all single predictors and corresponding score
        '''
        predictors_list = self.score.dataset_head
        predictors_list.remove(self.target)
        null_score = self.mbilscore.calculate_score(subset_size=0, top="all").values()
        null_score = list(null_score)[0]
        score_dict = self.mbilscore.calculate_score(subset_size=1, top="all")
        single_res = []

        for key,val in score_dict.items():
            if int(val) > null_score:
                single_res.append((key.strip("[]''"),val))


        return single_res



    def get_interaction_predictors_score(self):
        '''
        A function to get top interaction predictors and corresponding score according to the input self.max_interaction_predictors

        :return float: a list including all interaction predictors and corresponding score
        '''
        interaction_res = {}
        #score = BDeuScore(dataset_input_directory=self.dataset_input_directory, alpha=self.alpha, target=self.target)
        #number_of_predictors = score.n
        for i in range(2,self.max_size_interaction + 1):
            cur_infoGain_stren = self.score.calculate_interaction_strength(subset_size=i,dataset = self.dataset,threshold = self.threshold)
            cur_score_dict = self.mbilscore.calculate_score(subset_size=i)
            for key,val in cur_score_dict.items():
                if key in cur_infoGain_stren:
                    interaction_res[key] = cur_score_dict[key]
        #return Counter(self.interaction_list_score).most_common(1)
        final_res = Counter(interaction_res).most_common(self.max_interaction_predictors)
        return final_res

    def get_new_dataset_after_transform(self):
        '''
        A function to generate transformed dataset according to search result like, [[B, ['B', 'C'], ['B', 'F'], ['C', 'D'], ['D', 'F'], ['C', 'F'], E], [0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1],[1, 2, 2, 2, 2, 2, 0],[1, 2, 2, 2, 2, 2, 1],[0, 0, 3, 3, 3, 1, 0]]

        :return: dataframe see above
        '''
        def generate_inter_list(interaction):
            interaction = list(interaction[0][1:-1].split(", "))
            new_col = []
            for i in range(self.score.m):
                new_val = ""
                for item in interaction:
                    item = item.strip("'")
                    new_val += str(self.score.dataset_df[item][i])

                new_col.append(new_val)
            return new_col

        def generate_new_status_dataset(newdataset):
            '''
            A function to generate the transformed dataset status according to newdataset

            :return: a matrix
            '''

            newdataset_matrix = list(newdataset.values())
            m = len(newdataset_matrix)
            n = len(newdataset_matrix[0])
            new_status_dataset = [[0 for _ in range(n) ] for _ in range(m)]
            for i in range(m):
                status_size = len(set(newdataset_matrix[i]))
                status_set = list(set(newdataset_matrix[i]))
                status_set_add_size = [status_size]
                #print(status_set_add_size)
                status_set_add_size.extend(status_set)
                for j in range(len(status_set_add_size)):
                    new_status_dataset[i][j] = status_set_add_size[j]
            return new_status_dataset


        # score = BDeuScore(dataset_input_directory=self.dataset_input_directory, alpha=self.alpha, target=self.target)

        #new_dataset = collections.defaultdict(list)
        #self.new_dataset = {}
        for item in self.single_list_score:
            new_col = []
            hash_table = {}
            i = 0
            feature_original_list = list(self.score.dataset_df[item[0]])
            for val in feature_original_list:
                if val not in hash_table:
                    hash_table[val] = i
                    i += 1
                new_col.append(hash_table[val])
            self.new_dataset[item[0]] = new_col
        # print(new_dataset)
        for item in self.interaction_list_score:
            new_feature_list = generate_inter_list(item)
            new_col = []
            hash_table = {}
            i = 0
            for val in new_feature_list:
                if val not in hash_table:
                    hash_table[val] = i
                    i += 1
                new_col.append(hash_table[val])
            self.new_dataset[item[0]] = new_col
        self.new_dataset[self.score.target] = list(self.score.dataset_df[self.score.target])
        self.new_status_dataset = generate_new_status_dataset(self.new_dataset)
        #print(self.new_dataset)
        self.new_dataset = pd.DataFrame(self.new_dataset)
        # format the key from "['B','C']" to "BC"
        # for key,val in self.new_dataset.items():
        #     key = key[1:-1].split(',')
        #     print(key)
        return self.new_dataset

    def plot_score_aftersearch(self):
        '''
        A function to plot the bar graph of final  predictors(both single nodes and interactions) according to the result of MBIL search

        :return: bar graph
        '''

        res = self.single_list_score

        dic = {}
        for item in res:
            dic[item[0]] = item[1]
        for item in self.interaction_list_score:
            dic[item[0]] = item[1]

        plt.bar(*zip(*dic.items()))
        plt.title("Bdeu score of " + str(len(dic)) + " predictors after MBIL search")
        plt.show()
        #print(res_hash)
















