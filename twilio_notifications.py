
#This is a Python script to use as either standalone or as a template to monitor a single (or multiple)
#services on a Redhat\Fedora and send an SMS message via the Twilio service when an important service has gone down.
#This is intended to be run via a CRON job. 

import sys
import os
import subprocess
from twilio.rest import TwilioRestClient

#Global variables go here.

#Twilio Account Credentials
Account_Sid = "ACxxxxxxxxxxxxxxxxxxxxx"
Account_Token = "xxxxxxxxxxxxxxxxxxxx"

#Create a client which will be envoked to send the SMS messages or whatever you want to do with the Twilio API.
Client = TwilioRestClient(Account_Sid, Account_Token)

#The Twilio Number
Twilio_Number = "+1xxxxxxxxx"

#Make a simple dictionary to associate phone numbers to users so you can add or shrink as time goes on. 
Numbers = {'Jason': '+1xxxxxxxxx',}

#Shell Commands

checkdsclient = "service dsclient status | grep -oP '(running)"

#For CentOS 6.5 status 
"""service dsclient status | grep -oP '(running)'"""



#Global Functions

#Run a subprocess command to see if your service is running or not. If it is, just quit the program. If it isn't or it's some other status, return the status to finish the rest of the program.
#The example in this case is the Asigra Linux DS-Client Service.

def DSClientServiceCheck():
	IsItRunning_Value = subprocess.call(checkdsclient, shell=True)

	if IsItRunning_Value == 'running':
		sys.exit()

#If the service isn't running. Send an SMS to everyone listed in the Numbers Dictionary. Haven't figured out how to identify which customer the service is down for since most just use localhost.localdomain.  

def SendSMS():
	for name, number in Numbers.items():
		message = Client.messages.create(to=number, from_=Twilio_Number, body="HEY! The Linux DS-Client for <insert customer> is down or stuck!")


def main():
	#Main entry point for the script

	#Check If The Service Is Running
	DSClientServiceCheck()

	#Send The SMS If The Status is anything but running as defined in the global function above.
	SendSMS()

if __name__ == '__main__':
    sys.exit(main())
