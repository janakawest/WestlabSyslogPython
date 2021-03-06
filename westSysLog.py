#!/usr/bin/python2.7

'''
Implementing a Syslog wrapper for Westlab
This has been implemented based on following resources
RFC5424 				: https://tools.ietf.org/html/rfc5424
syslog man page	: https://linux.die.net/man[C/3/openlog
'''

import logging
import syslog

class WestlabSyslogStream (logging.Handler):
	logPriorities = {'emergency':'syslog.LOG_EMERG', 'alert':'syslog.LOG_ALERT', 'critical':'syslog.LOG_CRIT', 'error':'syslog.LOG_ERR', 'warning':'syslog.LOG_WARNING', 'notice':'syslog.LOG_NOTICE', 'info':'syslog.LOG_INFO', 'debug':'syslog.LOG_DEBUG'}

	logFacilities = {'auth':syslog.LOG_AUTH, 'cron':syslog.LOG_CRON, 'log_daemon':syslog.LOG_DAEMON, 'ftp':syslog.LOG_KERN,	'local0':syslog.LOG_LOCAL0, 'local1':syslog.LOG_LOCAL1,	'local2':syslog.LOG_LOCAL2, 'local3':syslog.LOG_LOCAL3,	'local4':syslog.LOG_LOCAL4,'local5':syslog.LOG_LOCAL5,'local6':syslog.LOG_LOCAL6,'local7':syslog.LOG_LOCAL7,'lpr':syslog.LOG_LPR,'mail':syslog.LOG_MAIL,'news':syslog.LOG_NEWS,'wsyslog':syslog.LOG_SYSLOG,'user':syslog.LOG_USER,'uucp':syslog.LOG_UUCP}

	# This region is for define variables
	n_logFacility = 'user' # default is set as LOG_USER
	n_logProperty = 'info' # Default is set as LOG_DEBUG

	def __init__ (self, lFacility, lPriority, programId):
		''' Constructor '''
		# Check for the parameters are correct
		if not lFacility in self.logFacilities:
			print ('Error! Check the ' + type(self).__name__ + ' Class for the supporting Syslog Facilities')
			exit ()
		if not lPriority in self.logPriorities:
			#print (Error! Check the ' + type(self).__name__ + ' Class for the supporting Syslog Priorities')
			exit ()
		self.n_logPriority = self.logPriorities[lPriority]
		self.n_logFacility = self.logFacilities[lFacility]

		# Now Try to open the Syslog
		try:
			syslog.openlog(logoption=syslog.LOG_PID, lgFac=self.logFacilities[lFacility])
		except Exception as err:
			try:
				syslog.openlog(syslog.LOG_PID, self.logFacilities[lFacility])
			except Exception as err:
				try:
					syslog.openlog('Westlab_Syslogger', syslog.LOG_PID, self.logFacilities[lFacility])
				except:
					raise

		# Get the logLeevel and the logFormat according to the logPriority passed by the user
		try:
			n_logLevel = ''
			n_logFormat = ''
			self.n_logLevel, self.n_logFormat = self.SetLogProperty (programId, self.GetLogPriority ())
		except Exception as err:
			print (err)
			raise

		# Initialize the Logging Handler
		logging.Handler.__init__ (self)
		# Setup the Logging Handler
		self.SetupLogger ()

	# Setup the logging handler and the related attributes
	def SetupLogger (self):
		# Configure the Logger
		westlabLogger = logging.getLogger ()
		westlabLogger.setLevel (self.GetLogLevel ())

		# Clear previous logs
		westlabLogger.handlers = []

		# Set the log format
		westlablLogFormatter = logging.Formatter (self.GetLogFormat ())

		# Add the handler
		westlabLogHandlers = []
		westlabLogHandlers.append (self)

		for h in westlabLogHandlers:
			h.setFormatter (westlablLogFormatter)
			westlabLogger.addHandler (h)
	
	#Return the log priority level
	def GetLogPriority (self):
		return self.n_logPriority

	#Return the log Facility level
	def GetLogFacility (self):
		return self.n_logFacility

	#Return the log level that syslog needs
	def GetLogLevel (self):
		return self.n_logLevel

	#Return the log format that syslog needs
	def GetLogFormat (self):
		return self.n_logFormat

	#defines the log level and the format as user neede
	def SetLogProperty(self, id, priority):
		LOG_ATTRIBUTE = []
		if priority == 'syslog.LOG_DEBUG':
			LOG_ATTRIBUTE = ((logging.DEBUG,
												id + ' %(levelname)-9s %(name)-15s %(threadName)-14s +%(lineno)-4d %(message)s'))
			return LOG_ATTRIBUTE
		elif priority == 'syslog.LOG_INFO':
			LOG_ATTRIBUTE = ((logging.INFO,
												id + ' %(levelname)-9s %(message)s'))
			return LOG_ATTRIBUTE
		elif priority == 'syslog.LOG_WARNING':
			LOG_ATTRIBUTE = ((logging.INFO,
												id + ' %(levelname)-9s %(message)s'))
			return LOG_ATTRIBUTE
		elif priority == 'syslog.LOG_ERR':
			LOG_ATTRIBUTE = ((logging.INFO,
												id + ' %(levelname)-9s %(message)s'))
			return LOG_ATTRIBUTE
		elif priority == 'syslog.LOG_CRIT':
			LOG_ATTRIBUTE = ((logging.INFO,
												id + ' %(levelname)-9s %(message)s'))
			return LOG_ATTRIBUTE
		else:
			print ('The Log Priority:'+str(priority)+'is incorrect. Check the ' + type(self).__name__ + ' Class for the supporting Syslog Priorities')
			exit ()

	# Output the given message to SYSLOG.
	# Determines the message ID, event category and event type, and then logs the message in the NT event log.
	# For more information please refer https://docs.python.org/3/library/logging.handlers.html
	def emit (self, record):
		syslog.syslog(self.format(record))

	def close (self):
		syslog.closelog ()
	def WriteToLog (self, message):
		syslog.syslog (message)


'''
Following is a test class case implemented to test the WestlabSyslogStream class
Note: you have to copy "westSysLog.py" into /usr/lib64/<python version>/site-packages/ directory
Then you can import the class as given in the following example

#!/usr/bin/python2.7
import westSysLog
import logging
import syslog

#Test case for Westlab Syslog class

if __name__ == '__main__':
	# Main method implemented for testing purposes
  # Create an instance of the WestlabSyslogStream class and pass necessary arguments
  westSysLog.WestlabSyslogStream ('user', 'debug', __file__)

  # Write to the syslog
  logging.debug ('debug message')
  logging.info('info')
  logging.warning('warning')
  logging.error('error')
  logging.critical('critical')
'''
