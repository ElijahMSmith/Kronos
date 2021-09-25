def parseTimeString(str):
    pieces = str.split(":")
    hour = pieces[0]
    return (int(pieces[0]),
            int(pieces[1][0:2]),
            pieces[1][len(pieces[1])-2:])


constants = {"canvWidth": 1400,
             "canvHeight": 850,
             "cellWidth": 200}