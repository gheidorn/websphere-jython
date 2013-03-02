# environment-specific variables
nodeName="CARS-GHEIDORNNode01"
serverName="server1"

busName = "syco.bus"

def deleteCF(jmsCFName):
    #--------------------------------------------------------------------
    # Retrieve specific Object ID and remove Connection Factory using ID
    #--------------------------------------------------------------------
    jmsCF = AdminConfig.getid('/Server:%s/J2CResourceAdapter:SIB JMS Resource Adapter/J2CConnectionFactory:%s' % (serverName,jmsCFName))
    if(jmsCF != ""):
        AdminConfig.remove(jmsCF)
        print "  deleted connection factory %s" % jmsCFName
    else:
        print "  connection factory %s not found" % jmsCFName
    #endElse
#endDef

def deleteQueue(qName):
    #--------------------------------------------------------------------
    # Search for queue based on scope and delete
    #--------------------------------------------------------------------
    for queue in AdminTask.listSIBJMSQueues(scope).splitlines():
        name = AdminConfig.showAttribute(queue, "name")
        if (name == qName):
            AdminTask.deleteSIBJMSQueue(queue)
            print "  deleted queue %s" % qName
            return
        #endIf
    #endFor
    print "  queue %s not found" % qName
#endDef

def deleteAS(jmsASName):
    #--------------------------------------------------------------------
    # Retrieve specific Resource Adapter Type ID for SIB JMS Resource Adapter
    #--------------------------------------------------------------------
    ra = AdminConfig.getid('/Server:%s/J2CResourceAdapter:SIB JMS Resource Adapter' % serverName)

    #--------------------------------------------------------------------
    # Remove the Activation Spec found in the SIB JMS Resource Adapter
    #--------------------------------------------------------------------
    for spec in AdminTask.listJ2CActivationSpecs(ra, ["-messageListenerType", "javax.jms.MessageListener"]).splitlines():
        name = AdminConfig.showAttribute(spec, "name")
        if (name == jmsASName):
            AdminConfig.remove(spec)
            print "  deleted activation spec %s" % jmsASName
            return
        #endIf
    #endFor
    print "  activation spec %s not found" % jmsASName
#endDef

def deleteBus(busName):
    for bus in AdminTask.listSIBuses().splitlines():
        name = AdminConfig.showAttribute(bus, "name")
        if (name == busName):
            params = ["-bus", busName]
            AdminTask.deleteSIBus(params)
            print "  deleted bus %s" % busName
            return
        #endIf
    #endFor
    print "  bus %s not found" % busName
#enddef


#
#    runtime
#

print ""
print "This script has the following targets defined:"
print "Node: %s" % nodeName
print "Server: %s" % serverName
print ""

scope = AdminConfig.getid('/Node:%s/Server:%s' % (nodeName, serverName))

prefixName = "SYCO"

eventQName = "%s_EventQ" % prefixName
submittedAdQName = "%s_SubmittedAdQ" % prefixName
cfName = "%s_CF" % prefixName

print "Deleting queue %s..." % eventQName    
deleteQueue(eventQName)

print "Deleting queue %s..." % submittedAdQName
deleteQueue(submittedAdQName)

print "Deleting connection factory %s..." % cfName
deleteCF(cfName)

#print "Deleting activation specification %s..." % activSpecName
#deleteAS(activSpecName)

print "Delete service integration bus %s" % busName
deleteBus(busName)

print "Saving..."
AdminConfig.save()

print ""
print "Resources deleted, configuration saved"
print "Please restart the application server to finalize changes"