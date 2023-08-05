import csv
from datetime import date
today = date.today()
class output:
    def __init__(self, output_path, dataset_name, all_input, dataset_path, dataset_information, null_score, single_score, interaction_score, direc_cause):
        self.output_path = output_path
        self.dataset_name = dataset_name
        self.all_input = all_input
        self.dataset_path = dataset_path
        self.dataset_information = dataset_information
        self.null_score = null_score,
        self.single_score = single_score,
        self.interaction_score = interaction_score,
        self.direc_cause = direc_cause
    def output_log(self,output_path = "output/"):
        '''
        A function to output the log file

        :param output_path: the output_path to store the text file

        :return float: the text file including all input information and final result
        '''
        file_name = "Log " + self.dataset_name + str(today.strftime("%b-%d-%Y"))
        with open(output_path + file_name + '.txt', 'w') as f:
            f.write("The user entered values for the parameters:")
            for key, val in self.all_input.items():
                f.write(str(key) + ": " + str(val))
                f.write('\n')
            f.write('\n')
            f.write("Current dataset path:" + self.dataset_path)
            f.write('\n')
            for key, val in self.dataset_information.items():
                f.write(str(key) + ": " + str(val))
                f.write('\n')
            f.write('\n')
            f.write("Null Score:" + str(self.null_score))
            f.write('\n')
            f.write("Now printing the score of each of the single predictor models:")
            f.write('\n')
            for item in self.single_score:
                f.write(str(item))
                f.write('\n')
            f.write('\n')
            f.write("Now printing interactions and their scores learned by IGain:")
            f.write('\n')
            for item in self.interaction_score:
                f.write(str(item))
                f.write('\n')
            f.write('\n')

            f.write("Direct cause Identified: " + str(self.direc_cause))
            print("Put log file in " + output_path + " successfully")

    def output_single_predictors(self, output_path = "output/"):
        '''
        A function to output the single predictors

        :param output_path: the output_path to store the cvs file

        :return float: the cvs file including all single predictors after mbil search
        '''
        file_name = "Learned_nodes_" + self.dataset_name + "_" + str(today.strftime("%b-%d-%Y") + ".csv")
        with open(output_path+ file_name, 'w', encoding='UTF8') as f:
            # create the csv writer
            writer = csv.writer(f)
            for item in self.single_score:
            # write a row to the csv file
                writer.writerow(item)

        print("Put single nodes file in " + output_path + " successfully")

    def output_interaction_predictors(self, output_path = "output/"):
        '''
        A function to output the interaction predictors

        :param output_path: the output_path to store the cvs file

        :return float: the cvs file including all interaction predictors after mbil search
        '''
        file_name = "Learned_interactions_" + self.dataset_name + "_" + str(today.strftime("%b-%d-%Y") + ".csv")
        with open(output_path + file_name, 'w', encoding='UTF8') as f:
            # create the csv writer
            writer = csv.writer(f)
            for item in self.interaction_score:
            # write a row to the csv file
                writer.writerow(item)


        print("Put interaction nodes file in " + output_path + " successfully")



    def output_direct_cause(self, output_path = "output/"):
        '''
        A function to output the direct cause

        :param output_path: the output_path to store the cvs file

        :return float: the cvs file including all direct cause after mbil search
        '''
        file_name = "Learned_direct_cause_" + self.dataset_name + "_" + str(today.strftime("%b-%d-%Y") + ".csv")
        with open(output_path + file_name, 'w', encoding='UTF8') as f:
            # create the csv writer
            writer = csv.writer(f,delimiter=',')
            for item in self.direc_cause:
                # write a row to the csv file
                writer.writerow(item)

        print("Put direct cause file in " + output_path + " successfully")



        # for line in lines:
        #     f.write(line)
        #     f.write('\n')