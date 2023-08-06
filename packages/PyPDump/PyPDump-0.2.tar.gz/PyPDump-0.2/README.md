Inofficial Pyton wrapper for [ProcDump - Windows Sysinternals | Microsoft Docs](https://docs.microsoft.com/en-us/sysinternals/downloads/procdump)

Very easy to use:

```python
    dumpfile = r"C:\MiniDumpWithFullMemoryx.dmp"
    pid = 16544
    createdump = True
    if createdump:
        erg = (
            ProcDump(executeable=r"C:\Program Files\procdump.exe")
            .o()
            .ma()
            .add_own_parameter_or_option(f"{pid}")
            .add_target_file_or_folder([dumpfile])
            .run()
        )

        )


```
