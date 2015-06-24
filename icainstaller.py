#!/usr/bin/env python
"""I have no idea what I'm going to do with this"""



# Define imported modules
import os
import sys
import subprocess

#Global Variables

#Shell CMDS
space = "df -k"
kernel = "uname -r | grep -oP '(\d)\.\d+'"
distrocmd = "cat /etc/*-release | grep -oP '(^NAME=(Fedora))' | grep -oP '(Fedora)$'"
fusioncmd = 'sudo yum localinstall --nogpgcheck http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm'
rpminstallcmd = "sudo rpm -ivh http://tpartners.com/ICAClient_12.1.0-0.x86_64.rpm"
copypemexportcmd = "sudo wget https://certs.godaddy.com/repository/gd-class2-root.crt; sudo cp ./gd-class2-root.crt /opt/Citrix/ICAClient/keystore/cacerts/"

#Global Functions.

#Get the main version of the kernel and return it to a variable.

def GetKernel():
	kernel_value = subprocess.check_output(kernel, shell=True)
	if kernel_value < 2.6 :
		print "\NYour kernel is not new enough. Requires Kernel 2.6.29 or higher to proceed\n"
		sys.exit()
	else:
		print "Your kernel is new enough. Go you. Moving on\n"


# Performs a similar command above to get your distribution name. 
def GetDistro():
	
	distro_value = subprocess.check_output(distrocmd, shell=True)

	return distro_value

#Runs a long yum local install to grab the latest Fusion repository for Fedora

def GetFusion():
	yumfusion = subprocess.check_output(fusioncmd, shell=True)


#Using an "or" operator causes any other input to be allowed past the loop. Not sure why. 
def InstallPrompt1():
	
	
	input = raw_input("Use Yum to install all the necessary dependencies? Type Y or N: ")

	while True:
		if input == "Y":
			break
		elif input == "N":
			break
		else:
			input = raw_input("Use Yum to install all the necessary dependencies? Type Y or N: ")

	return input


def InstallYumPkgs():

	subprocess.call("sudo yum -y install PackageKit-gtk3-module.i686 adwaita-gtk2-theme.i686 libpng12.i686 nspluginwrapper.x86_64 nspluginwrapper.i686 libgtkhotkey.i686 libwebkit2gtk.i686 libgtkhotkey.i686 libcurl.i686 ffmpeg.x86_64 motif.x86_64 motif.i686 alsa-lib.i686 alsa-lib.x86_64 libXaw.x86_64 libXaw.i686", shell= True)

#Need to install version 12.1 from some webserver somewhere force install if dependencies arn't met.

def RpmInstall():

	subprocess.call(rpminstallcmd, shell=True)

def InstallCert():

	subprocess.call(copypemexportcmd, shell=True)
	

def main():
	pass

# Check kernel requirements

	GetKernel()

#Check if it's a Fedora or ubuntu system
	distro_value = GetDistro()

	if distro_value == "Fedora\n":
		print "Proceeding with a Fedora installation of ICA Client\n"
	elif distro_value == "Ubuntu\n":
		print "Proceeding with an Ubuntu installation of ICA Client"
	else:
		print "Supported Distro Not Recognized."
		sys.exit()

#Check some basic system requirements for the system.
  	print "Checking if Fusion Repository is added, if not let's add it.\n"

	GetFusion()

	
#Prompt user if they want to update and install all the necessary libraries and warn
#them if they skip this option the receiver client might have issues.

	answer1 = InstallPrompt1()

	if answer1 == 'Y':
		InstallYumPkgs()
	else:
		print "\nSkipped\n"
		pass

#install the 12.1 rpm from the tpartners hosted on the tpartners website.

	RpmInstall()

#install the security certificates from the Mozilla directory

	InstallCert()

#Print Out a message.

	print "Cool, Citrix Receiver should be installed on your system.\n"
	print "\n Just tell Firefox to always open the .ica files with /opt/Citrix/ICAClient/wfica.bin"



"""Let's you run the program as standalone and return 0"""
if __name__ == '__main__':
    sys.exit(main())