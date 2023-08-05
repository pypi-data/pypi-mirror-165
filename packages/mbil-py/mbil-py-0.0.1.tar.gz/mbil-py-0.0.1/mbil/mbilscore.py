from matplotlib import pyplot as plt
from mbil import scores
# scores_abs will use the class and function that defined in scores.py
class mbilscore:
    def __init__(self,dataset_df, target, alpha):
        self.dataset_df = dataset_df
        self.target = target
        self.m = self.dataset_df.shape[0]
        self.alpha = alpha

        # self.bdeu = scores.BDeuScore(dataset_df=dataset_df, alpha=alpha, target=target)
        # self.


    def generate_subset(self, feature_list, subset_size):
        '''
        A function to generate all possible subset according to the subset_size

        :param feature_list: the list that includes all features in the dataset, it will be ["B", "C", "D", "F"] based on example dataset
        :param subset_size:  the size of the subset you want to generate

        :return list: a list that include all possible subset, if the subset_size == 2, it will be [["B", "C"], ["B", "D"], ["B", "F"], ["C", "D"],["C", "F"], ["D","F"]]
        '''
        if subset_size == 0:
            return [[]]

        def dfs(index, cur):
            if len(cur) == subset_size:
                result.append(cur[:])
                return
            for i in range(index, len(feature_list)):
                dfs(i + 1, cur + [feature_list[i]])

        index = 0
        cur = []
        result = []
        dfs(index, cur)
        return result
    def calculate_score(self, subset_size, top = "all"):
        '''
        A function to calculate BDeuscore based on subset_size, it will return the score of all possible specific subset with the input subset_size

        :param self: instance of BDeuScore class
        :param subset_size: a int to represent the length of the subset

        :return score: a hash map to store all possible result, the key is the subset and the value is the BDeu score, like{"['B','C']":-3.7534179752515073, "['B','D']":-4.382026634673881,...}
        '''
        Bdeu = scores.BDeuScore(dataset_df=self.dataset_df, alpha=self.alpha, target=self.target)
        feature_list_excepet_target = list(self.dataset_df.columns)

        #print(feature_list_excepet_target)
        feature_list_excepet_target.remove(self.target)
        #print(feature_list_excepet_target)
        subset = self.generate_subset(feature_list_excepet_target, subset_size)

        res = {}
        #print(subset)
        for subset in subset:
            # print("h")
            # print(subset)

            res[str(subset)] = Bdeu.calculate_BDeu(subset)

        if top == 'all':
            return res
        else:
            return sorted(res.items(), key=lambda item: item[1], reverse=True)[:top]

    def calculate_information_gain(self,subset_size,top = "all"):
        '''
        A function to calculate information gain based on subset_size, it will return the score of all possible specific subset with the input subset_size

        :param self: instance of BDeuScore class
        :param subset_size: a int to represent the length of the subset

        :return score: a hash map to store all possible result, the key is the subset and the value is the information score, like{"['B','C']":0.5709505944546684, "['B','D']":0.4199730940219749,...}
        '''

        m = self.dataset_df.shape[0]
        feature_list_excepet_target = list(self.dataset_df.columns)
        IGain = scores.IGain(dataset_df=self.dataset_df, alpha=self.alpha, target=self.target)
        res = {}

        #print(feature_list_excepet_target)
        feature_list_excepet_target.remove(self.target)
        subset = self.generate_subset(feature_list_excepet_target, subset_size)

        for each_com in subset:
            score = 0
            if len(each_com) == 0:
                score = 1
            else:
                score = IGain.calculate_IGain(each_com)
            res[str(each_com)] = score

        if top == 'all':
            return res
        else:
            return sorted(res.items(), key=lambda item: item[1], reverse=True)[:top]

    def check_if_add(self, curset, dataset,threshold = 0.05):
        '''
        A function to check is this curset interaction can be added to the

        :param self: instance of BDeuScore class
        :param curset: the set you want to use to check if should be added
        :param threshold: the threshold you want to use
        :return score: a hash map to store all possible result, the key is the subset and the value is the BDeu score, like{"['B','C']":-3.7534179752515073, "['B','D']":-4.382026634673881,...}
        '''

        m = self.m
        target = self.target
        dataset_df = self.dataset_df
        def isExitCase(single_set,single_set_ig,curset,curset_ig):
            set_minus_A = curset[:]
            set_minus_A.remove(single_set[0])
            # print(set_minus_A)
            set_minus_A_ig = self.calculate_informationgain_each_subset(set_minus_A) * m
            #set_minus_A_score = self.calculate_score_each_subset(set_minus_A, dataset_model_withoutA) * m
            sum_score = single_set_ig + set_minus_A_ig
            cur_is = (curset_ig - sum_score) / curset_ig
            if cur_is < self.IS:
                self.IS = cur_is
            return cur_is < threshold
        def stillAddable(curset,curset_ig):
            for feature in curset:
                single_set = [feature]
                single_set_ig = self.calculate_informationgain_each_subset(single_set) * m
                #single_set_score = self.calculate_score_each_subset(single_set, dataset_model_single) * m
                # calculate the set without the single
                # print(curset)

                if isExitCase(single_set,single_set_ig,curset,curset_ig):
                    return False
            return True
        add = False
        self.IS = 1
        curset_ig = scores.IGain.calculate_IGain(curset) * self.m
        #curset_score = self.calculate_score_each_subset(curset, dataset_model) * self.m

        if len(curset) > 1:
            add = stillAddable(curset,curset_ig)
        # is the size of subset is greater than 3, we need to use recursive to break it into all two possible combination

        # if add and len(curset) > 3:
        #     add =
        #I need to use add = recursiveInfoSearch exhaustiveinformationgain 241

        if add:
            self.interaction_strength[str(curset)] = self.IS
        return add

    def plot_score(self,subset_size):
        '''
        A function to plot the bar graph of final single predictors according to the size of subset
        :param subset_size: the subset size you want to use to plot the bar graph
        :return: bar graph
        '''
        res = self.calculate_score(subset_size = subset_size)
        plt.bar(*zip(*res.items()))
        plt.title("Bdeu score of " + str(subset_size) + " predictors")
        plt.show()
        #print(res_hash)

    def plot_information_gain(self, subset_size):
        '''
        A function to plot the bar graph of final interaction predictors according to the size of subset
        :param subset_size: the subset size you want to use to plot the bar graph
        :return: bar graph
        '''
        res = self.calculate_information_gain(subset_size = subset_size)
        plt.bar(*zip(*res.items()))
        plt.title("Information gain of " + str(subset_size) + " predictors")
        plt.show()
# from abc import ABC, abstractmethod
#
#
# class AbstractClassName(ABC):
#     @abstractmethod
#     def abstract_method_name(self):
#         pass