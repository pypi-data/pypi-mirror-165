# MBIL

## What is MBIL
## MBIL Algorithm

## Explanation of MBIL Algorithm
1) determine_single_predictors learns the set PA1 of single-variable risk factors of a target T. The procedure does this by determining whether the BDeu score of the model in which the variable has an edge to T is greater than the BDeu score of the model in which T has no parents.
![MBILProcedure1_img.png](MBILProcedure1_img.png)
## Installation


## Main Classes Introduction
1. mbilscore.mbilScore: mbilScore was used to calculate the mbilScore according to the input dataset.

2. mbilsearch.mbilSearch: mbilSearch was used to find the strong single predictors and interaction predictors according to the threshold.

3. mbilsearch.directCause: directCause was used to out put the final direct cause after the mbil search.

4. scores.BDeuScore: BDeuScore was used to finish the basic calculation work about BDeuScore.

5. scores.IGain: IGain was used to finish the basic calculation work about IGain.

6. output.output: output was used to output the log and important result of the mbil search

## How to use mbil package and specific example
![img_7.png](img_7.png)





Example of BDeu Score
Chuhan finish
