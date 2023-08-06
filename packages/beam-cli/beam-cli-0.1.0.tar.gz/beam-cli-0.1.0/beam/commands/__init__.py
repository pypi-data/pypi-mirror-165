class CommandTypes:
    READY = "READY"
    RUN_COMMAND = "RUN_COMMAND"
    STDIN = "STDIN"
    TYPES = (
        (READY, "ready"),
        (RUN_COMMAND, "run_command"),
        (STDIN, "stdin"),
    )
