# Machine Learning in the NFL - A Customer Segmentation Approach to NFL Quarterbacks

## Motivation
In 2016, the NFL took in $13 billion in revenue and is expected to clear $17 billion next year. The Super Bowl consistently draws more than 100 million viewers each year. Given this massive exposure, nearly every fan, whether casual or hardcore, can tell you that the most important position in football is the Quarterback position. Coaches know this. GMs know this. And even players admit this. With such a massive industry and common understanding for what it takes to succeed, it is shocking to me that teams are still not able to evaluate incoming rookie quarterbacks as well as current veterans. Since 1999, 12 teams have drafted 8 more QBs, almost 1 every 2 years. Some teams like the Patriots and Packers have found success, while many others have not just failed but continue to fail year after year; teams like the New York Jets, San Francisco 49ers, and Cleveland Browns.
 
 ## The Problem
 Currently there are two common ways that teams evaluate QBs:
 1. Watch previous game film and evaluate the traits of the QB. Traits include things such as: Arm strength, accuracy, footwork, etc.
 1. Statistics - Does a QB throw a lot of touchdowns or interceptions? How many yards do he throw in one game or season?
     
 To me, this felt like a problem. Take Tom Brady, for example. If you look at the statstics each week, you will find qbs with better or more attractive numbers. If you look at the game film you will find qbs with better attributes. Something must be missing. Are there certain places on the field that the best qbs throw to more? Are there certain scenarios where certain qbs play better than others?
 
 ## Goal - Setup - Data Source
 The goal for this project is to examine the play-by-play descriptions from every football game since 1994 and create a feature matrix based on the results of each play. Then from this scaled feature matrix, apply unsupervised learning techniques in order to group or cluster the qbs based on the results or outcomes of each play throught one season. The data will be from [Pro Football Reference](http://http://www.pro-football-reference.com/) as they provide a nice, consistent api for scraping the play-by-play tables.

![pbp](https://github.com/BradenJones5/galvanize_capstone/blob/master/pbp_snapshot.jpeg)
