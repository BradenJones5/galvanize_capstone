# Machine Learning in the NFL - A Customer Segmentation Approach to NFL Quarterbacks

## Motivation
In 2016, the NFL took in $13 billion in revenue and is expected to clear $17 billion next year. The Super Bowl consistently draws more than 100 million viewers each year. Given this massive exposure, nearly every fan, whether casual or hardcore, can tell you that the most important position in football is the Quarterback position. Coaches know this. GMs know this. And even players admit this. With such a massive industry and common understanding for what it takes to succeed, it is shocking to me that teams are still not able to evaluate incoming rookie quarterbacks as well as current veterans. Since 1999, 12 teams have drafted 8 more QBs, almost 1 every 2 years. Some teams like the Patriots and Packers have found success, while many others have not just failed but continue to fail year after year; teams like the New York Jets, San Francisco 49ers, and Cleveland Browns.
 
 ## The Problem
 Currently there are two common ways that teams evaluate QBs:
 1. Watch previous game film and evaluate the traits of the QB. Traits include things such as: Arm strength, accuracy, footwork, etc.
 1. Statistics - Does a QB throw a lot of touchdowns or interceptions? How many yards do he throw in one game or season?
     
 To me, this felt like a problem. Take Tom Brady, for example. If you look at the statstics each week, you will find qbs with better or more attractive numbers. If you look at the game film you will find qbs with better attributes. Something must be missing. Are there certain places on the field that the best qbs throw to more? Are there certain scenarios where certain qbs play better than others?
 
 ## Goal - Setup - Data Source
 The goal for this project is to examine the play-by-play descriptions from every football game since 1994 and create a feature matrix based on the results of each play. Then from this scaled feature matrix, apply unsupervised learning techniques in order to group or cluster the qbs based on the results or outcomes of each play throught one season. 
 
 The data will be from [Pro Football Reference](http://http://www.pro-football-reference.com/) as they provide a nice, consistent api for scraping the play-by-play tables.
 
 ## Data Collection and Processing
 Tools Used:
* BeautifulSoup
* Urllib2
* Requests
* Re 
* Pandas
* AWS
* MongoDB
* tmux

I built a webcrawler that would scrape the play-by-play tables (see example image below) for every game dating back to 1994. After running the crawler on an EC2 instance, I stored the data and scraped html files into a MongoDB database. After the crawler finished, I exported the more than 1 million scraped plays into a .csv file and secure copied this file back to my local machine for processing using Python's Pandas package.

## Feature Engineering
The starting point for my project was to see if I could use machine learning to group quarterbacks based on their passing tendencies. Using Pandas, I created new columns that flagged for specific characteristics in each play. For example, if Peyton Manning threw a pass that was completed short and to the right, a 1 would be flagged under the feature 'short_right_complete'. After obtaining these frequency counts for each play, I then grouped by player name and year, and this resulted in my feature matrix after subsetting for only qbs that threw more than 300 passes (roughly 6 games) in a season. 

Features Created:
* Passes completed for short yardage to the left, middle, and right sections of the field
* Passes complete for deep yardage to the left, middle, and right sections of the field

The example transformation can be seen below (some features removed for spacing).
![pbp](https://github.com/BradenJones5/galvanize_capstone/blob/master/pbp_snapshot.jpeg)

Resulting dataframe:

| QB Name | Year | Short Right Complete | Short left Complete | Deep Right Complete | Deep Left Complete |
| ------- | ---- | -------------------- | ------------------- | ------------------- | ------------------ |
| Marcus Mariota | 2016 | 150 | 98 | 30 | 26 |
| Shaun Hill | 2016 | 138 | 78 | 24 | 18 |
| Tom Brady | 2015 | 162 | 100 | 17 | 20 |
| Peyton Manning | 2012 | 150 | 100 | 27 | 23 |
| Carson Wentz | 2016 | 147 | 98 | 23 | 17 |
| Aaron Rodgers | 2013 | 137 | 80 | 22 | 40 |
| Aaron Rodgers | 2014 | 152 | 78 | 34 | 28 |
| Aaron Rodgers | 2015 | 133 | 84 | 41 | 30 |
| Alex Smith | 2013 | 120 | 77 | 32 | 29 |

## Model
After creating my feature matrix I then scaled my features based on the number of pass attempts each quarterback threw that year. Given, that each QB is going to throw a different number of passes I used this type of scaling over the traditional standardScaler in sklearn, which substracts by the mean and divides by the standard deviation.

The next step was to cluster my features and explore the groupings visualy against the principal components. After exploring various clustering algorithms, I decided that initializing kmeans with kmeans++ and 4 clusters, was the best fit for my data. Given that short, deep, left, right are the most common features this made the most sense to me.
![clusters](https://github.com/BradenJones5/galvanize_capstone/blob/master/base_cluster.png)

Now that I had my groupings, I wanted to explore the variations between the groupings and to do this I looked at the centroids from my clustering model. One thing I noticed overall, quarterbacks tend to favor throwing towards their strong arm (for example, if they are right-handed they tend to throw to the right side of the field). Although, some really great quarterbacks break that trend and do better better than most throwing to the opposite side of the field. Here is the analysis from those clusters:

**"West Coast"** - Theses quarterbacks have much more success throwing to the short left and right (most successful) side of the field. Avoid/not succcesful throwing to the middle of the field. Named "west coast" because many west coast offense quarterbacks fall into this grouping such as Alex Smith, Sam Bradford, Russell Wilson.

**"Gunslingers"** - These quarterbacks have the most success throwing deep down the field, especially to the middle and right sides of the field. Quarterbacks in this group include Matt Ryan and Ben Roethlisberger.

**"Lefties"** - These quarterbacks have the most success throwing to the left side of the field (both short and deep). Quarterbacks in this group are successful left-handed quarterbacks. One interesting note, Peyton Manning (right-handed) appears in this group for 8 seasons and I feel its interesting enough to explore deeper. My inital hypothesis, is that their offense uses a lot of misdirection and Peyton is comfortable enough to turn and throw to the opposite side of the field.

**"Balanced"** - These quarterbacks distribute the ball much more evenly across all quadrants of the field, signaling very good field vision and ability to go through progressions. Most of the higher level pocket passers fit in this category. Quarterbacks such as Philip Rivers, Carson Palmer, and Andrew Luck.

## 2016 Quarterback Network
The next thing I wanted to explore from my data was given these passing tendencies for each quadrant of the field which quarterbacks are the most similar. 

I computed a similarity matrix based on a L1 distance metric and used this to build a network graph with graphx of the quarterbacks that played the majority of the 2016 season.

![qb graph](https://github.com/BradenJones5/galvanize_capstone/blob/master/2016_qb_graph.png)

What is interesting is that if you look at the node with the most edges(#22), this represents Philip Rivers. This is interesting because Philip Rivers is often known as the model pocket passer in today's NFL. Diving deeper we see his connected neighbors as Carson Palmer, Andrew Luck, Jameis Winston. Furthermore, all of these quarterbacks were clustered in my model's "Balanced" group, a group I defined to have good field vision and can go through their progressions.. Interesting enough, I looked up some old scouting reports of all 4 of these quarterbacks and they were identified by professional scouts as having good field vision and possessing the ability to throw the ball to all parts of the field.

## For the Future
Since my data has access to which down the play occured and which quarter. I would like to explore these quarterback tendencies in different scenarios. For example, where do the top quarterbacks like to throw the ball on 3rd and 4th down? Same thing for late in games and seasons (high pressure scenarios)? If successful I am confident that we might be starting to be able to connect "clutch" quarterbacks to certain tendencies.

I would like to also build a web app that allows users to enter a qb name, and quickly return a few qbs that are most similar according to my various models.



