from PrintWithColor.PrintWithColor import print as print
print.change_settings('DoNotResetColor', True)
print('Đây là dòng 1', f='black', b='green')
print("Đây là dòng 2")
print.change_settings(1, False)
print("Đây là dòng 3", f='cyan', b='white')
print("Đây là dòng 4")