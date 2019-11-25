import os
import sys

if len(sys.argv) >= 2:
    kmlfilein = sys.argv[1]
    if len(sys.argv) >= 3:
        kmlfileout = sys.argv[2]
    else:
        dotext = kmlfilein[kmlfilein.rfind(os.extsep):]
        fname, ext = os.splitext(kmlfilein)
        kmlfileout = fname + '_flattened' + ext
else:
    kmlfilein = 'doc.kml'
    kmlfileout = 'doc_flattened.kml'


with open(kmlfilein, 'r') as fi:
    with open(kmlfileout, 'w') as fo:
        folder, skip = False, False
        for line in fi.readlines():
            stline = line.strip() #remove indents, but hang onto original line.
            if not folder: #copy up to first <Folder> tag
                if stline == '<Folder>':
                    folder, skip = True, True
                    fo.write(line) # write the first folder!
                else:
                    fo.write(line)
            if folder: #copy lines except for the <Folder> tags and the <name> tag immediately proceeding
                if skip:
                    skip = False
                elif stline == '</Document>':
                    fo.write('\t</Folder>\n</Document>\n') # make sure to write the last </Folder> before done
                elif stline == '<Folder>':
                    skip = True
                elif stline == '</Folder>':
                    pass
                else:
                    fo.write(line)
