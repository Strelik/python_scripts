__author__ = 'jason'
import sys
import os
import subprocess

"""Run subprocess to grab your running Linux Kernel and store it in a variable"""
running_kernel = subprocess.check_output('uname -a | grep -oP \'(\d+\.\d+\.\d+-\d+\.\w+)\'', shell=True)


"""Define Functions Here:"""

def grab_kernels():
    """Run a subprocess call to grab a list of all installed kernels installed in your system.
    Format the long string by \n (newline) into individual list elements and return them."""

    """Seems to grab an extra '.' at the end of the list. Doesn't halt the script so no need to fix it"""
    installed_kernels = subprocess.check_output("yum list kernel.* | awk '/kernel.*/ {print $2}'", shell=True)

    formatted_installed_kernels = installed_kernels.split('\n')

    return formatted_installed_kernels


def uninstall_kernels():
    """Take that list of installed kernels. Compare it to the list of installed kernels.
    If it doesn't match uninstall it.'"""

    list = grab_kernels()

    for x in list:
        if x == running_kernel:
            print("Skipping Running Kernel")
        else:
            subprocess.check_output("sudo yum remove kernel-%s.x86_64 -y" % x, shell=True)
            print(x)


def main():

    """Main entry point for the script."""

    grab_kernels()

    uninstall_kernels()

main()


if __name__ == '__main__':
    sys.exit(main())