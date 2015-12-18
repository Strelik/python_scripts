#!/usr/bin/env python
import os
import sys
import subprocess
import getpass


#Global Variables
password = getpass.getpass(prompt="Input your Sudo Password: " )

#Shell CMDS Variables
tmpdir = '[ ! -d /opt/ica ] && sudo mkdir -p /opt/ica'
kernel = "uname -r | grep -oP '(\d)\.\d+'"
distrocmd = "cat /etc/*-release | grep -oP '(^NAME=(Fedora))' | grep -oP '(Fedora)$'"
fusioncmd = 'sudo dnf install http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm'
rpminstallcmd = "sudo wget -O /opt/ica/linuxxica-13.3.tar.gz https://googledrive.com/host/0B_RKYajewrzSNVltd0NQcThxbkU && cd /opt/ica && sudo tar -xvzf /opt/ica/linuxxica-13.3.tar.gz && sudo /opt/ica/setupwfc"
copypemexportcmd = "cd /opt/Citrix/ICAClient/keystore/cacerts && sudo wget https://certs.godaddy.com/repository/gd-class2-root.crt "

#Global Functions

def GetKernel():
	kernel_value = float(subprocess.check_output(kernel, shell=True))
	if kernel_value < 2.6 :
		print("Your kernel is not new enough. Requires Kernel 2.6.29 or higher.")
		sys.exit()
	else:
		print ("Your kernel is new enough. Proceeding with install.\n")

def GetDistro():

	distro_value = str(subprocess.check_output(distrocmd, shell=True))

	return (distro_value)

def InstallFusion():
	subprocess.check_output(fusioncmd, shell=True)


# Using an "or" operator causes any other input to be allowed past the loop.
def InstallPrompt1():

	ask_yum = input("\nUse Yum to install all the necessary dependencies? Type Y or N: ")

	while True:
		if ask_yum == "Y":
			break
		elif ask_yum == "N":
			break
		else:
			ask_yum = input("\nUse Yum to install all the necessary dependencies? Type Y or N: ")

	return ask_yum


def InstallYumPkgs():

	subprocess.call("sudo yum -y install libgtk-x11-2.0.so.0 libgdk-x11-2.0.so.0 libatk-1.0.so.0 libgdk_pixbuf-2.0.so.0", shell= True)

def TmpDirCreate(): #Create temporary working directory to download ICAClient.

    subprocess.call(tmpdir, shell=True)

def ICAInstall():

	subprocess.call(rpminstallcmd, shell=True)

def InstallCert():

	subprocess.call(copypemexportcmd, shell=True)


def main():

    GetKernel()

    distro_value = GetDistro()

    if "Fedora" in distro_value:
        print("Proceeding with a Fedora installation of ICA Client.\n")
    else:
        print("\nDistro Is Not Fedora.\n")
        sys.exit()

    print("\nChecking if Fusion Repository is added, if not let's add it\n")

    InstallFusion()

    answer1 = InstallPrompt1()

    if answer1 == 'Y':
        InstallYumPkgs()
    else:
        print("\nSkipped\n")
        pass

    TmpDirCreate()

    ICAInstall()

# Install the GoDaddy security certificate from the web so ICA trusts it.
    InstallCert()

    print("\nCitrix Receiver should be installed and working on your system.\n")

if __name__ == '__main__':
    sys.exit(main())