import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import os, sys
import json
parentdir = Path(__file__).resolve().parents[1]
sys.path.append(parentdir)
data_path = os.path.join(parentdir,'data')
sys.path.append(data_path)

def createsinglebarplot(filename,x,y,color,legend,labelx,labely,title):
    #create a bar plot with multiple bars
    ind = np.arange(len(x))
    width = np.min(np.diff(ind))/3
    plt.figure(figsize=(10,5))
    p = plt.bar(ind, y, width, color=color,label=legend) 
    plt.xticks(ind + width/ 2, x)
    plt.title(title)
    plt.xlabel(labelx, fontsize=14)
    plt.ylabel(labely, fontsize=14)
    plt.legend(loc='best')
    plt.show()
    #plt.savefig(os.path.join(data_path,filename))
def createtwobarplot(filename,x,y1,y2,color1,color2,legend1,legend2,labelx,labely,title):
    #create a bar plot with multiple bars
    ind = np.arange(len(x))
    width = np.min(np.diff(ind))/3
    plt.figure(figsize=(10,5))
    p1 = plt.bar(ind, y1, width, color=color1,label=legend1) 
    p2 = plt.bar(ind + width, y2, width, color=color2,label=legend2)
    plt.xticks(ind + width/ 2, x)
    plt.title(title)
    plt.xlabel(labelx, fontsize=14)
    plt.ylabel(labely, fontsize=14)
    plt.legend(loc='best')
    plt.savefig(os.path.join(data_path,filename))
def createtriplebarplot(filename,x,y1,y2,y3,color1,color2,color3,legend1,legend2,legend3,labelx,labely,title):
    #create a bar plot with multiple bars
    ind = np.arange(len(x))
    width = np.min(np.diff(ind))/4
    plt.figure(figsize=(10,5))
    p1 = plt.bar(ind - width, y1, width, color=color1,label=legend1)
    p2 = plt.bar(ind, y2, width, color=color2,label=legend2) 
    p3 = plt.bar(ind + width, y3, width, color=color3,label=legend3)
    plt.xticks(ind + width/ 4, x)
    plt.title(title)
    plt.xlabel(labelx, fontsize=14)
    plt.ylabel(labely, fontsize=14)
    plt.legend(loc='best')
    plt.savefig(os.path.join(data_path,filename))

def main():
    #load the provided json file
    with open(os.path.join(data_path,'avg_retweets_fav.json'), 'r') as f:
        data1 = json.load(f)
    with open(os.path.join(data_path,'avg_retweets_fav_sent.json'), 'r') as f:
        data2 = json.load(f)
    topics = ["a","r","c","p","e","o","nc"]
    indices = [0,1,4,5]
    avg_rt1,avg_fav1 = [],[]
    p_avg_rt,n_avg_rt,nu_avg_rt = [],[],[]
    p_avg_fav,n_avg_fav,nu_avg_fav = [],[],[]
    #append the related fields to their corresponding lists
    for t in topics:
        avg_rt1.append(data1[t]["avg_rt"])
        avg_fav1.append(data1[t]["avg_fav"])
        p_avg_rt.append(data2[t]["p"]["avg_rt"])
        n_avg_rt.append(data2[t]["n"]["avg_rt"])
        nu_avg_rt.append(data2[t]["nu"]["avg_rt"])
        p_avg_fav.append(data2[t]["p"]["avg_fav"])
        n_avg_fav.append(data2[t]["n"]["avg_fav"])
        nu_avg_fav.append(data2[t]["nu"]["avg_fav"])
    
    trim_topics = [topics[x] for x in indices]
    trim_p_avg_rt = [p_avg_rt[x] for x in indices]
    trim_n_avg_rt = [n_avg_rt[x] for x in indices]
    trim_nu_avg_rt = [nu_avg_rt[x] for x in indices]

    trim_p_avg_fav = [p_avg_fav[x] for x in indices]
    trim_n_avg_fav = [n_avg_fav[x] for x in indices]
    trim_nu_avg_fav = [nu_avg_fav[x] for x in indices]

    
    createtwobarplot("avg_rt_fv.png",topics,avg_rt1,avg_fav1,"b","crimson","Retweets","Favorites","Topics","Average Retweets and Favorites","Average Retweets and Favorites per Topic")
    createtriplebarplot("avg_rt_sentiment.png",trim_topics,trim_n_avg_rt,trim_nu_avg_rt,trim_p_avg_rt,"firebrick","cadetblue","limegreen","Negative","Neutral","Positive","Topics","Average Retweets","Average Retweets for Each Sentiment per Topic")
    createtriplebarplot("avg_fav_sentiment.png",trim_topics,trim_n_avg_fav,trim_nu_avg_fav,trim_p_avg_fav,"firebrick","cadetblue","limegreen","Negative","Neutral","Positive","Topics","Average Favorites","Average Favorites for Each Sentiment per Topic")



if __name__ == "__main__":
    main()
