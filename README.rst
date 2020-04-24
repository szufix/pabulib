# Participatory Budgeting Library

Short guide:

the crucial function is MTC and it is located inside the file voting/methods.py
It takes three arguments, first is the name of the experiment, second is name of the district/region/instance and the third is the budget limit. It's important to name votes and projects files with the same name -- and that name is the second argument (without ".txt").

    
For approval ballots put the word "approval" in the first line then number_of_voters in the second line, and then each line contains approved candidates separated by comas -- that is, each line correspond to one vote.

For cumulative ballots put the word "cumulative" in the first line then number_of_voters in the second line and then each even line contains approved candidates separated by comas and each odd line contains the utilities separated by comas -- that is, each two lines correspond to one vote.

If the description is not clear please see data in toy_example.

The winners file contain the number of winner in the first line, and in the second line are all the winners separated by comas.
