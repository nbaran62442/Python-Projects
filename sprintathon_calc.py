import pandas as pd
import numpy as np
import re

'''
PATCH NOTES FOR NEXT STHON
DATE: 05 27 2024

- People should not change their nicknames if they are participating. The code see them as two different users.
- Does not take into account commas for word counts over 1000. Try to fix that.
- Figure out a way to tell the code if it's a weekend sprintathon, and add an extra 3 points to participation score
- Output to google sheets file instead of excel. Or even CSV (read by both). 
- Some entries copied with the discord coding in the text (ex: **, `, <>), which had to be manually changed
- Figure out a way to have output files go to output folder and not main folder



'''

# =============================================================================
# Import our spreadsheet information.
input_filename = r"C:\Users\nbara\Documents\syot_mod\MegaSthonSheets\Submission_Form_July_2026_Responses.xlsx"
# Read the sprint data into the value of 'all_sprint', skipping the first/title 
# row of our spreadsheet.
# all_sprint = pd.read_excel(input_filename)#["Output"]
all_sprint = pd.read_excel(input_filename)["Paste below the output from Sprinto to submit the sprint"]
# all_sprint = pd.read_excel(input_filename)["put the shit here"]
# Create a dictionary for our results. 
# =============================================================================
results = {} # word counts only
results2 = {} # word counts and participation counts


# -----------------------------------------------------------------------------
# Testing zone - for print statements in case code breaks !

# sprint_num = 0
# print(all_sprint)
# print("number of sprints: ", len(all_sprint))
# print(all_sprint[6])
# print(type(all_sprint))

# print(all_sprint[178:189])

# end_sprint = all_sprint[178:189]
# print(len(end_sprint))
# -----------------------------------------------------------------------------

# =============================================================================
# Analyze each sprint individually in this for loop. The results for each user 
# are inputted into the results dictionaries.
# =============================================================================
for sprint in all_sprint:
    # Only use non-nan values. Valid sprints should not be nans.
    if sprint is not np.nan:
        # Here, we are finding how many participants there are in the sprint.
        # print(sprint)
        # all_counts = re.findall("(?<=[0-9]\\. ).+(?= words)", sprint)
        all_counts = re.findall("(?<=`[0-9]\\.` ).+(?= words\*\*)", sprint) # <-- this version gets only the sprints that add words
        # `1.` <@!502563569779605516> — **220 words** (15 wpm)
        print("All counts = ", all_counts)
        # For each participant, we need their username and word count.
        for count in all_counts:
            # (Test print statements)
            # print("sprint num:", sprint)
            print("count num:", count)
            
            # Username: first equation is for getting nicknamed discord tags
            # Second equation is for getting from discord user IDs
            # user = re.search("(?<=@).+(?= — [0-9])", count).group()
            user = re.search(".+(?= —)", count).group()
            print("User = ", user)
            
            # WC: first equation is for getting from nicknamed discord tags
            # Second equation is for getting from discord user IDs
            # wc = int(re.search("(?<=. — )[0-9]+", count).group())
            wc = int(re.search("(?<=. — [*][*])[0-9]+", count).group())
            print("WC = ", wc)
            
            # results2 puts the word count and participation count in a dictionary 
            # under the same user. Here, we initialize the dictionary to assign 
            # a (currently empty) list of items to each user rather than a single value
            results2.setdefault(user, [])

                              
            try:
                results[user] += wc # *multiplier
                
                # If the user exists in the dictionary and there are items in 
                # the list, update the first element (0) with the word count from 
                # this sprint and add one to the second element (1) to increase 
                # the participation count.
                results2[user][0] += wc
                results2[user][1] += 1
                

            except Exception:
                results[user] = wc # *multiplier
                
                # If there are no items in the list yet (i.e. a new user is 
                # participating), append the word count to be the first element 
                # of the list, and the participation (1 automatically) as the
                # second element of the list
                results2[user].append(wc)
                results2[user].append(1)
        
        # ----------
        # if entry says deleted, dont add wc, but keep adding participation
        deleted_words = re.findall("(?<=`[0-9]\\.` ).+(?= words deleted)", sprint)
        for count in deleted_words:
            print("count num (del):", count)
            user = re.search(".+(?= —)", count).group()
            print("User (del) = ", user)
            wc = 0
            print("WC (del) = ", wc)
            results2.setdefault(user, [])
            try:
                results[user] += wc
                results2[user][1] += 1
            except Exception:
                results[user] = wc
                results2[user].append(wc)
                results2[user].append(1)
        # ----------
            
            
            # print("User: ", user)
            # print("WC: ", wc)
             
print(results)
# print(results2)


output_data = pd.DataFrame.from_dict(results, orient="index")
output_data = output_data.sort_values(0, ascending = False)
output_data.reset_index(inplace=True)

# =============================================================================
# Put our results in a pandas data frame and sort them by ascending word count values
# =============================================================================
output_data2 = pd.DataFrame.from_dict(results2, orient="index")
output_data2 = output_data2.sort_values(0, ascending = False)
output_data2.reset_index(inplace=True)

# =============================================================================
# Print final results.
# =============================================================================
# print(output_data)
print(output_data2)
#%%
# =============================================================================
# Save final data to an excel file !
# =============================================================================
# output_data.to_excel(f"{input_filename[0:-5]}_wc_rankings.xlsx", header=False, index=False)
output_data2.to_excel(f"{input_filename[0:-5]}_wc_rankings_participation.xlsx", header=False, index=False)

#%%

# print("sprint_num:", sprint_num) 

# print(results) 
# print(len(results))

a = {}

user = ["darth nell", "moose", "jade"]
wc1 = [200, 500, 100]
participation = 1

for i in range(len(user)):
    name = user[i]
    a[name] = [wc, participation]
    a[name][0] = wc1[i]



print(a)


# a[user][0] += wc
# a[user][1] += participation

# print(a)

