import re
import datetime


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
        def parse_entry(logfile):
            "given a logfile, return each entry as a tuple. Ask the user to " +
                "correct any misformed entries manually (or quit) along the way."
        def chunk_lines(logentries):
            "given a logfile, return chunks of set:main:# to set:main#. inclusive."
        def test_chunk(chunk):
            "figure out whether a chunk contains all and only the right options, print " +
            "notifications to sdout when it's missing cruicial features, return " +
            "a list containing tuples of (optiontype, timestamp)."
        def get_endstamp(chunk):
            "given a logchunk, return the timestamp of the single " + 
                "(error if more than one besides last) ack:main:null <label> " + 
                "matching the first label, or the next best option's timestamp"
        def order_options(label, array_of_option_timestamp_tuples):
            "given a label of the first entry in a chunk, return the best match " +
                "between the next fire:main:null <label>, ack:bother:null, " + 
                "fire:bother:null, and next set:main:#... prints out which is" +
                "used."
        def format_entry(entry, endstamp):
            "given an entry and a concluding timestamp, return a human readable string " +
                "containing the StartTime, SetLength, Duration, and Label."
        def save_data(filename, datastring, overwrite=None):
            "given a filename and a datastring, write the data to the file. " +
                "if file already exists, ask the user whether to abort, " +
                "overwrite, or append."

"""
def get_input(prompt, verification_fn=lambda x: True, return_fn=lambda x: x):
    user_reply = raw_input("Pin Parse: %s $ " % prompt)
    if user_reply.lower() in ("qq", "q", "quit"):
        return None
#TODO: count tries and vary it up a bit
    while not verification_fn(user_reply):
        user_reply = raw_input("  Try Again (q to quit): $ ")
        if user_reply.lower() in ("qq", "q", "quit"):
            return None
    return return_fn(user_reply)



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

def test():
    #TODO: make get_input noquittable
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


#----------------------------------------------
#                    RUN
#----------------------------------------------


if __name__ == "__main__":
    """main loop"""
    test()
