import gdb

bps = list()
colors = {
    "normal"               : "\033[0m",
    "bold"                 : "\033[1m",
    "bold_off"             : "\033[21m",
    "highlight"            : "\033[2m",
    "highlight_off"        : "\033[22m",
    "italic"               : "\033[3m",
    "italic_off"           : "\033[23m",
    "underline"            : "\033[4m",
    "underline_off"        : "\033[24m",
    "blink"                : "\033[5m",
    "blink_off"            : "\033[25m",
    "black"                : "\033[30m",
    "red"                  : "\033[31m",
    "green"                : "\033[32m",
    "yellow"               : "\033[33m",
    "blue"                 : "\033[34m",
    "magenta"              : "\033[35m",
    "cyan"                 : "\033[36m",
    "bright_black"         : "\033[90m",
    "bright_red"           : "\033[91m",
    "bright_green"         : "\033[92m",
    "bright_yellow"        : "\033[93m",
    "bright_blue"          : "\033[94m",
    "bright_magenta"       : "\033[95m",
    "bright_cyan"          : "\033[96m",
    "bright_white"         : "\033[97m",
    "coral_red"            : "\033[38;2;239;133;125m",
    "sunshine_yellow"      : "\033[38;2;255;237;171m",
    "ice_green"            : "\033[38;2;163;214;204m",
    "wistaria"             : "\033[38;2;141;147;200m",
    "pink_almond"          : "\033[38;2;227;172;174m",
    "poppy_red"            : "\033[38;2;234;85;80m",
    "cream_yellow"         : "\033[38;2;255;243;184m",
    "turquoise_green"      : "\033[38;2;0;148;122m",
    "white"                : "\033[38;2;255;255;255m",
}

class TraceBreakpoint(gdb.Breakpoint):
    def __init__(self, spec, callback):
        super(TraceBreakpoint, self).__init__(spec)
        self.silent = True
        self.callback = callback
    def stop(self):
        exec(self.callback)
        return False
    def __del__(self):
        self.delete()


class TraceFunction(gdb.Breakpoint):
    global colors
    def __init__(self, spec, trace_ret, argc):
        super(TraceFunction, self).__init__(spec)
        self.silent = True
        self.name = spec
        self.trace_ret = trace_ret
        self.color = colors['green'] + colors['bold']
        self.argc = argc
        self.calling_conv = ["$rdi", "$rsi", "$rdx", "$rcx", "$r8", "$r9"]

    def stop(self):
        args = []
        for i in range(self.argc):
            args.append(gdb.parse_and_eval(self.calling_conv[i]))
        ret = int(gdb.parse_and_eval("*(long *)($rsp)"))
        if self.trace_ret:
            callback = f'ret = gdb.parse_and_eval("$rax")\nprint(f"{self.color}[+]     {self.name} return {{hex(ret)}}")\nprint("{colors["white"] + colors["normal"]}",end="")'
            TraceBreakpoint("*"+hex(ret), callback)  
        arg_str = ''
        for i in args:
            arg_str += hex(i) + ", "
        arg_str = arg_str[:-2]
        print(f"{self.color}[+] {self.name}({arg_str})")
        print(colors['white'] + colors['normal'], end='')
        return False

TraceFunction("malloc", True, 1)
TraceFunction("free", False, 1)
TraceFunction('realloc', True, 2)

