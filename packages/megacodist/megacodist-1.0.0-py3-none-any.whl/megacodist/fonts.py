import winreg

def installed_fonts_str() -> tuple:
    """Retruns a list of string which every element is a string consists of family name and also style if it has."""
    
    # Connecting to the registry of the local computer...
    hklm = winreg.ConnectRegistry(
        None,
        winreg.HKEY_LOCAL_MACHINE
    )
    # Getting installed fonts registry key which is a subkey of HKEY_LOCAL_MACHINE...
    fonts_regkey = winreg.OpenKey(
        hklm,
        "software\\microsoft\\windows nt\\currentversion\\fonts"
    )
    fonts=[]
    i=0
    while True:
        try:
            vname, value, vtype = winreg.EnumValue(fonts_regkey, i)
            if (vname[-1] == ")"):
                vname = vname[0:(vname.rindex("(") - 1)]
            fonts.append(vname)
            i += 1
        except WindowsError:
            break
    fonts_regkey.Close()
    
    return fonts