# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/python code/main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/starco_icon.ico', '.'), ('C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/clients.json', '.'), ('C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/users.json', '.'), ('C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/guests.json', '.'), ('C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/user_profile.json', '.'), ('C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/clients_tasks.json', '.'), ('C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/clients_reviews.json', '.'), ('C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/python code/country_codes.json', '.'), ('C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/python code/Shops_Elect_meters.json', '.'), ('C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/python code/docs/documents.txt', '.'), ('C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/supporting_documents/starco_rent_contract_1.pdf', '.'), ('C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/application_outputs/contracts/reservation_contracts.json', '.'), ('C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/supporting_documents', '.'), ('C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/starco icon', '.'), ('C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/python code', '.'), ('C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/python code/docs', '.'), ('C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/Clients', '.'), ('C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/application_outputs', '.'), ('C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/application_outputs/clients_logs', '.'), ('C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/application_outputs/tasks_logs', '.'), ('C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/application_outputs/observation_logs', '.'), ('C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/application_outputs/contracts', '.')],
    hiddenimports=[],
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
    name='clients_manager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:/Users/ssssh/OneDrive/Documents/Client_Manager_optimized/starco_icon.ico'],
)
