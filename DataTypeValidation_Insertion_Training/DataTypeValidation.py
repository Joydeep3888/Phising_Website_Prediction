import shutil
import sqlite3
from datetime import datetime
from os import listdir
import os
import csv
from Logging.Logging import logger
from Training_Raw_data_validation.rawValidation import Raw_Data_Validation
import json


class dBOperation:
    """
      This class shall be used for handling all the SQL operations.

      Written By: Joydeep Ghosh
      Version: 1.0
      Revisions: None

      """
    def __init__(self):
        self.path = r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Training_Batch_Files/'
        self.badFilePath = r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Training_Raw_files_validated/Bad_Raw'
        self.goodFilePath = r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Training_Raw_files_validated/Good_Raw'
        self.log = logger()
        self.schema_path='C:/Users/hp/OneDrive/Desktop/ineuron/Phising_Website_Prediction/schema_training.json'
        with open(self.schema_path, 'r+') as f:
            dic = json.load(f)
            f.close()
        self.column_names = dic['ColName']
        self.path_log=r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\General_Logging/DB_Logs.log'

    def dataBaseConnection(self,DatabaseName):

        """
                Method Name: dataBaseConnection
                Description: This method creates the database with the given name and if Database already exists then opens the connection to the DB.
                Output: Connection to the DB
                On Failure: Raise ConnectionError

                 Written By: Joydeep Ghosh
                Version: 1.0
                Revisions: None

                """
        try:
            conn = sqlite3.connect(self.path+DatabaseName+'.db')

            file = open(self.path_log, 'a+')
            self.log.apply_log(file, "Opened %s database successfully" %DatabaseName)
            file.close()
        except ConnectionError:
            file = open(self.path_log, 'a+')
            self.log.apply_log(file, "Error while connecting to database: %s" %ConnectionError)
            file.close()
            raise ConnectionError
        return conn

    def createTableDb(self,DatabaseName):
        """
                        Method Name: createTableDb
                        Description: This method creates a table in the given database which will be used to insert the Good data after raw data validation.
                        Output: None
                        On Failure: Raise Exception

                         Written By: Joydeep Ghosh
                        Version: 1.0
                        Revisions: None

                        """
        try:
            conn = self.dataBaseConnection(DatabaseName)
            c=conn.cursor()
            c.execute("SELECT count(name)  FROM sqlite_master WHERE type = 'table'AND name = 'Good_Raw_Data'")
            if c.fetchone()[0] ==1:
                conn.close()
                file = open(self.path_log, 'a+')
                self.log.apply_log(file, "Tables exists already!!")
                file.close()

                file = open(self.path_log, 'a+')
                self.log.apply_log(file, "Closed %s database successfully" % DatabaseName)
                file.close()

            else:

                for key in self.column_names.keys():
                    type = self.column_names[key]

                    try:
                        conn.execute('ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,dataType=type))
                    except:
                        conn.execute('CREATE TABLE  Good_Raw_Data ({column_name} {dataType})'.format(column_name=key, dataType=type))
                conn.close()

                file = open(self.path_log, 'a+')
                self.log.apply_log(file, "Tables created successfully!!")
                file.close()

                file = open(self.path_log, 'a+')
                self.log.apply_log(file, "Closed %s database successfully" % DatabaseName)
                file.close()

        except Exception as e:
            file = open(self.path_log, 'a+')
            self.log.apply_log(file, "Error while creating table: %s " % e)
            file.close()
            conn.close()
            file = open(self.path_log, 'a+')
            self.log.apply_log(file, "Closed %s database successfully" % DatabaseName)
            file.close()
            raise e


    def insertIntoTableGoodData(self,Database):

        """
                               Method Name: insertIntoTableGoodData
                               Description: This method inserts the Good data files from the Good_Raw folder into the
                                            above created table.
                               Output: None
                               On Failure: Raise Exception

                                Written By: Joydeep Ghosh
                               Version: 1.0
                               Revisions: None

        """

        conn = self.dataBaseConnection(Database)
        goodFilePath= self.goodFilePath
        badFilePath = self.badFilePath
        onlyfiles = [f for f in listdir(goodFilePath)]
        file = open(self.path_log, 'a+')

        for file in onlyfiles:
            try:
                with open(goodFilePath+ '/' + file,"r") as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    # print(type(reader))
                    for line in enumerate(reader):
                        # print(line)
                        for list_ in (line[1]):
                            #print(list_)
                            try:
                                conn.execute('INSERT INTO Good_Raw_Data values ({values})'.format(values=(list_)))
                                file=open(self.path_log, 'a+')
                                self.log.apply_log(file," %s: File loaded successfully!!" % file)
                                conn.commit()
                                file.close()
                            except Exception as e:
                                raise e

            except Exception as e:

                conn.rollback()
                file = open(self.path_log, 'a+')
                self.log.apply_log(file,"Error while creating table: %s " % e)
                file.close()
                shutil.move(goodFilePath+'/' + file, badFilePath)
                file = open(self.path_log, 'a+')
                self.log.apply_log(file, "File Moved Successfully %s" % file)
                file.close()
                conn.close()

        conn.close()
        file.close()


    def selectingDatafromtableintocsv(self,Database):

        """
                               Method Name: selectingDatafromtableintocsv
                               Description: This method exports the data in GoodData table as a CSV file. in a given location.
                                            above created .
                               Output: None
                               On Failure: Raise Exception

                                Written By: Joydeep Ghosh
                               Version: 1.0
                               Revisions: None

        """

        self.fileFromDb = r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Training_File_from_DB/'
        self.fileName = 'InputFile.csv'
        file = open(self.path_log, 'a+')
        try:
            conn = self.dataBaseConnection(Database)
            sqlSelect = "SELECT *  FROM Good_Raw_Data"
            c = conn.cursor()

            c.execute(sqlSelect)

            results = c.fetchall()
            # Get the headers of the csv file
            headers = [i[0] for i in c.description]

            #Make the CSV ouput directory
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            # This will going to open CSV file for writing.
            csvFile = csv.writer(open(self.fileFromDb + self.fileName, 'w', newline=''),delimiter=',', lineterminator='\r\n',quoting=csv.QUOTE_ALL, escapechar='\\')

            # writerow writes just one single rows
            #writerows write mutiple rows, hence to add heading i have used writerow and to write
            #results i have used writerows
            csvFile.writerow(headers)
            csvFile.writerows(results)

            self.log.apply_log(file, "File exported successfully into csv")
            file.close()

        except Exception as e:
            self.logger.log(file, str(e))
            file.close()

print('sucessful completion of DataTypeValidation.py')





