#!/usr/bin/env python
"""I have no idea what I'm going to do with this"""
import os
import sys
import subprocess
import getpass

#Exception Class to make sure this is run with sudo privleges

#Global Variables

password = getpass.getpass(prompt="Input your Sudo Password: " )

#Shell CMDS
tmpdir = '[ ! -d /opt/ica ] && sudo mkdir -p /opt/ica'
space = "df -k"
kernel = "uname -r | grep -oP '(\d)\.\d+'"
distrocmd = "cat /etc/*-release | grep -oP '(^NAME=(Fedora))' | grep -oP '(Fedora)$'"
fusioncmd = 'sudo yum localinstall --nogpgcheck http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm'
rpminstallcmd = "sudo wget -O /opt/ica/linuxxica-13.1.tar.gz https://googledrive.com/host/0B_RKYajewrzSd0ZxNVFvY1pZNVU && sudo tar -xvzf /opt/ica/linuxxica-13.1.tar.gz && sudo /opt/ica/setupwfc"
copypemexportcmd = "sudo wget https://certs.godaddy.com/repository/gd-class2-root.crt; sudo cp ./gd-class2-root.crt /opt/Citrix/ICAClient/keystore/cacerts/"

#Global Functions.

#Get the main version of the kernel and return it to a variable.

def GetKernel():
	kernel_value = float(subprocess.check_output(kernel, shell=True))
	if kernel_value < 2.6 :
		print("Your kernel is not new enough. Requires Kernel 2.6.29 or higher to proceed\n")
		sys.exit()
	else:
		print ("Your kernel is new enough. Go you. Moving on\n")


# Performs a similar command above to get your distribution name. 
def GetDistro():

	distro_value = str(subprocess.check_output(distrocmd, shell=True))

	return (distro_value)

#Runs a long yum local install to grab the latest Fusion repository for Fedora

def GetFusion():
	yumfusion = subprocess.check_output(fusioncmd, shell=True)


#Using an "or" operator causes any other input to be allowed past the loop. Not sure why. 
def InstallPrompt1():

	ask_yum = input("Use Yum to install all the necessary dependencies? Type Y or N: ")

	while True:
		if ask_yum == "Y":
			break
		elif ask_yum == "N":
			break
		else:
			ask_yum = input("Use Yum to install all the necessary dependencies? Type Y or N: ")

	return ask_yum


def InstallYumPkgs():

	subprocess.call("sudo yum -y install yum install libgtk-x11-2.0.so.0 libgdk-x11-2.0.so.0 libatk-1.0.so.0 libgdk_pixbuf-2.0.so.0", shell= True)

#Need to install version 12.1 from some webserver somewhere force install if dependencies are not met.

def TmpDirCreate():

    subprocess.call(tmpdir, shell=True)

def RpmInstall():

	subprocess.call(rpminstallcmd, shell=True)

def InstallCert():

	subprocess.call(copypemexportcmd, shell=True)
	

def main():

# Check kernel requirements

    GetKernel()

#Check if it's a Fedora or ubuntu system
    distro_value = GetDistro()

    if "Fedora" in distro_value:
        print("Proceeding with a Fedora installation of ICA Client")

    elif "Ubuntu" in distro_value:
        print("Proceeding with an Ubuntu installation of ICA Client")
    else:
        print("Distro Not Recognized.")
        sys.exit()

    '''Check some basic system requirements for the system. Not sure if this is needed anymore for ICA 13.1 so I'm commenting it out.'''
    print("Checking if Fusion Repository is added, if not let's add it\n")

    GetFusion()

	
# Prompt user if they want to update and install all the necessary libraries and warn
#them if they skip this option the receiver client might have issues.

    answer1 = InstallPrompt1()

    if answer1 == 'Y':
        InstallYumPkgs()
    else:
        print("\nSkipped\n")
        pass

# Check and Create Tmp Directory For ICA Installer Download
    TmpDirCreate()

#Download and run the setup for the Citrix setup.

    RpmInstall()

#install the security certificates from the Mozilla directory.

    #InstallCert()

#Print Out a message.

    '''print("Cool, Citrix Receiver should be installed on your system.\n")
    print("\n Just tell Firefox to always open the .ica files with /opt/Citrix/ICAClient/wfica.bin")'''


if __name__ == '__main__':
    sys.exit(main())