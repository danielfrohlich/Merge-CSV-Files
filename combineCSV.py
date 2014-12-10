#!/usr/bin/env python

## these modules are for combining csv files
import pandas as pd
import glob
import re

## these modules are for the email
import smtplib
import email
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP

## SET THESE FIRST BEFORE RUNNING
## combineColumn is the column you want to combine in the list of files
## dateColumn is the column that includes all of your date values

combineColumn = "tlh"
dateColumn = "date"

## send email features, if you want to disable this functionality: set sendemail = "TRUE" to "FALSE"

sendemail = 'TRUE'
mail_user = 'ENTER YOUR MAIL USERNAME'
mail_password = 'ENTER YOUR MAIL PASSWORD'
mail_server = 'ENTER YOUR MAIL SERVER'
mail_from = mail_user + '@domain.com'
mail_to = ['email1', 'email2']

## obtain all files in directory

allFiles = glob.glob("*.csv")

## create empty dataframe and list for files

frame = pd.DataFrame()
list = []

## in general, this loop is set up to dump the contents of each file into the empty list we just set up. read more below for details.
## everything before the if statement exists solely to check if the file has the necessary columns, otherwise the file is ignored
## parse_dates turns everything in the date column into a common date format (if multiple formats exist across the files)
## the first df.rename renames the combineColumn to the filename so that you get unique column headers for each file
## the second df.rename removes the '.csv' from the end of the column name
## append adds the dataframe (df) to the empty list

for files in allFiles:
   df = pd.read_csv(files)
   if combineColumn in df.columns:
      df = pd.read_csv(''.join(files),index_col=0, header=0, parse_dates=[dateColumn])
      df = df.rename(columns = {combineColumn:files}) [[files]]
      df = df.rename(columns = {files:re.sub('\.csv$', '', files)})   
      list.append(df)

## concatenate the list into one dataframe

frame = pd.concat(list, axis=1)

## export dataframe to csv

frame.to_csv("output.csv")

## count the columns (files) and the number of missing values in each csv file. The missingValues variable has been turned into a string (str).

countFiles = len(frame.columns)
missingValues = str(frame.count(axis=0, numeric_only=False))


## the subject line, message, and attachment to include

Subject = 'ENTER YOUR SUBJECT LINE'
Message = 'View attached CSV file. It contains the contents of %s files. A row count for each file is listed below.' %countFiles
Message += '\n \n \n' + missingValues
fileAttachment = 'output.csv'

if(sendemail == 'TRUE'):
   msg = MIMEMultipart()
   msg['Subject'] = Subject
   msg['From'] = mail_from
   msg['To'] = ','.join(mail_to)
   msg.attach(MIMEText(Message))
   fp = open(fileAttachment)
   attachment = MIMEText(fp.read(), _subtype='text')
   fp.close()
   attachment.add_header('Content-Disposition', 'attachment', filename=fileAttachment)
   msg.attach(attachment)

   ## now send the email
   s = smtplib.SMTP(mail_server)
   s.ehlo()
   s.starttls()
   s.login(mail_user, mail_password)
   s.sendmail(mail_from, mail_to, msg.as_string())
   s.close

print Message
