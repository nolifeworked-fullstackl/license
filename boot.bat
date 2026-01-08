@echo off
echo.
echo !!! WARNING !!!
echo This will DELETE the Windows Boot Manager entry.
echo BIOS will report "No bootable device".
echo.
echo MAKE SURE YOU HAVE A RECOVERY USB!
echo.
pause
cls

:: 1. Делаем бэкап (на всякий случай)
bcdedit /export C:\bcd_backup_full

:: 2. Удаляем запись Диспетчера Загрузки (Boot Manager)
:: Это заставит BIOS думать, что винды нет
bcdedit /delete {bootmgr} /f

echo.
echo ==================================================
echo  DONE. WINDOWS BOOT MANAGER DELETED.
echo  RESTARTING IN 5 SECONDS...
echo ==================================================
timeout /t 5
shutdown /r /t 0