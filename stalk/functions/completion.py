def complete(output, cmdline, point=None):
    if point is None:
        point = len(cmdline)
    args = cmdline[0:point].split()
    current_arg = args[-1]
    current_arg_point = len(current_arg)
    cmd_args = [x for x in args if not x.startswith("-")]
    opts = ["add", "chat", "file"]
    if len(cmd_args) <= 2:
        if current_arg == "add":
            # Call camera
            pass
        elif current_arg == "chat":
            print(" \n".join(["server", "client"]))
        elif current_arg == "file":
            # List files and dirs under the current dir
            pass
        elif current_arg == "stalk":
            print(" \n".join(opts))
        else:
            # Return matched opts
            opts_matched = []
            for x in opts:
                if x.startswith(current_arg):
                    opts_matched.append(x + " ")
            print(" \n".join(opts_matched))
    elif len(cmd_args) > 2:
        if current_arg in ["server", "client"]:
            return 0

        bucket_list = []
        if len(cmd_args) == 4:
            # Avoid more completions
            for x in output["buckets"]:
                if x["name"].encode("utf-8") in cmd_args[-1]:
                    return 0
        if cmd_args[1] in ["ls", "mb", "rb", "rm", "presign"]:
            # If the cmd needs only one bucket
            for x in output["buckets"]:
                for w in cmd_args:
                    if x["name"].encode("utf-8") in w:
                        return 0
        if current_arg not in qs_path:
            # Input bucket without "qs://"
            for x in output["buckets"]:
                if x["name"].encode("utf-8").startswith(current_arg):
                    bucket_list.append((x["name"] + "/").encode("utf-8"))
            print(" \n".join(bucket_list))
        else:
            # Input bucket with "qs://"
            for x in output["buckets"]:
                if x["name"].encode("utf-8").startswith(
                        current_arg[5:current_arg_point + 1]
                ):
                    bucket_list.append(("//" + x["name"] + "/").encode("utf-8"))
            print(" \n".join(bucket_list))
    else:
        return 0
