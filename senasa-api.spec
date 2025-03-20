# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['senasa-api.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/odoo16/server/addons_ext/kernel/ws-rest/senasa/config.ini', '.'), ('C:/odoo16/server/addons_ext/kernel/ws-rest/senasa/conn', 'conn')],
    hiddenimports=['pyodbc', 'paramiko', 'configparser'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pkg_resources'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='senasa-api',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
