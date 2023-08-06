import builtins
# Sorry everyone, all this code still not translated into English :[

def get_settings(n=8):  # This code will get settings, if there are exception(s), it will reset everything
        try:
            with open('PrintWithColor.settings', 'r') as settings:
                AllSettings = settings.read()
                settings.close()
                if AllSettings == '':
                    raise Exception
        except:
            with open('PrintWithColor.settings', 'w') as settings:
                AllSettings = ('False\nWHITE\nBLACK\nNORMAL\nWHITE\nBLACK\nNORMAL')
                #                 1      2      3      4       5      6      7
                # 1       : DoNotResetColor
                # 2 --> 4 : DefaultForegroundColor, DefaultBackgroundColor, DefaultStyle
                # 5 --> 7 : LastForegroundColor   , LastBackgroundColor,    LastStyle
                settings.write(AllSettings)
                settings.close()

        AllSettings = AllSettings.split('\n')
        if AllSettings[0] == "True":
            AllSettings[0] = True
        else:
            AllSettings[0] = False
        if n < 8:
            return AllSettings[n-1]
        else:
            return AllSettings


def set_settings(n, value):     # <--  print.change_settngs

    AllSettings = get_settings()
    # 1       : DoNotResetColor
    # 2 --> 4 : DefaultForegroundColor, DefaultBackgroundColor, DefaultStyle
    # 5 --> 7 : LastForegroundColor   , LastBackgroundColor,    LastStyle

    with open('PrintWithColor.settings', 'w') as settings:
        AllSettings[n-1] = value
        if AllSettings[0] == True:
            AllSettings[0] = "True"
        else:
            AllSettings[0] = "False"
        
        settings.write('\n'.join( [str(i) for i in AllSettings] ))
        settings.close()

def printToComputer(self, *textfrominput, sep = ' ', end = '\n', file = None, flush = False, f, b, s,):

    # Đoạn code này dùng để hiển thị chữ có màu trên Windows

    from colorama import Fore        as FORE  # <-- Màu chữ
    from colorama import Back        as BACK  # <-- Màu nền
    from colorama import Style       as STYLE # <-- Kiểu màu
    from colorama import init        as __init
    from colorama import AnsiToWin32 as __AnsiToWin32
    import sys
    __init(wrap=False)
    __stream = __AnsiToWin32(sys.stderr).stream

    # Từ điển màu chữ
    foreground_dict = {
        "WHITE"  : FORE.WHITE,
        "RED"    : FORE.RED,
        "GREEN"  : FORE.GREEN,
        "YELLOW" : FORE.YELLOW,
        "BLUE"   : FORE.BLUE,
        "MAGENTA": FORE.MAGENTA,
        "CYAN"   : FORE.CYAN,
        "BLACK"  : FORE.BLACK,
    }

    background_dict = {
        "WHITE"  : BACK.WHITE,
        "RED"    : BACK.RED,
        "GREEN"  : BACK.GREEN,
        "YELLOW" : BACK.YELLOW,
        "BLUE"   : BACK.BLUE,
        "MAGENTA": BACK.MAGENTA,
        "CYAN"   : BACK.CYAN,
        "BLACK"  : BACK.BLACK,
    }

    styles_dict = {
        "DIM"    : STYLE.DIM,
        "NORMAL" : STYLE.NORMAL,
        "BRIGHT" : STYLE.BRIGHT,
    }

    # This list will contain all acceptable colors
    LegitColors = ['WHITE','RED','GREEN','YELLOW','BLUE','MAGENTA','CYAN','BLACK']


    f = f.upper()
    b = b.upper()
    s = s.upper()


    # Search in 3 dictionaries
    try:
        ff = foreground_dict[f]
        bb = background_dict[b]
        ss = styles_dict[s]
    except:                             # If errors, reset 3 colors into default and check errors
        ff = foreground_dict['WHITE']
        bb = background_dict['BLACK']
        ss = styles_dict['NORMAL']


        if f == get_settings(2) or f not in LegitColors:
      # if f == DefaultForegroundColor or f == LastForegroundColor or f not in LegitColors:
            set_settings(2, 'WHITE')
        elif f == get_settings(5):
      # elif f == LastForegroundColor:
            set_settings(5, 'WHITE')
        
        if b == get_settings(3) or b not in LegitColors:
      # if b == DefaultBackgroundColor or b == LastBackgroundColor or b not in LegitColors:
            set_settings(3, 'BLACK')
        elif b == get_settings(6):
      # elif f == LastForegroundColor:
            set_settings(6, 'BLACK')
        
        if s == get_settings(4) or b not in ['DIM','NORMAL','BRIGHT']:
            set_settings(4, 'NORMAL')
      # elif f == LastForegroundColor:
        elif s == get_settings(7):
            set_settings(7, 'NORMAL')

        if get_settings(1) not in [True, False]:
            set_settings(1, False)

    global fileIsWriteable

    try:    # Check if file argument is a writeable file?
            # If it is a writeable file, write the output to it
        if file != None:
            file.write('')
            fileIsWriteable = True
        else:
            fileIsWriteable = False
    except:
        fileIsWriteable = False

    for item in textfrominput:
        if item != textfrominput[-1]:
            if not fileIsWriteable:
                builtins.print(ff+bb+ss+item, end=sep, file=__stream, flush=flush)
            else:
                file.write(item+sep)

        else:
            if not fileIsWriteable:
                builtins.print(ff+bb+ss+item, end=end, file=__stream, flush=flush)
            else:
                file.write(item+end)
        
    if get_settings(1)== False:  # if DoNotResetColor == False:
        builtins.print(STYLE.RESET_ALL, end='')
        # LastForegroundColor = DefaultForegroundColor
        set_settings(5, get_settings(2))
        # LastBackgroundColor = DefaultBackgroundColor
        set_settings(6, get_settings(3))
        # LastStyle = DefaultStyle
        set_settings(7, get_settings(4))
    else:
        # LastBackgroundColor = b
        # LastForegroundColor = f
        # LastStyle = s

        set_settings(5, f)
        set_settings(6, b)
        set_settings(7, s)

    try:
        file.close()
    except:
        pass

get_settings()