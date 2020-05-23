import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

# Read data from file 'filename.csv'
# (in the same directory that your python process is based)
filename = "clean.csv"
data = pd.read_csv(filename)
df = pd.DataFrame(data)

#Avg_Combat_Score - Damage: 1 point each Kills based on enemies alive: 150/130/110/90/70 Multikills: +50 per additional round kill
h=sns.regplot(x=df.index, y=(df['avg_combat_score']))
h.set( title = 'Average Combat Score Over Time'.format(filename), xlabel = 'Game Number', ylabel = "Average Combat Score")
plt.show()

i=sns.regplot(x=df.index, y=(df['k']/df['d']))
i.set( title = 'Kill:Death Ratio Over Time'.format(filename),xlabel = "Game Number", ylabel = "K:D Ratio")
plt.show()

j=sns.swarmplot(x=df['map'],y=(df['k']/df['d']), hue = df['result'], palette='colorblind')
j.set(title = 'Kill:Death Ratio on all Maps'.format(filename),xlabel = 'Map Name', ylabel = "K:D Ratio")
plt.show()

k=sns.swarmplot(x=df['result'],y=df['d'], palette='pastel')
k.set(title = 'Relationship between deaths and match result'.format(filename),xlabel = 'Result', ylabel = "Deaths")
plt.show()

l=sns.regplot(x=df['k'], y=df['econ_rating'])
l.set( title = 'Relationship between economy rating and kills'.format(filename),xlabel = "Kills", ylabel = "Economy Rating")
plt.show()


## The following plots require additional data columns not currently implemented in the data scraping script

# m=sns.swarmplot(x=df['agent'],y=df['k'], hue = df['result'], palette = 'colorblind')
# m.set(title = 'Which agent do I play best with?'.format(filename), xlabel = 'Agent', ylabel = "Kills")
# plt.show()
#
# n=sns.violinplot(x=df['pregames'], y=df['avg_combat_score'], palette = 'colorblind')
# n.set( title = 'How does number of consecutive games affect Average Combat Score ?'.format(filename), xlabel = 'Number of Consecutive Games played', ylabel = "Average Combat Score")
# plt.show()
#
# o=sns.swarmplot(x=df['weekday'], y=df['avg_combat_score'],hue = df['result'], palette = 'colorblind')
# o.set( title = 'How does weekday affect Average Combat Score ?'.format(filename), xlabel = 'Weekday', ylabel = "Average Combat Score")
# o.set_xticklabels(['Su','M','T','W','R','F','Sa'])
# plt.show()
#
# p=sns.swarmplot(x=df['with_friends'], y=df['k']/df['d'], hue = df['result'], palette = 'colorblind')
# p.set( title = 'How does playing with friends affect K:D and results ?'.format(filename),xlabel = 'Playing as Party?', ylabel = "K:D Ratio")
# p.set_xticklabels(['No','Yes'])
# plt.show()
