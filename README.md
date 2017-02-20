# WestlabSyslogPython
A python wrapper for Westlab Syslog

Implementing a Syslog wrapper for Westlab
This has been implemented based on following resources
RFC5424         : https://tools.ietf.org/html/rfc5424
syslog man page : https://linux.die.net/man[C/3/openlog

## Usage
```python
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
  logging.debug ('Debug')
  logging.info('Info')
  logging.warning('A Warning')
  logging.error('An error')
  logging.critical('A Critical Message')
```


