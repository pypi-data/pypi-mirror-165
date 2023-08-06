class Parse_Args(object):
    def __init__(self, cmd: str) -> None:
        self.msg = cmd[:]

        self.cmd = self.msg.split(" ")[1:]

        self.command = self.cmd[0]

        self.subcommands = [arg for arg in self.cmd[1:] if arg[0] != "-"]

        if len(self.subcommands) > 1:
            self.variables = self.subcommands[1:]
        else:
            self.variables = None

        self.flags = [arg[1:] for arg in self.cmd if arg[0] == "-"]
