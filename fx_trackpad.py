# https://github.com/eletrixtime/elanlinux-fix

import os
import time
_DEBUG = False # change this to False :)
_AUTO = False

if _DEBUG:
    print("debug is enabled..")

print("[Trackpad FX] : Are your sure this is a Lenovo Laptop ? (tested on Lenovo 14w gen 2)")
print("WARNING: I'm not responsible for any break of your OS \n ONLY USE IF YOU UNDERSTAND THE RISK!")
if not _AUTO:
    if input("Sure ? (Y/N)").lower() == "y":
        print("Continuing...")
    else:
        exit()

def detect_distro():
    try:
        with open('/etc/os-release', 'r') as f:
            data = f.read().lower()
            if 'arch' in data:
                return False
            elif 'debian' in data:
                return True
            else:
                False

    except FileNotFoundError:
        return "error when searching file"
        

print("[Trackpad FX] : Installing acpi-tools")

if detect_distro():
    os.system("sudo apt install acpica-tools -y")
else:
    os.system("sudo pacman -Sy --noconfirm acpica")

print("[Trackpad FX] : Done installing acpica tools")
if not _DEBUG:
    os.system("sudo sh -c 'cat /sys/firmware/acpi/tables/DSDT > dsdt.aml'")
    os.system("iasl -d dsdt.aml")

replacement = 'DefinitionBlock ("", "DSDT", 1, "LENOVO", "AMD", 0x00001001)'

with open("dsdt.dsl", 'r') as f:
    lines = f.readlines()

with open("dsdt_out.dsl", 'w') as f:
    for line in lines:
        if line.strip() == 'DefinitionBlock ("", "DSDT", 1, "LENOVO", "AMD", 0x00001000)':
            f.write(replacement + '\n')
            print("done modifying the def block")
        else:
            f.write(line)

with open("dsdt_out.dsl", 'r') as f_in, open("dsdt.dsl.tmp", 'w') as f_out:
    for line_num, line in enumerate(f_in, start=1):
        if line_num == 7734:
            print("replce")
            f_out.write("                            Else\n")
        elif line_num == 7778:
            print("replace")
            f_out.write("                Else\n")
        else:
            f_out.write(line)

os.replace("dsdt.dsl.tmp", "dsdt_out.dsl")

print("[Trackpad FX] : Patched the DSDT")

if not _DEBUG:
    os.system("iasl -sa dsdt_out.dsl")
    os.system("sudo cp dsdt_out.aml /boot/fixed_dsdt.aml")
    os.system("""sudo sh -c "echo '# load correct acpi table on any boot\nacpi /boot/fixed_dsdt.aml' >> /etc/grub.d/40_custom""")
    print("Patching is done, please review the grub config before continuing")
    os.system("cat /etc/grub.d/40_custom")
    if not _AUTO:
        if input("DO YOU WANT TO CONTINUE ?? (Y/N)").lower() == "y":
            print("starting in 3 seconds")
        else:
            print("cancelled")
            exit()
    time.sleep(5)
    os.system("sudo update-grub")
    print("patching successfully, please reboot your computer.")
