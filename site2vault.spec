# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = []
binaries = []
hiddenimports = ['h2', 'hpack', 'hyperframe', 'lxml.html', 'lxml.html.clean', 'lxml.etree', 'markdownify', 'yaml', 'bs4', 'site2vault', 'site2vault.cli', 'site2vault.config', 'site2vault.crawler', 'site2vault.extract', 'site2vault.convert', 'site2vault.rewrite', 'site2vault.canonical', 'site2vault.slug', 'site2vault.state', 'site2vault.robots', 'site2vault.politeness', 'site2vault.antibot', 'site2vault.frontmatter', 'site2vault.logging_setup', 'site2vault.orchestrator']
tmp_ret = collect_all('trafilatura')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('certifi')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['src\\site2vault\\cli.py'],
    pathex=['src'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='site2vault',
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
