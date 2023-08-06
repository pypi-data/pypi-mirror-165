#wrapper for https://github.com/FastCopyLab/FastCopy

import subprocess
from tempfile import SpooledTemporaryFile as tempfile
from typing import Union, Any


class FastCopy:
    def __init__(self, executeable=r"fcp.exe"):
        self.executeable = executeable
        self.necessary_beginning = [self.executeable]
        self.options_parameters = {
            "cmd_noexist_only": "/cmd=noexist_only",
            "cmd_diff": "/cmd=diff",
            "cmd_update": "/cmd=update",
            "cmd_force_copy": "/cmd=force_copy",
            "cmd_sync": "/cmd=sync",
            "cmd_move": "/cmd=move",
            "cmd_delete": "/cmd=delete",
            "auto_close": "/auto_close",
            "force_close": "/force_close",
            "open_window": "/open_window",
            "estimate": "/estimate",
            "balloon": "/balloon",
            "no_ui": "/no_ui",
            "no_confirm_del": "/no_confirm_del",
            "no_confirm_stop": "/no_confirm_stop",
            "no_exec": "/no_exec",
            "error_stop": "/error_stop",
            "bufsize": "/bufsize",
            "log": "/log",
            "logfile": "/logfile",
            "filelog": "/filelog",
            "skip_empty_dir": "/skip_empty_dir",
            "job": "/job",
            "force_start": "/force_start",
            "disk_mode": "/disk_mode",
            "speed": "/speed",
            "low_io": "/low_io",
            "srcfile": "/srcfile",
            "srcfile_w": "/srcfile_w",
            "include": "/include",
            "exclude": "/exclude",
            "from_date": "/from_date",
            "to": "/to",
            "to_date": "/to_date",
            "min_size": "/min_size",
            "max_size": "/max_size",
            "time_allow": "/time_allow",
            "wipe_del": "/wipe_del",
            "acl": "/acl",
            "stream": "/stream",
            "reparse": "/reparse",
            "verify": "/verify",
            "verifyinfo": "/verifyinfo",
            "dlsvt": "/dlsvt",
            "linkdest": "/linkdest",
            "recreate": "/recreate",
            "postproc": "/postproc",
        }
        self.execute_dict = {
            "/cmd_noexist_only": False,
            "/cmd_diff": False,
            "/cmd_update": False,
            "/cmd_force_copy": False,
            "/cmd_sync": False,
            "/cmd_move": False,
            "/cmd_delete": False,
            "/auto_close": False,
            "/force_close": False,
            "/open_window": False,
            "/estimate": False,
            "/balloon": False,
            "/no_ui": False,
            "/no_confirm_del": False,
            "/no_confirm_stop": False,
            "/no_exec": False,
            "/error_stop": False,
            "/bufsize": False,
            "/log": False,
            "/logfile": False,
            "/filelog": False,
            "/skip_empty_dir": False,
            "/job": False,
            "/force_start": False,
            "/disk_mode": False,
            "/speed": False,
            "/low_io": False,
            "/srcfile": False,
            "/srcfile_w": False,
            "/include": False,
            "/exclude": False,
            "/from_date": False,
            "/to_date": False,
            "/to": False,
            "/min_size": False,
            "/max_size": False,
            "/time_allow": False,
            "/wipe_del": False,
            "/acl": False,
            "/stream": False,
            "/reparse": False,
            "/verify": False,
            "/verifyinfo": False,
            "/dlsvt": False,
            "/linkdest": False,
            "/recreate": False,
            "/postproc": False,
        }
        self.execute_command = {}
        self.helpdict = {
            "cmd_noexist_only": "Specify operation mode. (By default, diff mode is used.) Diff (No Overwrite)",
            "cmd_diff": "Specify operation mode. (By default, diff mode is used.) Diff (Size/date)",
            "cmd_update": "Specify operation mode. (By default, diff mode is used.) Diff (update)",
            "cmd_force_copy": "Specify operation mode. (By default, diff mode is used.) Copy (Overwrite)",
            "cmd_sync": "Specify operation mode. (By default, diff mode is used.) Sync (Size/date)",
            "cmd_move": "Specify operation mode. (By default, diff mode is used.) Move (Overwrite)",
            "cmd_delete": 'If delete mode is specified, then "/to=desit_dir" is not used.',
            "auto_close": "Close automatically after execution is finished with no errors.",
            "force_close": "Close automatically and forcibly after execution is finished.",
            "open_window": "It will not be stored in the task notification area.",
            "estimate": "Estimate complete time.(to disable, /estimate=FALSE)",
            "balloon": "Show balloon notification at finish. (to disable, /balloon=FALSE)",
            "no_ui": "Dialog box will not be shown. This is for background tasks. If /no_ui is used, /no_confirm_del\n/no_confirm_stop /force_close are set automatically. If FastCopy runs in session 0 (e.g. running\nwith task scheduler), /no_ui is set automatically. However even if /no_ui is set,\nstandby/hibernate/shutdown countdown dialog will not be prevented.",
            "no_confirm_del": "Don't confirm before deleting.",
            "no_confirm_stop": "Don't show error dialog, even if critical errors occur.",
            "no_exec": "Don't start to execute.",
            "error_stop": "Show error dialog (and operation is interrupted), if an error occurs. (to disable,\n/error_stop=FALSE)",
            "bufsize": "Specify the size(MB) of the main buffer for Read/Write operation. N(MB)",
            "log": "Write the operation/errors information to the logfile(FastCopy.log). (to disable, /log=FALSE)",
            "logfile": "Specify the filename of logfile. =filename",
            "filelog": "Write to the filelog(detail of copy/delete files). It is stored TIMESTAMP.log in FastCopy/Log\ndirectory. If using verify mode, write digest data as additional data. (To specify filelogname,\n/filelog=filename)",
            "skip_empty_dir": "Skip to create empty directories when /include or /exclude option is used. (to disable,\n/skip_empty_dir=FALSE)",
            "job": "Specify the job that is already registered.  =job_name",
            "force_start": "Start at once without waiting for the finish of other FastCopy executing. (/force_start=2-N ...\nspecify number of max parallel process) (=N)",
            "disk_mode": "Specify Auto/Same/Diff HDD mode. (default: Auto)  =(auto|same|diff)",
            "speed": "Specify speed control level.  =(full|autoslow| 9-1(90%-10%)|suspend)",
            "low_io": "Prioritize IO for other apps(to disable, /low_io=FALSE)",
            "srcfile": 'Specify source files by textfile with UTF-8. User is able to describe 1 filename per line.\n(Attention:We don\'t recommend specifying a lot of files ="files.txt"',
            "srcfile_w": 'same as "/srcfile=", except describing with UTF-16. ="files.txt"',
            "include": 'Specify Include filter. (details) ="..."',
            "exclude": 'Specify Exclude filter. (details) ="..."',
            "from_date": "Specify oldest timestamp filter. (details)",
            "to_date": "Specify newest timestamp filter. (details)",
            "to": "Destination",
            "min_size": 'Specify minimum size filter. (details) ="..."',
            "max_size": 'Specify maximum size filter. (details) ="..."',
            "time_allow": "Specify tolerance timestamp difference(ms) as same date in Diff(Date/Size) or Diff(Newer). =N(ms)",
            "wipe_del": "Rename filename and wipe(overwrite Random data) before deleting.",
            "acl": "Copy ACL/EA (only NTFS)(to disable, /acl=FALSE)",
            "stream": "Copy Alternate Stream (only NTFS) (to disable, /stream=FALSE)",
            "reparse": "Copy junction/mountpoint/symlink itself(to disable, /reparse=FALSE) (details)",
            "verify": "Verify written files data by xxHash3(MD5/SHA-1/SHA-256/xxHash) (to disable, /verify=FALSE) (details)",
            "verifyinfo": "Enable VeriyInfo to the AltStream (:fc_verify) option (to disable, /veriyinfo=FALSE)",
            "dlsvt": "Specify Daylight Saving Time grace (details) =(none|auto|always)",
            "linkdest": "Reproduce hardlink as much as possible. (details)",
            "recreate": 'Change updating behavior "overwrite the target" to "delete and recreate the target". (If /linkdest\noption is enabled, this option is enabled by default.) If you want always to enable, write [main]\nrecreate=1 in FastCopy2.ini.',
            "postproc": "Specify post-process action name (to disable, /postproc=FALSE) =action_name",
        }
        self.target_file_or_folder = []
        self.target_value = []
        self.self_added_arguments = []
        self.last_command_line_called = []

    def add_target_file_or_folder(self, target_file_or_folder: Union[str, list]):
        if isinstance(target_file_or_folder, str):
            target_file_or_folder = [target_file_or_folder]
        self.target_file_or_folder.extend(target_file_or_folder)
        return self

    def print_options_to_screen(self):
        for help, exe in zip(self.helpdict.items(), self.execute_dict.items()):
            key_h, item_h = help
            key_e, item_e = exe
            print(f"Parameter:\t\t\t{key_e} {key_h}")
            print(f"Current Settings:\t\t`{item_e}` (False=not activated)")
            print(f"Information:\t\t{item_h}")
            print(
                "---------------------------------------------------------------------------------------------"
            )
        print(f"Self Added Arguments:\t\tf{self.self_added_arguments}")
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

    def _add_to_execute_command_dict(self, key, value, join=False):
        newkey = 0
        while newkey in self.execute_command:
            newkey = newkey + 1
        if not join:
            self.execute_command[newkey] = [str(key), str(value)]
        else:
            self.execute_command[newkey] = [f"{key}{value}"]

    def _prepare_tmp_file(self, variable):
        f = tempfile()
        f.write(variable)
        f.seek(0)
        return f

    def _prepare_commandline(self):
        return (
            [self.executeable]
            + FastCopy.flatten_iter([x[1] for x in self.execute_command.items()])
            + self.target_file_or_folder
            + self.target_value
        )

    def check_if_bytes(self, cmdline, element=-1):
        return isinstance(cmdline[element], bytes)

    def r_subprocess_popen_shell(self):
        cmdline = self._prepare_commandline()
        print(cmdline)
        if self.check_if_bytes(cmdline):
            f = self._prepare_tmp_file(cmdline[-1])
            ergebnis = subprocess.Popen(
                cmdline[:-1], shell=True, stdin=f, stdout=subprocess.PIPE,
            )
            f.close()
            self.last_command_line_called = cmdline[:-1].copy()
        else:
            ergebnis = subprocess.Popen(
                cmdline, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            )
            self.last_command_line_called = cmdline.copy()
        return ergebnis

    def r_subprocess_popen(self):
        cmdline = self._prepare_commandline()
        if self.check_if_bytes(cmdline):
            f = self._prepare_tmp_file(cmdline[-1])
            ergebnis = subprocess.Popen(
                cmdline[:-1], shell=True, stdin=f, stdout=subprocess.PIPE,
            )
            f.close()
            self.last_command_line_called = cmdline[:-1].copy()
        else:
            ergebnis = subprocess.Popen(
                cmdline, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            )
            self.last_command_line_called = cmdline.copy()
        return ergebnis

    def r_subprocess_run_shell_to_file(self, filepath):
        cmdline = self._prepare_commandline()
        if self.check_if_bytes(cmdline):
            f = self._prepare_tmp_file(cmdline[-1])
            ergebnis = subprocess.run(
                cmdline[:-1] + [f">>", filepath],
                shell=True,
                stdin=f,
                capture_output=False,
            )
            f.close()
            self.last_command_line_called = cmdline[:-1].copy()
        else:
            ergebnis = subprocess.run(
                cmdline + [f">>", filepath], shell=True, capture_output=False
            )
            self.last_command_line_called = cmdline.copy()
        return ergebnis

    def r_subprocess_run(self, capture_output=True):
        cmdline = self._prepare_commandline()
        print(cmdline)
        if self.check_if_bytes(cmdline):
            f = self._prepare_tmp_file(cmdline[-1])
            ergebnis = subprocess.run(
                cmdline[:-1], shell=False, stdin=f, capture_output=capture_output
            )
            f.close()
            self.last_command_line_called = cmdline[:-1].copy()
        else:
            ergebnis = subprocess.run(
                cmdline, shell=False, capture_output=capture_output
            )
            self.last_command_line_called = cmdline.copy()
        return ergebnis

    def add_own(self, parameter, value: Union[Any] = True, join_value=False):
        if value is True:
            self._add_to_execute_command_dict(parameter, "", join=True)
        else:
            self._add_to_execute_command_dict(parameter, value, join=join_value)
        return self

    def cmd_noexist_only(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Specify operation mode. (By default, diff mode is used.) Diff (No Overwrite)"""
        if get_help:
            print(self.helpdict["cmd_noexist_only"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/cmd=noexist_only", "", join=True)
        else:
            self._add_to_execute_command_dict(
                "/cmd_noexist=only", f"{value}", join=join_value
            )
        return self

    def cmd_diff(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Specify operation mode. (By default, diff mode is used.) Diff (Size/date)"""
        if get_help:
            print(self.helpdict["cmd_diff"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/cmd=diff", "", join=True)
        else:
            self._add_to_execute_command_dict("/cmd=diff", f"{value}", join=join_value)
        return self

    def cmd_update(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Specify operation mode. (By default, diff mode is used.) Diff (update)"""
        if get_help:
            print(self.helpdict["cmd_update"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/cmd=update", "", join=True)
        else:
            self._add_to_execute_command_dict(
                "/cmd=update", f"{value}", join=join_value
            )
        return self

    def cmd_force_copy(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Specify operation mode. (By default, diff mode is used.) Copy (Overwrite)"""
        if get_help:
            print(self.helpdict["cmd_force_copy"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/cmd=force_copy", "", join=True)
        else:
            self._add_to_execute_command_dict(
                "/cmd=force_copy", f"{value}", join=join_value
            )
        return self

    def cmd_sync(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Specify operation mode. (By default, diff mode is used.) Sync (Size/date)"""
        if get_help:
            print(self.helpdict["cmd_sync"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/cmd=sync", "", join=True)
        else:
            self._add_to_execute_command_dict("/cmd=sync", f"{value}", join=join_value)
        return self

    def cmd_move(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Specify operation mode. (By default, diff mode is used.) Move (Overwrite)"""
        if get_help:
            print(self.helpdict["cmd_move"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/cmd=move", "", join=True)
        else:
            self._add_to_execute_command_dict("/cmd=move", f"{value}", join=join_value)
        return self

    def cmd_delete(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """If delete mode is specified, then "/to=desit_dir" is not used."""
        if get_help:
            print(self.helpdict["cmd_delete"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/cmd=delete", "", join=True)
        else:
            self._add_to_execute_command_dict(
                "/cmd=delete", f"{value}", join=join_value
            )
        return self

    def auto_close(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Close automatically after execution is finished with no errors."""
        if get_help:
            print(self.helpdict["auto_close"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/auto_close", "", join=True)
        else:
            self._add_to_execute_command_dict("/auto_close", value, join=join_value)
        return self

    def force_close(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Close automatically and forcibly after execution is finished."""
        if get_help:
            print(self.helpdict["force_close"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/force_close", "", join=True)
        else:
            self._add_to_execute_command_dict("/force_close", value, join=join_value)
        return self

    def open_window(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """It will not be stored in the task notification area."""
        if get_help:
            print(self.helpdict["open_window"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/open_window", "", join=True)
        else:
            self._add_to_execute_command_dict("/open_window", value, join=join_value)
        return self

    def estimate(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Estimate complete time.(to disable, /estimate=FALSE)"""
        if get_help:
            print(self.helpdict["estimate"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/estimate", "", join=True)
        else:
            self._add_to_execute_command_dict("/estimate", value, join=join_value)
        return self

    def balloon_off(self, value="FALSE", join_value=True, get_help: bool = False):
        """Show balloon notification at finish. (to disable, /balloon=FALSE)"""
        if get_help:
            print(self.helpdict["balloon"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/balloon", "", join=True)
        else:
            self._add_to_execute_command_dict("/balloon", value, join=join_value)
        return self

    def no_ui(self, value: Union[Any] = True, join_value=False, get_help: bool = False):
        """Dialog box will not be shown. This is for background tasks. If /no_ui is used, /no_confirm_del
        /no_confirm_stop /force_close are set automatically. If FastCopy runs in session 0 (e.g. running
        with task scheduler), /no_ui is set automatically. However even if /no_ui is set,
        standby/hibernate/shutdown countdown dialog will not be prevented."""
        if get_help:
            print(self.helpdict["no_ui"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/no_ui", "", join=True)
        else:
            self._add_to_execute_command_dict("/no_ui", value, join=join_value)
        return self

    def no_confirm_del(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Don't confirm before deleting."""
        if get_help:
            print(self.helpdict["no_confirm_del"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/no_confirm_del", "", join=True)
        else:
            self._add_to_execute_command_dict("/no_confirm_del", value, join=join_value)
        return self

    def no_confirm_stop(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Don't show error dialog, even if critical errors occur."""
        if get_help:
            print(self.helpdict["no_confirm_stop"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/no_confirm_stop", "", join=True)
        else:
            self._add_to_execute_command_dict(
                "/no_confirm_stop", value, join=join_value
            )
        return self

    def no_exec(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Don't start to execute."""
        if get_help:
            print(self.helpdict["no_exec"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/no_exec", "", join=True)
        else:
            self._add_to_execute_command_dict("/no_exec", value, join=join_value)
        return self

    def error_stop(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Show error dialog (and operation is interrupted), if an error occurs. (to disable,
        /error_stop=FALSE)"""
        if get_help:
            print(self.helpdict["error_stop"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/error_stop", "", join=True)
        else:
            self._add_to_execute_command_dict("/error_stop", value, join=join_value)
        return self

    def bufsize(
        self, value: Union[Any] = True, join_value=True, get_help: bool = False
    ):
        """Specify the size(MB) of the main buffer for Read/Write operation. N(MB)"""
        if get_help:
            print(self.helpdict["bufsize"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/bufsize", "", join=True)
        else:
            self._add_to_execute_command_dict("/bufsize", f"={value}", join=join_value)
        return self

    def log(self, value: Union[Any] = True, join_value=False, get_help: bool = False):
        """Write the operation/errors information to the logfile(FastCopy.log). (to disable, /log=FALSE)"""
        if get_help:
            print(self.helpdict["log"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/log", "", join=True)
        else:
            self._add_to_execute_command_dict("/log", value, join=join_value)
        return self

    def logfile(
        self, value: Union[Any] = True, join_value=True, get_help: bool = False
    ):
        """Specify the filename of logfile. =filename"""
        if get_help:
            print(self.helpdict["logfile"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/logfile", "", join=True)
        else:
            self._add_to_execute_command_dict("/logfile", f"={value}", join=join_value)
        return self

    def filelog(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Write to the filelog(detail of copy/delete files). It is stored TIMESTAMP.log in FastCopy/Log
        directory. If using verify mode, write digest data as additional data. (To specify filelogname,
        /filelog=filename)"""
        if get_help:
            print(self.helpdict["filelog"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/filelog", "", join=True)
        else:
            self._add_to_execute_command_dict("/filelog", value, join=join_value)
        return self

    def skip_empty_dir(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Skip to create empty directories when /include or /exclude option is used. (to disable,
        /skip_empty_dir=FALSE)"""
        if get_help:
            print(self.helpdict["skip_empty_dir"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/skip_empty_dir", "", join=True)
        else:
            self._add_to_execute_command_dict("/skip_empty_dir", value, join=join_value)
        return self

    def job(self, value: Union[Any] = True, join_value=True, get_help: bool = False):
        """Specify the job that is already registered.  =job_name"""
        if get_help:
            print(self.helpdict["job"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/job", "", join=True)
        else:
            self._add_to_execute_command_dict("/job", f"={value}", join=join_value)
        return self

    def force_start(
        self, value: Union[Any] = True, join_value=True, get_help: bool = False
    ):
        """Start at once without waiting for the finish of other FastCopy executing. (/force_start=2-N ...
        specify number of max parallel process) (=N)"""
        if get_help:
            print(self.helpdict["force_start"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/force_start", "", join=True)
        else:
            self._add_to_execute_command_dict(
                "/force_start", f"={value}", join=join_value
            )
        return self

    def disk_mode(
        self, value: Union[Any] = True, join_value=True, get_help: bool = False
    ):
        """Specify Auto/Same/Diff HDD mode. (default: Auto)  =(auto|same|diff)"""
        if get_help:
            print(self.helpdict["disk_mode"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/disk_mode", "", join=True)
        else:
            self._add_to_execute_command_dict(
                "/disk_mode", f"={value}", join=join_value
            )
        return self

    def speed(self, value: Union[Any] = True, join_value=True, get_help: bool = False):
        """Specify speed control level.  =(full|autoslow| 9-1(90%-10%)|suspend)"""
        if get_help:
            print(self.helpdict["speed"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/speed", "", join=True)
        else:
            self._add_to_execute_command_dict("/speed", f"={value}", join=join_value)
        return self

    def low_io(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Prioritize IO for other apps(to disable, /low_io=FALSE)"""
        if get_help:
            print(self.helpdict["low_io"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/low_io", "", join=True)
        else:
            self._add_to_execute_command_dict("/low_io", value, join=join_value)
        return self

    def srcfile(
        self, value: Union[Any] = True, join_value=True, get_help: bool = False
    ):
        """Specify source files by textfile with UTF-8. User is able to describe 1 filename per line.
        (Attention:We don't recommend specifying a lot of files ="files.txt"""
        if get_help:
            print(self.helpdict["srcfile"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/srcfile", "", join=True)
        else:
            self._add_to_execute_command_dict("/srcfile", f"={value}", join=join_value)
        return self

    def srcfile_w(
        self, value: Union[Any] = True, join_value=True, get_help: bool = False
    ):
        """same as "/srcfile=", except describing with UTF-16. ="files.txt"""
        if get_help:
            print(self.helpdict["srcfile_w"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/srcfile_w", "", join=True)
        else:
            self._add_to_execute_command_dict(
                "/srcfile_w", f"={value}", join=join_value
            )
        return self

    def include(
        self, value: Union[Any] = True, join_value=True, get_help: bool = False
    ):
        """Specify Include filter. (details) ="..."""
        if get_help:
            print(self.helpdict["include"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/include", "", join=True)
        else:
            self._add_to_execute_command_dict("/include", f"={value}", join=join_value)
        return self

    def exclude(
        self, value: Union[Any] = True, join_value=True, get_help: bool = False
    ):
        """Specify Exclude filter. (details) ="..."""
        if get_help:
            print(self.helpdict["exclude"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/exclude", "", join=True)
        else:
            self._add_to_execute_command_dict("/exclude", f"={value}", join=join_value)
        return self

    def from_date(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Specify oldest timestamp filter. (details)"""
        if get_help:
            print(self.helpdict["from_date"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/from_date", "", join=True)
        else:
            self._add_to_execute_command_dict("/from_date", value, join=join_value)
        return self

    def to_date(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Specify newest timestamp filter. (details)"""
        if get_help:
            print(self.helpdict["to_date"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/to_date", "", join=True)
        else:
            self._add_to_execute_command_dict("/to_date", value, join=join_value)
        return self

    def min_size(
        self, value: Union[Any] = True, join_value=True, get_help: bool = False
    ):
        """Specify minimum size filter. (details) ="..."""
        if get_help:
            print(self.helpdict["min_size"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/min_size", "", join=True)
        else:
            self._add_to_execute_command_dict("/min_size", f"={value}", join=join_value)
        return self

    def max_size(
        self, value: Union[Any] = True, join_value=True, get_help: bool = False
    ):
        """Specify maximum size filter. (details) ="..."""
        if get_help:
            print(self.helpdict["max_size"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/max_size", "", join=True)
        else:
            self._add_to_execute_command_dict("/max_size", f"={value}", join=join_value)
        return self

    def time_allow(
        self, value: Union[Any] = True, join_value=True, get_help: bool = False
    ):
        """Specify tolerance timestamp difference(ms) as same date in Diff(Date/Size) or Diff(Newer). =N(ms)"""
        if get_help:
            print(self.helpdict["time_allow"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/time_allow", "", join=True)
        else:
            self._add_to_execute_command_dict(
                "/time_allow", f"={value}", join=join_value
            )
        return self

    def wipe_del(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Rename filename and wipe(overwrite Random data) before deleting."""
        if get_help:
            print(self.helpdict["wipe_del"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/wipe_del", "", join=True)
        else:
            self._add_to_execute_command_dict("/wipe_del", value, join=join_value)
        return self

    def acl(self, value: Union[Any] = True, join_value=False, get_help: bool = False):
        """Copy ACL/EA (only NTFS)(to disable, /acl=FALSE)"""
        if get_help:
            print(self.helpdict["acl"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/acl", "", join=True)
        else:
            self._add_to_execute_command_dict("/acl", value, join=join_value)
        return self

    def stream(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Copy Alternate Stream (only NTFS) (to disable, /stream=FALSE)"""
        if get_help:
            print(self.helpdict["stream"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/stream", "", join=True)
        else:
            self._add_to_execute_command_dict("/stream", value, join=join_value)
        return self

    def reparse(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Copy junction/mountpoint/symlink itself(to disable, /reparse=FALSE) (details)"""
        if get_help:
            print(self.helpdict["reparse"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/reparse", "", join=True)
        else:
            self._add_to_execute_command_dict("/reparse", value, join=join_value)
        return self

    def verify(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Verify written files data by xxHash3(MD5/SHA-1/SHA-256/xxHash) (to disable, /verify=FALSE) (details)"""
        if get_help:
            print(self.helpdict["verify"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/verify", "", join=True)
        else:
            self._add_to_execute_command_dict("/verify", value, join=join_value)
        return self

    def verifyinfo(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Enable VeriyInfo to the AltStream (:fc_verify) option (to disable, /veriyinfo=FALSE)"""
        if get_help:
            print(self.helpdict["verifyinfo"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/verifyinfo", "", join=True)
        else:
            self._add_to_execute_command_dict("/verifyinfo", value, join=join_value)
        return self

    def dlsvt(self, value: Union[Any] = True, join_value=True, get_help: bool = False):
        """Specify Daylight Saving Time grace (details) =(none|auto|always)"""
        if get_help:
            print(self.helpdict["dlsvt"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/dlsvt", "", join=True)
        else:
            self._add_to_execute_command_dict("/dlsvt", f"={value}", join=join_value)
        return self

    def linkdest(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Reproduce hardlink as much as possible. (details)"""
        if get_help:
            print(self.helpdict["linkdest"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/linkdest", "", join=True)
        else:
            self._add_to_execute_command_dict("/linkdest", value, join=join_value)
        return self

    def recreate(
        self, value: Union[Any] = True, join_value=False, get_help: bool = False
    ):
        """Change updating behavior "overwrite the target" to "delete and recreate the target". (If /linkdest
        option is enabled, this option is enabled by default.) If you want always to enable, write [main]
        recreate=1 in FastCopy2.ini."""
        if get_help:
            print(self.helpdict["recreate"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/recreate", "", join=True)
        else:
            self._add_to_execute_command_dict("/recreate", value, join=join_value)
        return self

    def postproc(
        self, value: Union[Any] = True, join_value=True, get_help: bool = False
    ):
        """Specify post-process action name (to disable, /postproc=FALSE) =action_name"""
        if get_help:
            print(self.helpdict["postproc"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/postproc", "", join=True)
        else:
            self._add_to_execute_command_dict("/postproc", f"={value}", join=join_value)
        return self

    def to(self, value: Union[Any] = True, join_value=True, get_help: bool = False):
        """Specify post-process action name (to disable, /postproc=FALSE) =action_name"""
        if get_help:
            print(self.helpdict["to"])
            return self

        if value is True:
            self._add_to_execute_command_dict("/to", "", join=True)
        else:
            self._add_to_execute_command_dict("/to", f"={value}", join=join_value)
        return self


if __name__ == "__main__":
    test = False
    if test:
        pathfastcopy = r"C:\path\fcp.exe"
        path1 = "c:\\blabla"
        path2 = "c:\\blabla2"

        asz = (
            FastCopy(pathfastcopy)
            .force_close()
            .no_confirm_del()
            .force_start()
            .error_stop("=FALSE", join_value=True)
            .speed("full")
            .log("=FALSE", join_value=True)
            # .srcfile(tmpfile)
            .to(path2)
            .cmd_diff(path1)
            .r_subprocess_run()
        )

        for xx in asz.stdout.decode("utf-8", "ignore").splitlines():
            print(xx)
