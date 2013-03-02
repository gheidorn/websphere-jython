#   Usage:  ./wsadmin.sh -lang jython [-port # -username u -password p] -f checkTraceServiceSettings.py
#   
#   The wsadmin.sh defaults to dmgr port.  If this is not desired, you need to find the SOAP_CONNECTOR port in the 
#   serverindex.xml file of the server you want to administer.  Credentials are only required if you are running from
#   an account without appropriate WAS console access.
#
#   @version 1.0 - Greg Heidorn - 01/11/2013    Initial script.

global AdminConfig

def generateTraceServiceSettings():
    print("\nPreparing AdminConfig 'TraceService' objects for display...")
    traceSvcObjs = AdminConfig.list('TraceService').split()
    for obj in traceSvcObjs:
        # context shows the server in question
        context = AdminConfig.showAttribute(obj, "context")

        # enable indicates whether the tracing is enabled or not
        enable = AdminConfig.showAttribute(obj, "enable")

        # memoryBufferSize is the number of thousands of entries to buffer
        # Not needed at this time; trace logs are written to files
        #memoryBufferSize = AdminConfig.showAttribute(obj, "memoryBufferSize")
        
        # properties: not sure of the extent of properties
        # Not needed at this time;
        #properties = AdminConfig.showAttribute(obj, "properties")
        
        # startupTraceSpecification indicates the level of tracing to perform
        # http://pic.dhe.ibm.com/infocenter/wasinfo/v6r1/index.jsp?topic=%2Fcom.ibm.websphere.express.doc%2Finfo%2Fexp%2Fae%2Frtrb_enabletrc.html
        startupTraceSpecification = AdminConfig.showAttribute(obj, "startupTraceSpecification")
        
        # traceFormat
        traceFormat = AdminConfig.showAttribute(obj, "traceFormat")
        
        # traceLog
        # Not needed at this time
        #traceLog = AdminConfig.showAttribute(obj, "traceLog")

        # traceOutputType
        # Not needed at this time
        #traceOutputType = AdminConfig.showAttribute(obj, "traceOutputType")

        # output settings to console
        print(context[0:context.find("(")].replace("\"", "") + ' : ' + enable.replace("\"", "") + ', ' + startupTraceSpecification + ', ' + traceFormat)
        #print('\"' + context[0:context.find("(")] + '" : enable="' + enable + '", startupTraceSpecification="' + startupTraceSpecification + '", traceFormat="' + traceFormat + '", traceLog="' + traceLog + '", trace="' + traceOutputType + '")')

generateTraceServiceSettings()