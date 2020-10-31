# -*- coding: utf-8 -*-
"""sql-cookbook-r.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Y1n_FFTip76p2FpN2LpYQ6pXF-Sjg0By
"""

library(tidyverse); library(zoo); library(sqldf)

"""[SageMathCell Version](https://olgabelitskaya.github.io/sql_cookbook.html) & [SageMathCell Test Example](https://olgabelitskaya.github.io/sql_test.html)
## 📑 Creating SQL Databases
"""

if (!is.null(getOption("sqldf.connection"))) sqldf()
sqlite<-dbDriver("SQLite")
example<-dbConnect(sqlite,dbname="example.db")
for (df in c("projects","tasks","df1","df2",
             "tips","schooledu","nba")) {
    if (dbExistsTable(example,df)) {
        dbRemoveTable(example,df)}}
list.files(path="../input")

"""## 📑 Creating SQL Tables"""

st_ex<-function(str){
    st<-do.call(paste,c(as.list(str),sep=""))
    dbExecute(st,conn=example)}
cr_task<-function(str){
    st<-c("INSERT INTO tasks(name,priority,status_id,",
          "project_id,begin_date,end_date) VALUES",str)
    st<-do.call(paste,c(as.list(st),sep=""))
    dbExecute(st,conn=example)}

st1<-c("CREATE TABLE IF NOT EXISTS projects (",
       "id integer PRIMARY KEY, ",
       "name text NOT NULL, ",
       " begin_date text, ",
       " end_date text);")
st2<-c("CREATE TABLE IF NOT EXISTS tasks ( ",
       "id integer PRIMARY KEY, ",
       "name text NOT NULL, ",
       "priority integer, ",
       "status_id integer NOT NULL, ",
       "project_id integer NOT NULL, ",
       "begin_date text NOT NULL, ",
       "end_date text NOT NULL, ",
       "FOREIGN KEY (project_id) REFERENCES projects (id));")
st3<-c("INSERT INTO projects(name,begin_date,end_date) ",
       "VALUES('SQL CookBook with SageMathCell',",
       "'2020-02-04','2020-02-18');")
st4<-c("INSERT INTO projects(name,begin_date,end_date) ",
       "VALUES('SQL Tests','2020-01-31','2020-02-14');")
st5<-list("('Page 1',1,1,1,'2020-02-04','2020-02-12');",
          "('Page 2',1,1,1,'2020-02-10','2020-02-18');",
          "('Test 1',1,1,2,'2020-01-31','2020-02-01');",
          "('Test 2',1,1,2,'2020-02-02','2020-02-03');",
          "('Test 3',1,1,2,'2020-02-04','2020-02-05');",
          "('Test 4',1,1,2,'2020-02-06','2020-02-07');",
          "('Test 5',1,1,2,'2020-02-08','2020-02-09');",
          "('Test 6',1,1,2,'2020-02-09','2020-02-10');",
          "('Test 7',1,1,2,'2020-02-10','2020-02-11');",
          "('Dublicate',1,1,2,'2020-02-11','2020-02-14')")
for (st in list(st1,st2,st3,st4)) {st_ex(st)}
for (st in st5) {cr_task(st)}

"""## 📑 Creating DataFrames"""

df1<-data.frame(key1=c('A','B','C','D','F','F'),
                value1=sample(1:10,6))
df2<-data.frame(key2=c('B','D','D','E','F'),
                value2=sample(1:10,5))
df1; df2

path1<-paste0('https://raw.github.com/pydata/pandas/',
              'master/pandas/tests/data/')
tips<-read.csv(paste0(path1,'tips.csv'))

path2<-'../input/data-science-for-good/'
school_explorer<-read.csv(paste0(path2,'2016 School Explorer.csv'))

school_explorer<-school_explorer[,4:161]
school_explorer[school_explorer=="N/A"]<-NA
school_explorer$School.Name<-
as.character(school_explorer$School.Name)
school_explorer$School.Name[c(428,1024,713,909)]<- 
c('P.S. 212 D12','P.S. 212 D30','P.S. 253 D21','P.S. 253 D27')
school_explorer$School.Income.Estimate<-
as.character(school_explorer$School.Income.Estimate)
school_explorer$School.Income.Estimate<-
sub("\\$","",school_explorer$School.Income.Estimate)
school_explorer$School.Income.Estimate<-
sub(",","",school_explorer$School.Income.Estimate)
school_explorer$School.Income.Estimate<-
as.numeric(school_explorer$School.Income.Estimate)
school_explorer$School.Income.Estimate<-
na.approx(school_explorer$School.Income.Estimate)
percent_list<-c('Percent.ELL',
                'Percent.Asian','Percent.Black','Percent.Hispanic',
                'Percent.Black...Hispanic','Percent.White',
                'Student.Attendance.Rate',
                'Percent.of.Students.Chronically.Absent',
                'Rigorous.Instruction..','Collaborative.Teachers..',
                'Supportive.Environment..','Effective.School.Leadership..',
                'Strong.Family.Community.Ties..','Trust..')
target_list<-c("Average.ELA.Proficiency","Average.Math.Proficiency")
economic_list<-c("Economic.Need.Index","School.Income.Estimate")
rating_list<-c('Rigorous.Instruction.Rating','Collaborative.Teachers.Rating',
               'Supportive.Environment.Rating','Effective.School.Leadership.Rating',
               'Strong.Family.Community.Ties.Rating','Trust.Rating',
               'Student.Achievement.Rating')
nastr2num<-function(x){ x<-as.numeric(sub("%","",x)) }
for (el in c(percent_list,target_list,"Economic.Need.Index")) {
    school_explorer[el]<-sapply(school_explorer[el],nastr2num)
    school_explorer[el]<-na.approx(school_explorer[el]) }
for (el in rating_list) {
    vtable<-data.frame(table(school_explorer[el]))
    mvalue<-as.character(vtable$Var1[vtable$Freq==max(vtable$Freq)])
    school_explorer[el][is.na(school_explorer[el])]<-mvalue
    school_explorer[,el]<-factor(school_explorer[,el]) }
sum(is.na(school_explorer))

names(school_explorer)<-gsub("\\.","",names(school_explorer))
head(school_explorer)[1:10]

path3<-'../input/nba-all-star-game-20002016/'
fn3<-'NBA All Stars 2000-2016 - Sheet1.csv'
nba<-read.csv(paste0(path3,fn3))

"""## 📑 SQL Basic Queries"""

q<-paste0("SELECT * FROM projects,tasks ",
          "WHERE projects.id=tasks.project_id;")
sqldf(q,conn=example)

q<-"SELECT * from df1,df2;"
sqldf(q)

q<-c("SELECT * from df1,df2 ",
     "WHERE df1.key1=df2.key2 AND df1.value1>2 ",
     "ORDER BY key1 DESC;")
q<-do.call(paste,c(as.list(q),sep=""))
sqldf(q)

q<-paste0("SELECT total_bill,tip,smoker,time ",
          "FROM tips LIMIT 7;")
sqldf(q)

q<-paste0("SELECT * FROM tips ",
          "WHERE time='Dinner' LIMIT 3;")
sqldf(q)

q<-paste0("SELECT COUNT(LocationCode),TrustRating ",
          "FROM school_explorer GROUP BY TrustRating;")
sqldf(q)

q<-"PRAGMA table_info('nba');"
sqldf(q)

q<-"SELECT DISTINCT Team FROM nba WHERE Year=2014;"
sqldf(q)

"""## 📑 Closing the Connection"""

sqldf("SELECT * from sqlite_master;",
       conn=example)

dbDisconnect(example)
dbUnloadDriver(sqlite)
file.remove("example.db")