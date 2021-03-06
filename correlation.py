"""
Created on November 14, 2017
@author: Melody Tribble & Xuying Wang

"""

import collections
from scipy.stats.stats import pearsonr
from scipy.stats.stats import spearmanr
import matplotlib.pyplot as plt


# This class calculates the Pearson's correlation coefficient and p-value for a given data set
class Pearson:

    # This creates a new instance of the Pearson Class
    # @param data = dictionary containing two sets of data to analyse
    def __init__(self, data):
        self.data = data  # This is a dictionary {Age: number of roles}
        print('\n\nQ1. Is there a positive or a negative correlation between age and number of roles an '
              'actor stars in?')
        print("Using Pearson's Correlation Coefficient")
        self.run_pearson()

    # This splits the data into two lists and runs pearson's on it.
    def run_pearson(self):

        age_list = []
        num_roles_list = []

        # sort the dictionary by age
        od = collections.OrderedDict(sorted(self.data.items()))

        # split dictionary into two lists
        for key in od:
            age_list.append(key)
            num_roles_list.append(od[key])

        # set pcc and pvalue as the values returned from pearsonr()
        pcc, pvalue = pearsonr(age_list, num_roles_list)

        print("Pearson correlation coefficient: ", pcc)
        print("P-value: ", pvalue)

        # visualize results
        plt.scatter(age_list, num_roles_list, s=10)
        plt.xlabel("Actor Age")
        plt.ylabel("Number of roles")
        plt.title("Relationship between Actor Age and Number of Roles")
        plt.show()


# This class calculates the Spearman Rank correlation coefficient and p-value for a given
# data set using the scipy.stats library
class SpearmanRank:

    # creates a new instance of Spearman Rank and starts the model
    # @ param data = data to run the model on
    def __init__(self, data):
        print("\n\nQ4: Is there a correlation between a movie's country and budget?")
        print('Created SpearmanRank')
        self.data = data
        self.run_spearman()

    # This preps the data, starts the spearman rank model, and visualizes the results
    def run_spearman(self):
        country_l = self.data[0]
        budget_l = self.data[1]

        # sets the results from spearmanr to the coefficient and p-value variables
        coef, pval = spearmanr(country_l, budget_l)

        print("Spearman Coefficient: ", coef)
        print("P-value: ", pval)

        # plot relationship b/w country and budget
        plt.scatter(country_l, budget_l, s=10)
        plt.xlabel("Country Code")
        plt.ylabel("Budget")
        plt.title("Relationship between Country and Budget")
        # plt.show()
