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
