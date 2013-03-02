# environment-specific variables
nodeName="CARS-GHEIDORNNode01"
serverName="server1"
providerEndpointPort = "7280"
providerEndpointHost = "localhost"

# resource-specific variables
busName = "syco.bus"
scope = AdminConfig.getid('/Node:%s/Server:%s' % (nodeName, serverName))

def createJMSQParams(name, description):
    jndiName = "jms/%s" % name
    params = ["-name", name, "-jndiName", jndiName, "-description", description, "-queueName", name]
    return params
#enddef

def createSIBQParams(name):
    params = ["-bus", busName, "-name", name, "-type", "Queue", "-node", nodeName, "-server", serverName]
    return params
#enddef

def createASParams(name, destinationQName):
    jndiName = "jms/%s" % name
    destQJNDI = "jms/%s" % destinationQName
    params = ["-name", name, "-jndiName", jndiName, "-busName", busName, "-destinationJndiName", destQJNDI, "-destinationType", "Queue"]
    return params
#enddef

#
# Runtime
#
print ""
print "NOTE: this script only needs to be run once. If target resources already exist this script will fail. If the server is not started this script will fail."
print ""
print ""
print "This script has the following targets defined:"
print "Node: %s" % nodeName
print "Server: %s" % serverName
print ""

# Create the bus
print "Creating Service Integration Bus %s..." % busName
AdminTask.createSIBus(["-bus", busName, "-description", "Messaging bus for SYCO Ad Engine", "-secure", "FALSE"])

# Add server as a bus member
print "Adding server Node:%s/Server:%s as bus member" % (nodeName, serverName)
print "If an error occurs here, make sure the right nodeName and serverName values are defined in this script"
AdminTask.addSIBusMember(["-bus", busName, "-node", nodeName, "-server", serverName])
print "  Node:%s/Server:%s added to bus %s" % (nodeName, serverName, busName)

prefixName = "SYCO"

# JMS resource WAS names
eventQName = "%s_EventQ" % prefixName
submittedAdQName = "%s_SubmittedAdQ" % prefixName
cfName = "%s_CF" % prefixName
#activSpecName = "%s_AS" % prefixName

# JMS resource descriptions
eventQDesc = "queue for SYCO events"
submittedAdQDesc = "queue for Ads submitted to the SYCO Ad Engine"
cfDesc = "Connection factory for SYCO"

# Collect WAS resource parameters
eventQParams = createJMSQParams(eventQName, eventQDesc)
submittedAdQParams = createJMSQParams(submittedAdQName, submittedAdQDesc)
#activSpecParams = createASParams(activSpecName, requestQName)
    
cfEndProvider = providerEndpointHost + ":" + providerEndpointPort + ":" + "BootstrapBasicMessaging"
cfParams = ["-name", cfName, "-jndiName", "jms/%s"%cfName, "-busName", busName, "-description", cfDesc, "-type", "queue", "-providerEndPoints", cfEndProvider]

# Collect bus destination resource parameters
eventQDestParams = createSIBQParams(eventQName)
submittedAdQDestParams = createSIBQParams(submittedAdQName)

# Create SIB queues
print "Creating SIB Queues ..."
print "  destination %s" % eventQName
AdminTask.createSIBDestination(eventQDestParams)
print "  destination %s" % submittedAdQName
AdminTask.createSIBDestination(submittedAdQDestParams)

# Create WAS JMS queues
print "Creating JMS queues..."
print "  queue %s" % eventQName
AdminTask.createSIBJMSQueue(scope, eventQParams)
print "  queue %s" % submittedAdQName
AdminTask.createSIBJMSQueue(scope, submittedAdQParams)

# Create connection factory
print "Creating connection factory %s..." % cfName
AdminTask.createSIBJMSConnectionFactory(scope, cfParams)

# Create activation specs
#print "Creating activation specification %s..." % activSpecName
#AdminTask.createSIBJMSActivationSpec(scope, activSpecParams)

print "Saving..."
AdminConfig.save()

print "Resources created, configuration saved"
print "Please restart the application server to make resources available"