import os
import sys
import errno
import signal
import argparse


class BaseCommand(object):
    command = ""
    usage = ""
    description = ""

    options = None

    @classmethod
    def add_common_arguments(cls, parser):
        parser.add_argument(
            "-c",
            "--config",
            dest="config",
            action="store",
            type=str,
            default="~/.qingstor/config.yaml",
            help="Configuration file"
        )
        parser.add_argument(
            "-z",
            "--zone",
            dest="zone",
            action="store",
            type=str,
            help="In which zone to do the operation"
        )

    @classmethod
    def add_extra_arguments(cls, parser):
        pass

    @classmethod
    def add_transfer_arguments(cls, parser):
        pass

    @classmethod
    def get_argument_parser(cls):
        parser = argparse.ArgumentParser(
            prog="qsctl %s" % cls.command,
            usage=cls.usage,
            description=cls.description
        )
        cls.add_common_arguments(parser)
        cls.add_extra_arguments(parser)
        cls.add_transfer_arguments(parser)

        return parser

    @classmethod
    def validate_local_path(cls, path):
        dirname = os.path.dirname(path)
        if dirname != "":
            if os.path.isfile(dirname):
                cls.uni_print(
                    "Error: File with the same name '%s' already exists" %
                    dirname
                )
                sys.exit(-1)
            elif not os.path.isdir(dirname):
                try:
                    os.makedirs(dirname)
                    cls.uni_print("Directory '%s' created" % dirname)
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        cls.uni_print(
                            "Error: Failed to create directory '%s': %s" %
                            (dirname, e)
                        )
                        sys.exit(-1)
                    else:
                        cls.uni_print(
                            "Directory '%s' exists, ignore." % dirname
                        )

    @classmethod
    def main(cls, args):

        parser = cls.get_argument_parser()
        cls.options = parser.parse_args(args)

        # Load config file
        config_path = ["~/.qingstor/config.yaml", "~/.qingcloud/config.yaml"]

        # IF has options.config, insert it
        config_path.insert(0, cls.options.config)

        for path in config_path:
            conf = load_conf(path)
            if conf is not None:
                # Get client of qingstor
                cls.client = cls.get_client(conf)
                break

        cls._init_recorder()

        cls.init_current_bucket()

        if cls.client is None:
            sys.exit(-1)

        # Register SIGINT handler
        signal.signal(signal.SIGINT, cls._handle_sigint)

        # Send request
        cls.send_request()
        # Close print worker
        cls.print_worker.shutdown()
        return

    @classmethod
    def uni_print(cls, statement):
        """This function is used to properly write unicode to console.
        It ensures that the proper encoding is used in different os platforms.
        """
        try:
            if is_python2:
                statement = statement.encode(stdout_encoding)
        except UnicodeError:
            statement = (
                "Warning: Your shell's encoding <%s> does not "
                "support printing this content" % stdout_encoding
            )

        if cls.pbar:
            cls.print_worker.submit(cls.pbar.write, statement)
        else:
            cls.print_worker.submit(print, statement)

    @classmethod
    def safe_walk(cls, top, topdown=True, onerror=None, followlinks=False):
        """
        ref: https://github.com/yunify/qsctl/issues/49
        os.listdir in python 2.x on linux with return str while there are
        illegal characters in the file name, with this override function
        we cloud handle this situation and did nothing else.
        """
        islink, join, isdir = os.path.islink, os.path.join, os.path.isdir

        try:
            # Note that listdir and error are globals in this module due
            # to earlier import-*.
            names = os.listdir(top)
            # force non-ascii text out
            for i in range(len(names)):
                if type(names[i]) == str:
                    names[i].decode(stdout_encoding, "strict")
        except UnicodeError as err:
            if onerror is not None:
                onerror(
                    b"Error: This file's name <%s> contains illegal characters."
                    % names[i]
                )
                onerror(
                    b"Error: The illegal File is under <%s> and is skipped." %
                    top
                )
                del names[i]
        except OSError as err:
            if onerror is not None:
                onerror(err)
            return

        dirs, nondirs = [], []
        for name in names:
            if isdir(join(top, name)):
                dirs.append(name)
            else:
                nondirs.append(name)

        if topdown:
            yield top, dirs, nondirs
        for name in dirs:
            new_path = join(top, name)
            if followlinks or not islink(new_path):
                for x in cls.safe_walk(new_path, topdown, onerror, followlinks):
                    yield x
        if not topdown:
            yield top, dirs, nondirs

    @classmethod
    def walk(cls, top, topdown=True, onerror=None, followlinks=False):
        if is_python2:
            return cls.safe_walk(top, topdown, onerror, followlinks)
        else:
            return os.walk(top, topdown, onerror, followlinks)
