import arcpy, sys, string, os, time, datetime, shutil, traceback


#LogFile class developed by Warren Kunkler to reduce repeating lines ofcode to generate log file.
#Use this to create an object of class LogFile 


#our class LogFile
class LogFile_Class:
    #member variables which are declared and initialized to default values
    timeYearMonDay = datetime.date.today()
    timeHour = time.localtime()[3]
    timeMin = time.localtime()[4]
    name = ''
    logpath = ''
    ws = ''
    #our constructor which initisializes the object and establishes the logfile object, uses composition to generate the file object
    def __init__(self, logpath, name, ws):
        LogFile_Class.ws = ws
        LogFile_Class.logpath = logpath
        LogFile_Class.name = name
        LogFile_Class._outfile = open(LogFile_Class.logpath + '\\' + LogFile_Class.name + '.log', 'a')
        LogFile_Class._outfile.write('\n' + LogFile_Class.ws  + '\n' + LogFile_Class.name + " ----------------------------------------" '\n')
        
    #our appendStartStatus method which takes a reference to a feature or raster layer during geoprocessing, appends the data to the log file
    def appendStartStatus(self, lyr):
        LogFile_Class._outfile = open(LogFile_Class.logpath + '\\' + LogFile_Class.name + '.log', 'a')
        LogFile_Class._outfile.write(lyr + " " + str(LogFile_Class.timeYearMonDay) +  " " + str(LogFile_Class.timeHour)+ ":"   + str(LogFile_Class.timeMin) +  '\n')


    #our failedStatus method which takes an ESRI arcgis error message and a reference to a feature or raster layer during geoprocessing
    #appends the data to the log file
    def failedStatus(self, ouch, lyr):
        print "Process: Failed for: " + lyr
        print ouch
        LogFile_Class._outfile.write(ouch + '\n')
        LogFile_Class._outfile.write("Process: Failed for: " + lyr + " " + str(LogFile_Class.timeYearMonDay) +  " " + str(LogFile_Class.timeHour)+ ":"   + str(LogFile_Class.timeMin) +  '\n' )


    #our closeFile method, closes the resources used to maintain an open I/O connection to our outfile object
    def closeFile(self):
        LogFile_Class._outfile.close()

    #our getEndTime method which prints the success message and appends the time to our outfile object and then closes the connection when finished
    def getEndTime(self):
        print "Process done! " + str(LogFile_Class.timeYearMonDay) +  " " + str(LogFile_Class.timeHour)+ ":"   + str(LogFile_Class.timeMin)
        LogFile_Class._outfile = open(LogFile_Class.logpath + '\\' + LogFile_Class.name + '.log','a')
        LogFile_Class._outfile.write("Process Complete "  + str(LogFile_Class.timeYearMonDay) +  " " + str(LogFile_Class.timeHour)+ ":"   + str(LogFile_Class.timeMin) +  '\n')
        LogFile_Class._outfile.close()

    def passMessage(self, mess):
        self._outfile.write(mess + '\n')
    
