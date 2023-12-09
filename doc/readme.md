# nuitka打包指令
nuitka --mingw64 --standalone --show-progress --show-memory --windows-disable-console  --windows-icon-from-ico=./doc/image/exeicon.ico --output-dir=out1 main.py

# pyinstall打包指令
pyinstaller -i ./config/icon/icon.ico -F -w main.py