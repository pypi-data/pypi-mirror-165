import collections
import math
from collections import defaultdict, Counter
import pandas as pd
import itertools
class ReadDataset:
    def __init__(self, file, sep='\t'):
        self.file = file
        self.sep = sep
        self.dataset_df = self.read()
    def read(self):
        '''
        A function to read into a dataframe the dataset according to the input directory of this dataset

        :param file: input directory of this dataset
        :param sep: the delimiter of the dataset like '\t' or ',', default='\t'

        :return dataset: the dataset with data frame format in python
        '''
        dataset_df = pd.read_csv(filepath_or_buffer=self.file, sep=self.sep, lineterminator='\n')
        columns_name = list(dataset_df.columns)
        columns_name[-1] = columns_name[-1].strip()
        dataset_df.columns = columns_name

        return dataset_df
class Dataset:
    def __init__(self, dataset, target = "E", subset = ["B", "C"]):
        '''
        init function of Dataset class
        :param dataset: the return df from readDataset function
        :param target: the name of the classifier of the model
        :param subset: the name of parent node you want to use in the bayesian network

        '''
        self.number_nodes = dataset.ndim
        self.subset = subset
        self.dataset = dataset
        self.target = target

    def get_target_status(self):
        '''
        A function to get the status of the classifier

        :param self: the instance of dataset class

        :return list: A list that include all unique values of classifier
        '''

        return self.dataset[self.target].unique()

    def get_subset_status(self):
        '''
        A function to get the status of the feature in subset

        :param self: the instance of dataset class

        :return map: A map include all unique values of features in subset
        '''
        subset_status_map = defaultdict(list)
        #print(self.subset)
        for item in self.subset:
            item = item.strip("'")
            subset_status_map[item] = self.dataset[item].unique()
        return subset_status_map

    def get_feature_count(self, feature_name):
        '''
        A function to get the count of different feature by feature name

        :param self: the instance of dataset class
        :param feature_name: the name of feature you want to count

        :return Counter: A map that key is the different values for this feature_name and the value is the corresponding count of this value
        '''
        return Counter(self.dataset[self.target])

    def get_parent(self,subset_status_map):
        '''
        A function to get all the possible parent based on the current dataset


        :param self: the instance of dataset class
        :param subset_status_map: a map that the key is the name of current feature and the value is the corresponding unique values of this feature

        :return parent_list:  a list that include all possible parent combinations, when the subset_status_map is {"B":[2,3],"C":[0,1]}, the parent list will be [[0,0], [0,1], [1,0], [1,1]]
        '''
        #defaultdict(<class 'list'>, {'B': array([2, 3], dtype=int64), 'C': array([1, 0], dtype=int64)})
        node_list = list(subset_status_map.values())
        n = len(node_list)
        for i in range(n):
            node_list[i] = list(node_list[i])

        #print(node_list)
        parent_list = list(itertools.product(*node_list))
        #print(parent_list)
        return parent_list

    def get_all_count(self,subset,parent,target_status):
        '''
        A function to get the count of records according to current subset and parent set

        :param self: the instance of dataset class
        :param subset: the current subset like ["B","C"] or ["C","D"]
        :param parent: one of possible parents based on the current subset, if the subset is ["B","C"],B(2,3),C(0,1) the parent list will be [0,0] or [0,1] or [1,0] or [1,1]
        :param target_status: the current target status like "0" or "1"

        :return count: it will be the int the represents how many records you have in the dataset based these conditions
        '''
        select_df = self.dataset
        for i in range(len(subset)):
            select_df = select_df[(select_df[subset[i]] == int(parent[i]))]
        select_df = select_df[(select_df[self.target] == target_status)]
        # subset= [B,C]
        # parent[(2,1)]
        # target_status = 0
        return select_df.shape[0]


    #count = dataset_model.get_all_count(each_com, parent, target_status)

    def get_feature_count_according_target(self,feature_name, feature_value,target_value):
        '''
        A function to get the count of different feature by feature name and feature value


        :param self: the instance of dataset class
        :param feature_name: the name of current feature like "B"
        :param feature_value: one feature name will have different values, for feature "B", it includes "2" or "3"
        :param target_value: the current target value like "0" or "1"

        :return count: it will be the int the represents how many records you have according to the specific condition for the input
        '''
        df2 = self.dataset[(self.dataset[feature_name] == int(feature_value)) & (self.dataset[self.target] == int(target_value))]
        #print(df2)
        return df2.shape[0]
    def get_dataset_size(self):
        """
        A function to get the status of classifier

        :param self: the instance of dataset class

        :return list: A list that include all unique values of classifier
        """

        return(self.dataset.shape)

# '''
# This function is to compute the dimension of the dataset, which contains number of datapoints and number of columns (features) of datapoints in the input dataset.
#
# :return size: the size of dataset as an array of two values.
# '''
# Output: should be natural log of score






















#
#
# class Dataset:
#     def __init__(self, dataset, target = "E", subset = ["B", "C"]):
#         '''
#         init function of Dataset class
#         :param dataset: the return df from readDataset function
#         :param target: the name of the classifier of the model
#         :param subset: the name of parent node you want to use in the bayesian network
#
#         '''
#         self.number_nodes = dataset.ndim
#         self.subset = subset
#         self.dataset = dataset
#         self.target = target
#
#     def get_target_status(self):
#         '''
#         A function to get the status of classifier
#
#         :param self: the instance of dataset class
#
#         :return list: A list that include all unique values of classifier
#         '''
#
#         return self.dataset[self.target].unique()
#
#     def get_subset_status(self):
#         '''
#         A function to get the status of the feature in subset
#
#         :param self: the instance of dataset class
#
#         :return map: A map include all unique values of features in subset
#         '''
#         subset_status_map = defaultdict(list)
#         #print(self.subset)
#         for item in self.subset:
#             item = item.strip("'")
#             subset_status_map[item] = self.dataset[item].unique()
#         return subset_status_map
#
#     def get_feature_count(self, feature_name):
#         '''
#         A function to get the count of different feature by feature name
#
#         :param self: the instance of dataset class
#         :param feature_name: the name of feature you want to count
#
#         :return Counter: A map that key is the different values for this feature_name and the value is the corresponding count of this value
#         '''
#         return Counter(self.dataset[self.target])
#
#     def get_parent(self,subset_status_map):
#         '''
#         A function to get all the possible parent based on the current dataset
#
#
#         :param self: the instance of dataset class
#         :param subset_status_map: a map that the key is the name of current feature and the value is the corresponding unique values of this feature
#
#         :return parent_list:  a list that include all possible parent combinations, when the subset_status_map is {"B":[2,3],"C":[0,1]}, the parent list will be [[0,0], [0,1], [1,0], [1,1]]
#         '''
#         #defaultdict(<class 'list'>, {'B': array([2, 3], dtype=int64), 'C': array([1, 0], dtype=int64)})
#         node_list = list(subset_status_map.values())
#         n = len(node_list)
#         for i in range(n):
#             node_list[i] = list(node_list[i])
#
#         #print(node_list)
#         parent_list = list(itertools.product(*node_list))
#         #print(parent_list)
#         return parent_list
#
#     def get_all_count(self,subset,parent,target_status):
#         '''
#         A function to get the count of records according to current subset and parent set
#
#         :param self: the instance of dataset class
#         :param subset: the current subset like ["B","C"] or ["C","D"]
#         :param parent: one of possible parents based on the current subset, if the subset is ["B","C"],B(2,3),C(0,1) the parent list will be [0,0] or [0,1] or [1,0] or [1,1]
#         :param target_status: the current target status like "0" or "1"
#
#         :return count: it will be the int the represents how many records you have in the dataset based these conditions
#         '''
#         select_df = self.dataset
#         for i in range(len(subset)):
#             select_df = select_df[(select_df[subset[i]] == int(parent[i]))]
#         select_df = select_df[(select_df[self.target] == target_status)]
#         # subset= [B,C]
#         # parent[(2,1)]
#         # target_status = 0
#         return select_df.shape[0]
#
#
#     #count = dataset_model.get_all_count(each_com, parent, target_status)
#
#     def get_feature_count_according_target(self,feature_name, feature_value,target_value):
#         '''
#         A function to get the count of different feature by feature name and feature value
#
#
#         :param self: the instance of dataset class
#         :param feature_name: the name of current feature like "B"
#         :param feature_value: one feature name will have different values, for feature "B", it includes "2" or "3"
#         :param target_value: the current target value like "0" or "1"
#
#         :return count: it will be the int the represents how many records you have according to the specific condition for the input
#         '''
#         df2 = self.dataset[(self.dataset[feature_name] == int(feature_value)) & (self.dataset[self.target] == int(target_value))]
#         #print(df2)
#         return df2.shape[0]
#
#     def get_dataset_size(self):
#         '''
#         A function to get the status of classifier
#
#         :param self: the instance of dataset class
#
#         :return list: A list that include all unique values of classifier
#         '''
#         return(self.dataset.shape)
#
#
#
#
# # if __name__ == "__main__":
# #     #dataset_input_directory = "../datasets/TEST.txt"
# #     dataset_input_directory = "../datasets/LSM-15Year.txt"
# #     output_directory = "C:/Users/CHX37/Practice"
# #     #alpha = 4
# #     alpha = 240
# #     #target = "E"
# #     target = "distant_recurrence"
# #     subset_size_list = [0,1,2]
# #     top = 20
# #     #subset_size_list = [1]
# #     #subset_size = 2
# #     res1 = {}
# #     res2 = {}
# #     for subset_size in subset_size_list:
# #         score = BDeuScore(dataset_input_directory, alpha, target, subset_size)
# #         ir_score = score.calculate_score()
# #         res1.update(ir_score)
# #         #res1.append(ir_score)
# #         ig_score = score.calculate_information_gain()
# #         res2.update(ig_score)
# #         #res2.append(ig_score)
# #     res1_sorted = sorted(res1.items(), key=lambda item: item[1])
# #     res2_sorted = sorted(res2.items(), key=lambda item: item[1])
# #     print(res1_sorted[:top])
# #     print(res2_sorted[:top])
#



