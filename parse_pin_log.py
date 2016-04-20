import re
import datetime
from os.path import isfile


"""
# wishlist
def main_loop():
    "run all the pieces I need"

def get_logfile(savename):
    "get logfile from adb, save to savename. if already exists, ask whether to
    append or to overwrite"

def get_filenames():
    "prompt user or get args for logfile and savefile filepaths"

def make_readable(logname, savename):
    "get

    with open(filename, 'w') as logfile:
        # wishlist
        def test_chunk(chunk):
            "figure out whether a chunk contains all and only the right options, print " +
            "notifications to sdout when it's missing cruicial features, return " +
            "a list containing tuples of (optiontype, timestamp)."
        def order_options(label, array_of_option_timestamp_tuples):
            "given a label of the first entry in a chunk, return the best match " +
                "between the next fire:main:null <label>, ack:bother:null, " +
                "fire:bother:null, and next set:main:#... prints out which is" +
                "used."

"""

def get_input(prompt, verification_fn=lambda x: True, return_fn=lambda x: x):
    user_reply = raw_input("Pin Parse: %s $ " % prompt)
    if user_reply.lower() in ("qq", "q", "quit"):
        return None
# TODO: count tries and vary it up a bit
    while not verification_fn(user_reply):
        user_reply = raw_input("  Try Again (q to quit): $ ")
        if user_reply.lower() in ("qq", "q", "quit"):
            return None
    return return_fn(user_reply)


def save_data(filename, datastring, overwrite=None):
    """given a filename and a datastring, write the data to the file.
        if file already exists, ask the user whether to abort,  overwrite, or append."""
    if isfile(filename) and overwrite==None:
        overwrite = get_input("%s exists already.\n" % filename +
                "  Would you like to Overwrite, Append, or Quit? [O/a/q]",
                lambda x: x.lower() in ("overwrite","o","append","a","quit","q",""),
                lambda x: "w" if x.lower() in ("overwrite","o","") else "a" if x.lower() in ("append","a") else None)
        if overwrite == None:
            print "Save aborted"
            return
    else:
        if overwrite == None:
            overwrite = "a"
    #TODO: test for overwrite is invalid
    with open(filename, overwrite) as f:
        f.write(datastring)
    print "Data saved to %s" % filename


def parse_line(line):
    """given a line, returns a valid entry tuple or raises a ValueError"""
    entry = re.findall("(\d+) (\w+:\w+):(\w+) *(.*)[ \n]*", line)
    if len(entry) != 1:
        raise ValueError("Wrong number of entries found in line %s")
    validate_entry(entry[0])
    return list(entry[0])

def parse_file(logfile):
    """given a logfile, return each entry as a tuple. Ask the user to
       correct any misformed entries manually (or quit) along the way."""
    lines = logfile.readlines()
    entries = []
    for line in lines:
        try:
            entry = parse_line(line)
            entries.append(entry)
        except ValueError:
            # TODO: finish
            user_reply = get_input(ValueError.message)
            try:
                if user_reply != None:
                    entries.append(parse_line(user_reply))
                else:
                    print "Skipping"
            except ValueError:
                print "That was invalid. skipping."
    chunks = chunk_lines(entries)
    results = []
    for chunk in chunks:
         results.append(format_entry(chunk[0], get_endstamp(chunk)))

    return results


def get_endstamp(chunk):
    """Given a logchunk, return the timestamp of the single (error if more than
    one besides last) ack:main:null <label> matching the first label, or the
    next best option's timestamp"""
    first_label = chunk[0][3]
    last_ack = None
    for entry in chunk[1:]:
        if entry[1] == "ack:main":
            if entry[3] == first_label:
                return entry[0]
            else:
                last_ack = entry
    else:
        for entry in chunk:
            if entry[1][-6:] == "bother":
                print "   course a. used %s %s to end %s" % (entry[1], entry[3], first_label)
                return entry[0]
        else:
            if last_ack != None:
                print "   course b. used %s %s to end %s" % (last_ack[1], last_ack[3], first_label)
                return last_ack[-1][0]
            else:
                print "   course c. used %s %s to end %s" % (chunk[-1][1], chunk[-1][3], first_label)
                return chunk[-1][0]




        # TODO: test to check #of lines compared to #entries

    #entry = re.findall("(\d+) (\w+:\w+):(\w+) (.*?) *", line)

def chunk_lines(loglines):
    """given a list of entries, return chunks of set:main:# to set:main#. inclusive."""

    results = []
        # check the first one and make a baby chunk out of it
    index = 0
    while index < len(loglines):
        first_entry = loglines[index]
        index += 1
        if not first_entry[2].isdigit():
            if not get_input("%s not a valid first line.\n  Skip? Y/n" % str(first_entry),
                                lambda x: x.lower() in ("y", "yes","no","n",""),
                                lambda x: True if x == "" else check_boolean(x)):
                user_reply = get_input("Set estimate time in minutes",
                        lambda x: x.isdigit(), int)
                if user_reply != None:
                    first_entry[2] = user_reply
                else:
                    continue
            else:
                continue

        if first_entry[1] != "set:main":
            if get_input("%s not setting a main timer.\n  Use Anyways? y/N" % str(first_entry),
                                lambda x: x.lower() in ("y", "yes","no","n",""),
                                lambda x: False if x == "" else check_boolean(x)):
                first_entry[1] = "set:main"
            else:
                continue
        if first_entry[1] == "set:main":
            chunked = []
            chunked.append(first_entry)
            while index < len(loglines):
                # consider checking for set:main too
                next_entry = loglines[index]
                chunked.append(next_entry)
                if next_entry[2].isdigit() and next_entry[1] != "set:bother":
                    break
                index += 1
            results.append(chunked)
    return results

        # check if it's set:main:#
        # if it is, loop and collect until next set:main:#
            # save set:main:# for next result and break


def format_entry(entry, endstamp):
    """given an entry and a concluding timestamp, return a human readable string
       containing the StartTime, Duration, Label, and Estimate Accuracy."""
    start = datetime.datetime.fromtimestamp(float(entry[0]) / 1000)
    end = datetime.datetime.fromtimestamp(float(endstamp) / 1000)
    duration = round((end - start).total_seconds() / 60.0,0)
    # wishlist: take timedelta/# of minutes, return M or H:MM string.
    # wishlist: take timedelta and estimate, return significance rounded timedelta
    start = start.strftime("%Y %b %d. %a %I:%M%p")
    return "%s: %3d min %s (%s)" % (start, duration, entry[3], entry[2])


"""
    parseall = re.findall("(\d+) (\S+):main:(\S+) (.*?)[$\n]", lines)
    import json
    with open('pin_interpreted.log','w') as savefile:
        json.dump(parse_matches(timers_info), savefile)

"""

#----------------------------------------------
#                  TESTS
#----------------------------------------------
def check_boolean(string):
    if string.lower() in ("true", "t","yes","y"):
        return True
    elif string.lower() in ("false", "f","no","n"):
        return False
    else:
        raise ValueError("%s not boolean" % string)

def test_save_data():
# TODO: check/delete prev. test file, set up test file, tear down test file
    save_data('test_save.log',"test_string")
    print "... saving data passed!"

def test_format_entry():
# 1458509931396 fire:main:null Checking Out Logcat
    string = format_entry(["1458509931396","entry","20","Testing Format Entries"], "1458513019429")
    assert len(string) > 0
    print "... formatting entries passed!"

def valid_line(line):
    try:
        validate_entry(parse_line(line))
        return True
    except ValueError:
        return False

def validate_entry(entry):
    assert len(entry) == 4
    assert int(entry[0]) > 0
    try:
        int(entry[2])
    except ValueError:
        assert entry[2] == "null"

def test_parse_line():
# 1458509931396 fire:main:null Checking Out Logcat
    entry = parse_line("1458509931396 fire:main:null Checking Out Logcat")
    validate_entry(entry)
    entry = parse_line("1458510880821 set:main:20 Testing Parse Entries")
    validate_entry(entry)
    #TODO: Test for None if user decides to skip
    print("... parsing lines passed!")


def test_parse_file():
    with open('test_parse.log',"r") as testfile:
        result = parse_file(testfile)
        """for entry in result:
            assert int(entry[0]) > 0
            try:
                int(entry[2])
            except ValueError:
                assert entry[2] == "null"
                """
    print "... parsing file passed!"

    # TODO: assert these things match

def test_get_input():
    # TODO: make get_input noquittable
    user_input = get_input("type anything")
    print "... pass!"
    user_input = get_input("Say Okay", lambda x: (x.lower() == "okay"))
    assert user_input in ("okay","Okay", None)
    print "... pass!"
    user_input = get_input("Say Banana", lambda x: (x.lower() == "banana"), lambda x: x.lower())
    assert user_input in ("banana", None)
    print "... pass!"
    user_input = get_input("Say True or False",lambda x: (x.lower() in ("true","false")), check_boolean)
    assert user_input in (True, False, None)
    print "... pass!"

def test():
    # TODO: put back test_get_input()
    test_save_data()
    test_format_entry()
    test_parse_line()
    test_parse_file()
# ----------------------------------------------
#                    RUN
# ----------------------------------------------


if __name__ == "__main__":
    """main loop"""
    test()
    with open(get_input("Logfile", isfile), 'r+') as logfile:
        header = datetime.datetime.now().strftime("%Y%b%d-%m")

        save_data("%s save.log" % header, "\n".join(parse_file(logfile)),"w")
