import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import os, sys
import json
parentdir = Path(__file__).resolve().parents[1]
sys.path.append(parentdir)
data_path = os.path.join(parentdir,'data','annnotated_csv')
sys.path.append(data_path)


def main():
    topics = {
    "a": {},
    "r": {},
    "c": {},
    "p": {},
    "e": {},
    "o": {},
    "nc": {}
}
    #traverse the files. group by category and sentiment for each file (number of times per category-sentiment pair)
    for file in os.listdir(data_path):
        df = pd.read_csv(os.path.join(data_path,file),sep=",")
        count_series = df.groupby(['CATEGORY', 'SENTIMENT']).size()
        new_df = count_series.to_frame(name = 'size').reset_index()
        d = {k: (g["SENTIMENT"].tolist(),g["size"].tolist()) for k,g in new_df.groupby("CATEGORY")}
        #d is a dictionary of tuples which consist of 2 lists. Flatten it in a dict
        for key in d.keys():
            conversion = dict(zip(d[key][0], d[key][1]))
            d[key] = conversion
        #merge with the topics dictionary (do not overwrite)
        for key in topics:
            if(key in d.keys()):
                topics[key] = {k: topics[key].get(k, 0) + d[key].get(k, 0) for k in set(topics[key]) | set(d[key])}
    
    #x axis labels
    #x = ["Announcement","Restriction","Conspiracy","Politics","Personal Experience", "Personal Opinion", "No Context"]
    x = list(topics.keys())

    #not a great solution but create lists for each sentiment. Conspiracy does not have positive so avoid error by assigning 0.
    topics["c"]["p"] = 0
    n,p,nu = [],[],[]
    for topic in topics:
        n.append(topics[topic]["n"])
        p.append(topics[topic]["p"])
        nu.append(topics[topic]["nu"])

    #create the plot
    p1 = plt.bar(x, n, 0.7, color='r')
    p2 = plt.bar(x, nu, 0.7, bottom=n, color='b')
    p3 = plt.bar(x, p, 0.7, bottom=[sum(x) for x in zip(n,nu)], color='g')
    plt.title("Tweet Sentiments Per Topic")
    plt.xlabel('Topics', fontsize=14)
    plt.ylabel('Occurences', fontsize=14)
    plt.legend((p1[0], p2[0], p3[0]), (["negative", "neutral", "positive"]), fontsize=12, ncol=4, framealpha=0, fancybox=True)
    plt.savefig(os.path.join(parentdir,'data','sentiment_graph.png'))

    #sentiment per topic json file generation to use in our table
    sentiment_per_topic = topics.copy()
    totals= []
    for topic in topics:
        s = (sum(topics[topic].values()))
        totals.append(s)
        p_percent, nu_percent, n_percent = topics[topic]["p"]/s * 100, topics[topic]["nu"]/s * 100, topics[topic]["n"]/s * 100
        p_percent, nu_percent, n_percent = ("%.2f" % p_percent), ("%.2f" % nu_percent), ("%.2f" % n_percent)
        sentiment_per_topic[topic]["p"] = p_percent
        sentiment_per_topic[topic]["nu"] = nu_percent
        sentiment_per_topic[topic]["n"] = n_percent
    
    #dump the dict
    with open(os.path.join(parentdir,'data','sentiment_per_topic.json'), 'w') as f:
        json.dump(sentiment_per_topic, f,indent=2)
    
    #create the pie chart with full labels
    labels = ["Announcement","Restriction","Conspiracy","Politics","Personal Experience", "Personal Opinion", "No Context"]
    plt.pie(totals,labels=labels)
    plt.title("Percent Distribution of Tweets per Topic",fontsize=20)
    plt.savefig(os.path.join(parentdir,'data','piechart.png'))
    
    #provide the % per topic data for a table in the report
    percentages = dict.fromkeys(topics.keys(),0)
    for k,v in zip(topics.keys(),totals):
        val = v/999 * 100
        percentages[k] = ("%.2f" % val)
    
    with open(os.path.join(parentdir,'data','percentages_per_topic.json'), 'w') as f:
        json.dump(percentages, f,indent=2) 




if __name__ == "__main__":
    main()