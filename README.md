# WoW AddOn Updater
AddOn updater for popular game World of Warcraft.

## Building
Use the following `.spec` file to build the project to a single-file executable with PyInstaller
```
# -*- mode: python -*-

block_cipher = None


a = Analysis(['src\\run.py'],
             pathex=['PATH_TO_REPO_DIRECTORY'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='WoW Addon Updater',
          debug=False,
          strip=False,
          upx=True,
          icon='graphics/icon.ico',
          runtime_tmpdir=None,
          console=False )
```

Be sure to change `pathex=['PATH_TO_REPO_DIRECTORY']` to the directory where the project files are stored. 

Command to build: 
* `> pyinstaller ./run.spec`

## Licensing
This application is licensed under the [GNU General Public License v3.0](LICENSE).
