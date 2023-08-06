import subprocess
import re
from tempfile import SpooledTemporaryFile as tempfile
from typing import Union


class ProcDump:
    def __init__(self, executeable=r"procdump.exe", option_targetfile=None):

        self.tempfile_for_vars = "ProcDump.Protmp"
        self.delete_tempfile_for_vars_search = False
        self.executeable = executeable
        self.necessary_beginning = [self.executeable]
        self.options_parameters = {
            "a": "-a",
            "at": "-at",
            "b": "-b",
            "c": "-c",
            "cl": "-cl",
            "d": "-d",
            "e": "-e",
            "f": "-f",
            "fx": "-fx",
            "g": "-g",
            "h": "-h",
            "i": "-i",
            "k": "-k",
            "l": "-l",
            "m": "-m",
            "ma": "-ma",
            "mc": "-mc",
            "md": "-md",
            "mk": "-mk",
            "ml": "-ml",
            "mm": "-mm",
            "mp": "-mp",
            "n": "-n",
            "o": "-o",
            "p": "-p",
            "pl": "-pl",
            "r": "-r",
            "s": "-s",
            "t": "-t",
            "u": "-u",
            "w": "-w",
            "wer": "-wer",
            "x": "-x",
            "NO_64": "-64",
        }
        self.execute_dict = {
            "-a": False,
            "-at": False,
            "-b": False,
            "-c": False,
            "-cl": False,
            "-d": False,
            "-e": False,
            "-f": False,
            "-fx": False,
            "-g": False,
            "-h": False,
            "-i": False,
            "-k": False,
            "-l": False,
            "-m": False,
            "-ma": False,
            "-mc": False,
            "-md": False,
            "-mk": False,
            "-ml": False,
            "-mm": False,
            "-mp": False,
            "-n": False,
            "-o": False,
            "-p": False,
            "-pl": False,
            "-r": False,
            "-s": False,
            "-t": False,
            "-u": False,
            "-w": False,
            "-wer": False,
            "-x": False,
            "-64": False,
        }
        self.helpdict = {
            "a": "Avoid outage. Requires -r. If the trigger will cause the target to suspend for a prolonged time due\nto an exceeded concurrent dump limit, the trigger will be skipped.",
            "at": "Avoid outage at Timeout. Cancel the trigger's collection at N seconds.",
            "b": "Treat debug breakpoints as exceptions (otherwise ignore them).",
            "c": "CPU threshold at which to create a dump of the process.",
            "cl": "CPU threshold below which to create a dump of the process.",
            "d": "Invoke the minidump callback routine named MiniDumpCallbackRoutine of the specified DLL.",
            "e": "Write a dump when the process encounters an unhandled exception. Include the 1 to create dump on\nfirst chance exceptions.",
            "f": 'Filter the first chance exceptions. Wildcards (*) are supported. To just display the names without\ndumping, use a blank (") filter.',
            "fx": "Filter (exclude) on the content of exceptions and debug logging. Wildcards are supported.",
            "g": "Run as a native debugger in a managed process (no interop).",
            "h": "Write dump if process has a hung window (does not respond to window messages for at least 5\nseconds).",
            "i": "Install ProcDump as the AeDebug postmortem debugger. Only -ma, -mp, -d and -r are supported as\nadditional options.",
            "k": "Kill the process after cloning (-r), or at the end of dump collection",
            "l": "Display the debug logging of the process.",
            "m": "Memory commit threshold in MB at which to create a dump.",
            "ma": "Write a dump file with all process memory. The default dump format only includes thread and handle\ninformation.",
            "mc": "Write a custom dump file. Include memory defined by the specified MINIDUMP_TYPE mask (Hex).",
            "md": "Write a Callback dump file. Include memory defined by the MiniDumpWriteDump callback routine named\nMiniDumpCallbackRoutine of the specified DLL.",
            "mk": "Also write a Kernel dump file. Includes the kernel stacks of the threads in the process. OS doesn't\nsupport a kernel dump (-mk) when using a clone (-r). When using multiple dump sizes, a kernel dump\nis taken for each dump size.",
            "ml": "Trigger when memory commit drops below specified MB value.",
            "mm": "Write a mini dump file (default).",
            "mp": "Write a dump file with thread and handle information, and all read/write process memory. To minimize\ndump size, memory areas larger than 512MB are searched for, and if found, the largest area is\nexcluded. A memory area is the collection of same sized memory allocation areas. The removal of this\n(cache) memory reduces Exchange and SQL Server dumps by over 90%.",
            "n": "Number of dumps to write before exiting.",
            "o": "Overwrite an existing dump file.",
            "p": 'Trigger on the specified performance counter when the threshold is exceeded. Note: to specify a\nprocess counter when there are multiple instances of the process running, use the process ID with\nthe following syntax: "\\Process(<name>_<pid>)\\counter"',
            "pl": "Trigger when performance counter falls below the specified value.",
            "r": "Dump using a clone. Concurrent limit is optional (default 1, max 5). CAUTION: a high concurrency\nvalue may impact system performance. - Windows 7\xa0\xa0 : Uses Reflection. OS doesn't support -e. -\nWindows 8.0 : Uses Reflection. OS doesn't support -e. - Windows 8.1+: Uses PSS. All trigger types\nare supported.",
            "s": "Consecutive seconds before dump is written (default is 10).",
            "t": "Write a dump when the process terminates.",
            "u": "Treat CPU usage relative to a single core (used with -c). As the only option, Uninstalls ProcDump as\nthe postmortem debugger.",
            "w": "Wait for the specified process to launch if it's not running.",
            "wer": "Queue the (largest) dump to Windows Error Reporting.",
            "x": "Launch the specified image with optional arguments. If it is a Store Application or Package,\nProcDump will start on the next activation (only).",
            "NO_64": "By default ProcDump will capture a 32-bit dump of a 32-bit process when running on 64-bit Windows.\nThis option overrides to create a 64-bit dump. Only use for WOW64 subsystem debugging.",
        }
        self.target_file_or_folder = []
        self.option_targetfile = option_targetfile
        self.join_parameters_dict = {}
        self.same_command_multiple_times = {}
        self.separador_for_multiple_arguments = "Ç"
        self.self_added_arguments = []
        self.last_command_line_called = []

    def add_python_variable_instead_of_file(self, variable: [bytes, str]):
        if isinstance(variable, str):
            variable = variable.encode()
        self.target_file_or_folder.append(variable)
        return self

    def add_target_file_or_folder(self, target_file_or_folder: Union[str, list]):
        if isinstance(target_file_or_folder, str):
            target_file_or_folder = [target_file_or_folder]
        self.target_file_or_folder.extend(target_file_or_folder)
        return self

    def reset_options(self):
        for key in list(self.execute_dict.keys()):
            self.execute_dict[key] = False
        self.self_added_arguments = []
        return self

    def print_options_to_screen(self):
        for help, exe in zip(self.helpdict.items(), self.execute_dict.items()):
            key_h, item_h = help
            key_e, item_e = exe
            print(f"""Parameter:\t\t\t{key_e} {key_h}""")
            print(f"""Current Settings:\t\t{item_e} (False=not activated)""")
            print(f"""Information:\t\t{item_h}""")

            print(
                "---------------------------------------------------------------------------------------------"
            )
        print(f"""Self Added Arguments:\t\tf{self.self_added_arguments}""")
        return self

    def run(
        self,
        capture_output: bool = True,
        save_output_with_shell: Union[None, str] = None,
    ):
        self.last_command_line_called = []
        regexlist = []
        add_to_search = [
            (
                re.sub(str(self.separador_for_multiple_arguments) + r"\d*$", "", x[0]),
                str(x[1]),
                x[1],
            )
            for x in self.execute_dict.items()
            if x[1] is not False
        ]
        add_to_search_list = []
        for key, item, real_value in add_to_search:
            print(key, item)
            if isinstance(real_value, bool):

                add_to_search_list.append([key])
            else:
                if key in self.join_parameters_dict:
                    add_to_search_list.append([f"{key}{item}"])
                else:
                    add_to_search_list.append([key, item])

        regexlist.extend(add_to_search_list)
        regexlist = self.necessary_beginning + regexlist + self.self_added_arguments
        regexlist = ProcDump.flatten_iter(regexlist)
        if self.option_targetfile is not None:
            regexlist.append(self.option_targetfile)
        if self.target_file_or_folder:
            if isinstance(self.target_file_or_folder[0], str):
                regexlist.extend(self.target_file_or_folder)
            else:
                f = tempfile()
                f.write(self.target_file_or_folder[0])
                f.seek(0)
                ergebnis = subprocess.run(regexlist, stdin=f, capture_output=True)
                f.close()
                self.last_command_line_called = regexlist.copy()
                return ergebnis

        if save_output_with_shell is not None:
            regexlist.append(">>")
            regexlist.append(save_output_with_shell)
            ergebnis = subprocess.run(
                regexlist, capture_output=capture_output, shell=True
            )
        else:
            ergebnis = subprocess.run(regexlist, capture_output=capture_output)
        self.last_command_line_called = regexlist.copy()
        return ergebnis

    def add_own_parameter_or_option(self, values):
        if not isinstance(values, (list, tuple)):
            values = [values]
        values = self.flatten_iter(values)
        self.self_added_arguments.extend(values)
        return self

    @staticmethod
    def _delete_duplicates_from_nested_list(nestedlist):
        tempstringlist = {}
        for ergi in nestedlist:
            tempstringlist[str(ergi)] = ergi
        endliste = [tempstringlist[key] for key in tempstringlist.keys()]
        return endliste.copy()

    @staticmethod
    def flatten_iter(iterable):
        def iter_flatten(iterable):
            it = iter(iterable)
            for e in it:
                if isinstance(e, (list, tuple)):
                    for f in iter_flatten(e):
                        yield f
                else:
                    yield e

        a = [
            i if not isinstance(i, (str, int, float)) else [i]
            for i in iter_flatten(iterable)
        ]
        a = [i for i in iter_flatten(a)]
        return a

    def _handle_multiple_times_same_flag(self, key_to_check, value_to_set):
        are_there_more = True
        startvalue = 0
        keytocheck = ""
        while are_there_more:
            keytocheck = (
                f"{key_to_check}"
                + self.separador_for_multiple_arguments
                + str(startvalue)
            )
            if not keytocheck in self.execute_dict:
                are_there_more = False
            else:
                if isinstance(value_to_set, bool):
                    if value_to_set is False:
                        self.execute_dict[keytocheck] = value_to_set
                startvalue = startvalue + 1
        if keytocheck not in self.execute_dict:
            if isinstance(value_to_set, bool):
                if value_to_set is False:
                    return
            self.execute_dict[keytocheck] = value_to_set

    def _print_option_activate_warning(self):
        print(
            'Did you confuse option and activated?\\nIf you use True/False (bool), for option, I will activate/deactivate the active settings\\nUse "True"/"False" as arguments for the commandline '
        )

    def add_own_argument(self):
        print(
            'Did you confuse option and activated?\\nIf you use True/False (bool), for option, I will activate/deactivate the active settings\\nUse "True"/"False" as arguments for the commandline '
        )

    def a(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Avoid outage. Requires -r. If the trigger will cause the target to suspend for a prolonged time due
to an exceeded concurrent dump limit, the trigger will be skipped."""
        if get_help:
            print(self.helpdict["a"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-a"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-a", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-a"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-a"] is False and not multi_allowed:
                self.execute_dict["-a"] = option
            varformulti = option
        else:
            self.execute_dict["-a"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-a", value_to_set=varformulti
            )
        return self

    def at(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Avoid outage at Timeout. Cancel the trigger's collection at N seconds."""
        if get_help:
            print(self.helpdict["at"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-at"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-at", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-at"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-at"] is False and not multi_allowed:
                self.execute_dict["-at"] = option
            varformulti = option
        else:
            self.execute_dict["-at"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-at", value_to_set=varformulti
            )
        return self

    def b(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Treat debug breakpoints as exceptions (otherwise ignore them)."""
        if get_help:
            print(self.helpdict["b"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-b"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-b", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-b"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-b"] is False and not multi_allowed:
                self.execute_dict["-b"] = option
            varformulti = option
        else:
            self.execute_dict["-b"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-b", value_to_set=varformulti
            )
        return self

    def c(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """CPU threshold at which to create a dump of the process."""
        if get_help:
            print(self.helpdict["c"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-c"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-c", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-c"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-c"] is False and not multi_allowed:
                self.execute_dict["-c"] = option
            varformulti = option
        else:
            self.execute_dict["-c"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-c", value_to_set=varformulti
            )
        return self

    def cl(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """CPU threshold below which to create a dump of the process."""
        if get_help:
            print(self.helpdict["cl"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-cl"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-cl", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-cl"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-cl"] is False and not multi_allowed:
                self.execute_dict["-cl"] = option
            varformulti = option
        else:
            self.execute_dict["-cl"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-cl", value_to_set=varformulti
            )
        return self

    def d(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Invoke the minidump callback routine named MiniDumpCallbackRoutine of the specified DLL."""
        if get_help:
            print(self.helpdict["d"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-d"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-d", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-d"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-d"] is False and not multi_allowed:
                self.execute_dict["-d"] = option
            varformulti = option
        else:
            self.execute_dict["-d"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-d", value_to_set=varformulti
            )
        return self

    def e(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Write a dump when the process encounters an unhandled exception. Include the 1 to create dump on
first chance exceptions."""
        if get_help:
            print(self.helpdict["e"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-e"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-e", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-e"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-e"] is False and not multi_allowed:
                self.execute_dict["-e"] = option
            varformulti = option
        else:
            self.execute_dict["-e"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-e", value_to_set=varformulti
            )
        return self

    def f(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Filter the first chance exceptions. Wildcards (*) are supported. To just display the names without
dumping, use a blank (") filter."""
        if get_help:
            print(self.helpdict["f"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-f"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-f", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-f"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-f"] is False and not multi_allowed:
                self.execute_dict["-f"] = option
            varformulti = option
        else:
            self.execute_dict["-f"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-f", value_to_set=varformulti
            )
        return self

    def fx(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Filter (exclude) on the content of exceptions and debug logging. Wildcards are supported."""
        if get_help:
            print(self.helpdict["fx"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-fx"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-fx", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-fx"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-fx"] is False and not multi_allowed:
                self.execute_dict["-fx"] = option
            varformulti = option
        else:
            self.execute_dict["-fx"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-fx", value_to_set=varformulti
            )
        return self

    def g(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Run as a native debugger in a managed process (no interop)."""
        if get_help:
            print(self.helpdict["g"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-g"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-g", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-g"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-g"] is False and not multi_allowed:
                self.execute_dict["-g"] = option
            varformulti = option
        else:
            self.execute_dict["-g"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-g", value_to_set=varformulti
            )
        return self

    def h(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Write dump if process has a hung window (does not respond to window messages for at least 5
seconds)."""
        if get_help:
            print(self.helpdict["h"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-h"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-h", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-h"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-h"] is False and not multi_allowed:
                self.execute_dict["-h"] = option
            varformulti = option
        else:
            self.execute_dict["-h"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-h", value_to_set=varformulti
            )
        return self

    def i(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Install ProcDump as the AeDebug postmortem debugger. Only -ma, -mp, -d and -r are supported as
additional options."""
        if get_help:
            print(self.helpdict["i"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-i"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-i", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-i"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-i"] is False and not multi_allowed:
                self.execute_dict["-i"] = option
            varformulti = option
        else:
            self.execute_dict["-i"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-i", value_to_set=varformulti
            )
        return self

    def k(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Kill the process after cloning (-r), or at the end of dump collection"""
        if get_help:
            print(self.helpdict["k"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-k"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-k", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-k"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-k"] is False and not multi_allowed:
                self.execute_dict["-k"] = option
            varformulti = option
        else:
            self.execute_dict["-k"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-k", value_to_set=varformulti
            )
        return self

    def l(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Display the debug logging of the process."""
        if get_help:
            print(self.helpdict["l"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-l"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-l", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-l"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-l"] is False and not multi_allowed:
                self.execute_dict["-l"] = option
            varformulti = option
        else:
            self.execute_dict["-l"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-l", value_to_set=varformulti
            )
        return self

    def m(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Memory commit threshold in MB at which to create a dump."""
        if get_help:
            print(self.helpdict["m"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-m"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-m", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-m"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-m"] is False and not multi_allowed:
                self.execute_dict["-m"] = option
            varformulti = option
        else:
            self.execute_dict["-m"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-m", value_to_set=varformulti
            )
        return self

    def ma(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Write a dump file with all process memory. The default dump format only includes thread and handle
information."""
        if get_help:
            print(self.helpdict["ma"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-ma"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-ma", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-ma"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-ma"] is False and not multi_allowed:
                self.execute_dict["-ma"] = option
            varformulti = option
        else:
            self.execute_dict["-ma"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-ma", value_to_set=varformulti
            )
        return self

    def mc(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Write a custom dump file. Include memory defined by the specified MINIDUMP_TYPE mask (Hex)."""
        if get_help:
            print(self.helpdict["mc"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-mc"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-mc", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-mc"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-mc"] is False and not multi_allowed:
                self.execute_dict["-mc"] = option
            varformulti = option
        else:
            self.execute_dict["-mc"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-mc", value_to_set=varformulti
            )
        return self

    def md(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Write a Callback dump file. Include memory defined by the MiniDumpWriteDump callback routine named
MiniDumpCallbackRoutine of the specified DLL."""
        if get_help:
            print(self.helpdict["md"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-md"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-md", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-md"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-md"] is False and not multi_allowed:
                self.execute_dict["-md"] = option
            varformulti = option
        else:
            self.execute_dict["-md"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-md", value_to_set=varformulti
            )
        return self

    def mk(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Also write a Kernel dump file. Includes the kernel stacks of the threads in the process. OS doesn't
support a kernel dump (-mk) when using a clone (-r). When using multiple dump sizes, a kernel dump
is taken for each dump size."""
        if get_help:
            print(self.helpdict["mk"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-mk"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-mk", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-mk"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-mk"] is False and not multi_allowed:
                self.execute_dict["-mk"] = option
            varformulti = option
        else:
            self.execute_dict["-mk"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-mk", value_to_set=varformulti
            )
        return self

    def ml(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Trigger when memory commit drops below specified MB value."""
        if get_help:
            print(self.helpdict["ml"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-ml"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-ml", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-ml"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-ml"] is False and not multi_allowed:
                self.execute_dict["-ml"] = option
            varformulti = option
        else:
            self.execute_dict["-ml"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-ml", value_to_set=varformulti
            )
        return self

    def mm(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Write a mini dump file (default)."""
        if get_help:
            print(self.helpdict["mm"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-mm"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-mm", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-mm"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-mm"] is False and not multi_allowed:
                self.execute_dict["-mm"] = option
            varformulti = option
        else:
            self.execute_dict["-mm"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-mm", value_to_set=varformulti
            )
        return self

    def mp(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Write a dump file with thread and handle information, and all read/write process memory. To minimize
dump size, memory areas larger than 512MB are searched for, and if found, the largest area is
excluded. A memory area is the collection of same sized memory allocation areas. The removal of this
(cache) memory reduces Exchange and SQL Server dumps by over 90%."""
        if get_help:
            print(self.helpdict["mp"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-mp"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-mp", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-mp"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-mp"] is False and not multi_allowed:
                self.execute_dict["-mp"] = option
            varformulti = option
        else:
            self.execute_dict["-mp"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-mp", value_to_set=varformulti
            )
        return self

    def n(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Number of dumps to write before exiting."""
        if get_help:
            print(self.helpdict["n"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-n"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-n", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-n"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-n"] is False and not multi_allowed:
                self.execute_dict["-n"] = option
            varformulti = option
        else:
            self.execute_dict["-n"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-n", value_to_set=varformulti
            )
        return self

    def o(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Overwrite an existing dump file."""
        if get_help:
            print(self.helpdict["o"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-o"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-o", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-o"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-o"] is False and not multi_allowed:
                self.execute_dict["-o"] = option
            varformulti = option
        else:
            self.execute_dict["-o"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-o", value_to_set=varformulti
            )
        return self

    def p(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Trigger on the specified performance counter when the threshold is exceeded. Note: to specify a
process counter when there are multiple instances of the process running, use the process ID with
the following syntax: "\Process(<name>_<pid>)\counter"""
        if get_help:
            print(self.helpdict["p"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-p"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-p", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-p"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-p"] is False and not multi_allowed:
                self.execute_dict["-p"] = option
            varformulti = option
        else:
            self.execute_dict["-p"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-p", value_to_set=varformulti
            )
        return self

    def pl(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Trigger when performance counter falls below the specified value."""
        if get_help:
            print(self.helpdict["pl"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-pl"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-pl", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-pl"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-pl"] is False and not multi_allowed:
                self.execute_dict["-pl"] = option
            varformulti = option
        else:
            self.execute_dict["-pl"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-pl", value_to_set=varformulti
            )
        return self

    def r(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Dump using a clone. Concurrent limit is optional (default 1, max 5). CAUTION: a high concurrency
value may impact system performance. - Windows 7   : Uses Reflection. OS doesn't support -e. -
Windows 8.0 : Uses Reflection. OS doesn't support -e. - Windows 8.1+: Uses PSS. All trigger types
are supported."""
        if get_help:
            print(self.helpdict["r"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-r"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-r", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-r"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-r"] is False and not multi_allowed:
                self.execute_dict["-r"] = option
            varformulti = option
        else:
            self.execute_dict["-r"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-r", value_to_set=varformulti
            )
        return self

    def s(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Consecutive seconds before dump is written (default is 10)."""
        if get_help:
            print(self.helpdict["s"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-s"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-s", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-s"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-s"] is False and not multi_allowed:
                self.execute_dict["-s"] = option
            varformulti = option
        else:
            self.execute_dict["-s"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-s", value_to_set=varformulti
            )
        return self

    def t(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Write a dump when the process terminates."""
        if get_help:
            print(self.helpdict["t"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-t"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-t", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-t"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-t"] is False and not multi_allowed:
                self.execute_dict["-t"] = option
            varformulti = option
        else:
            self.execute_dict["-t"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-t", value_to_set=varformulti
            )
        return self

    def u(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Treat CPU usage relative to a single core (used with -c). As the only option, Uninstalls ProcDump as
the postmortem debugger."""
        if get_help:
            print(self.helpdict["u"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-u"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-u", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-u"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-u"] is False and not multi_allowed:
                self.execute_dict["-u"] = option
            varformulti = option
        else:
            self.execute_dict["-u"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-u", value_to_set=varformulti
            )
        return self

    def w(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Wait for the specified process to launch if it's not running."""
        if get_help:
            print(self.helpdict["w"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-w"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-w", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-w"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-w"] is False and not multi_allowed:
                self.execute_dict["-w"] = option
            varformulti = option
        else:
            self.execute_dict["-w"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-w", value_to_set=varformulti
            )
        return self

    def wer(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Queue the (largest) dump to Windows Error Reporting."""
        if get_help:
            print(self.helpdict["wer"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-wer"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-wer", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-wer"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-wer"] is False and not multi_allowed:
                self.execute_dict["-wer"] = option
            varformulti = option
        else:
            self.execute_dict["-wer"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-wer", value_to_set=varformulti
            )
        return self

    def x(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """Launch the specified image with optional arguments. If it is a Store Application or Package,
ProcDump will start on the next activation (only)."""
        if get_help:
            print(self.helpdict["x"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-x"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-x", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-x"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-x"] is False and not multi_allowed:
                self.execute_dict["-x"] = option
            varformulti = option
        else:
            self.execute_dict["-x"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-x", value_to_set=varformulti
            )
        return self

    def NO_64(self, option=None, activated=True, multi_allowed=False, get_help=False):
        """By default ProcDump will capture a 32-bit dump of a 32-bit process when running on 64-bit Windows.
This option overrides to create a 64-bit dump. Only use for WOW64 subsystem debugging."""
        if get_help:
            print(self.helpdict["NO_64"])
            return self
        varformulti = ""
        if not activated:
            self.execute_dict["-64"] = False
            if multi_allowed:
                self._handle_multiple_times_same_flag(
                    key_to_check="-64", value_to_set=False
                )
            return self
        if isinstance(option, bool):
            self._print_option_activate_warning()
            self.execute_dict["-64"] = True
            varformulti = True

        elif option is not None and activated:
            if self.execute_dict["-64"] is False and not multi_allowed:
                self.execute_dict["-64"] = option
            varformulti = option
        else:
            self.execute_dict["-64"] = True
            varformulti = True
        if multi_allowed:
            self._handle_multiple_times_same_flag(
                key_to_check="-64", value_to_set=varformulti
            )
        return self


if __name__ == "__main__":
    dumpfile = r"C:\MiniDumpWithFullMemoryx.dmp"
    pid = 16544
    createdump = False
    if createdump:
        erg = (
            ProcDump(executeable=r"C:\Program Files\procdump.exe")
            .o()
            .ma()
            .add_own_parameter_or_option(f"{pid}")
            .add_target_file_or_folder([dumpfile])
            .run()
        )
