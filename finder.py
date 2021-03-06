# needs pyacoustid and mutagen
import acoustid
import pprint
import sys
from mutagen.mp3 import MP3

debug = False
file_out = sys.stdout
error_count = 0
line_count = 0


def process_file( file_name, dict ) :
    """ process a file, given file_name and write the results to out_file."""
    (duration, fingerprint) = acoustid.fingerprint_file(file_name)

    try :
        dict[fingerprint].append(file_name)
    except KeyError :
        dict[fingerprint] = list()
        dict[fingerprint].append(file_name)

    global file_count
    file_count += 1


def optParser( args = None  ) :
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option( "", "--debug", action="store_true", default = False, dest = "debug", help = "")
    parser.add_option( "", "--outfile", default = "", dest = "file_out", help = "")
    parser.add_option( "", "--verbose", action="store_true", default = False, dest = "verbose", help = "")

    return parser.parse_args()

#
# Main
#
if __name__ == "__main__" :
    ( options, args ) = optParser()

    debug = options.debug
    file_count = 0
    different_files = 0
    dict = dict()
    output = list()

    if len( sys.argv ) > 1 :
        # read from a file(s)

        for arg in args :
            if options.verbose :
                print "processing " + arg
            process_file( arg, dict )

    for key in dict :
        if len(dict[key]) > 1:
            output_line = list()
            for item in dict[key]:
                if options.verbose :
                    print "getting info for: " + item
                audio = MP3(item)
                bitrate = audio.info.bitrate
                length = audio.info.length
                output_line.append({'bitrate' : bitrate, 'lenght' : length, 'file' : item})
            output_line = sorted(output_line)
            output.append(output_line)
        different_files+=1

    if options.file_out :
        file_out = file( options.file_out, "w" )
        pprint.pprint(output,file_out,4)
        file_out.close()
    else :
        # just print it
        print output


    if options.verbose:
        print " files processed: ", file_count
        print " different files: " , different_files