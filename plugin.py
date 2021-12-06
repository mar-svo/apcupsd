"""
<plugin key="apcupsd" name="APC UPS" author="Maxim" version="2021.12.02">
    <params>
        <param field="Address" label="TCP: IP" width="140px" required="true" default="127.0.0.1"/>
        <param field="Port" label="TCP: Port" width="140px" required="true" default="3551"/>
        <param field="SerialPort" label="Debug mode" width="140px" required="true">
            <options>
                <option label="NO" value="0"/>
                <option label="YES" value="1"/>
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz
import os

class ApcUPSd:

    def onStart(self):

        self.uBCHARGE = 1
        self.uSTATUS = 2
        self.uTIMELEFT = 3

        if (Parameters["SerialPort"] == "1"):
            Domoticz.Debugging(1)
            DumpConfigToLog()
            Domoticz.Debug("***** NOTIFICATION: Debug is enabled!")
        else:
            Domoticz.Debugging(0)
        Domoticz.Debug("onStart called")

        Domoticz.Heartbeat(int(20)) # Device pollrate (heartbeat) : 20s

        self.TCP_IP = Parameters["Address"]
        self.TCP_PORT = Parameters["Port"]

        if self.uBCHARGE  not in Devices: Domoticz.Device(Unit=self.uBCHARGE,  DeviceID="BCHARGE",  Name="Battery charge", TypeName="Percentage", Used=1).Create()
        if self.uSTATUS   not in Devices: Domoticz.Device(Unit=self.uSTATUS,   DeviceID="STATUS",   Name="Status", Type=243, Subtype=22, Used=1).Create()
        if self.uTIMELEFT not in Devices: Domoticz.Device(Unit=self.uTIMELEFT, DeviceID="TIMELEFT", Name="Timeleft", Type=243, Subtype=33, Switchtype=3, Used=1).Create()

        return

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat called")

        Devices[self.uBCHARGE].Update(0, str(os.popen("apcaccess -h " + str(self.TCP_IP) + ":" + str(self.TCP_PORT) + " -p BCHARGE -u").read().strip()))
        Devices[self.uTIMELEFT].Update(0, str(os.popen("apcaccess -h " + str(self.TCP_IP) + ":" + str(self.TCP_PORT) + " -p TIMELEFT -u").read().strip()))

        STATUS = str(os.popen("apcaccess -h " + str(self.TCP_IP) + ":" + str(self.TCP_PORT) + " -p STATUS -u").read().strip())
        vSTATUS = 4
        if STATUS == "ONLINE": vSTATUS = 1
        elif STATUS == "CAL" or STATUS == "TRIM" or STATUS == "BOOST": vSTATUS = 2
        elif STATUS == "ONBATT": vSTATUS = 3
        Devices[self.uSTATUS].Update(vSTATUS, STATUS)

        return


global _plugin
_plugin = ApcUPSd()

def onStart():
    global _plugin
    _plugin.onStart()

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug("'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device ID='" + str(Devices[x].ID) + "', DeviceID='" + str(Devices[x].DeviceID) + "', Name='" + Devices[x].Name 
                       + "', nValue='" + str(Devices[x].nValue) + "', sValue='" + Devices[x].sValue + "', LastLevel='" + str(Devices[x].LastLevel) 
                       + "', Type='" + str(Devices[x].Type) + "', SubType='" + str(Devices[x].SubType) + "', SwitchType='" + str(Devices[x].SwitchType) + "'")
        
    return
