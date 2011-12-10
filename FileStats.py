import sys

class FileInfo(object):

    def __init__(self, filename):

        self.filename = filename
        self.fileData = self.getFile()
        self.stats    = self.filter()

    def getFile(self):
        try:
             file = open(self.filename, "rb").readlines()
             return map(lambda x: x.rstrip().lstrip(), file)
        except IOError:
            print "invalid filename \"%s\"" % (self.filename)

    def filter(self):
        docString   = False
        doc         = 0
        comment     = 0
        codeComment = 0
        blank       = 0
        code        = 0
        for row in self.fileData:

            if not docString:
                try:
                    row[0]
                except IndexError:
                    blank += 1
                    continue
                if row[0] == "#":
                    comment += 1
                elif row[0] not in ["#", "'", '"'] and "#" in row:
                    codeComment += 1
                elif row[:3] in ["'''", '"""']:
                    doc += 1
                    docString = not docString
                    if row[-3:] in ["'''", '"""'] and len(row) >= 6:
                        docString = not docString
                else:
                    code += 1
            else:
                doc += 1
                if row[-3:] in ["'''", '"""']:
                    docString = not docString

        stats = dict(zip(("code", "codeComment", "comment", "blank", "doc"),
                    (code, codeComment, comment, blank, doc)))
        stats["total"] = len(self.fileData)
        return stats

    def __str__(self):
        total = float(self.stats["total"])
        string = \
        """
Number of lines of each in file
        Total              %5i
        Code               %5i %.2f
        Code with comments %5i %.2f
        Comments           %5i %.2f
        Blanks             %5i %.2f
        Doc String         %5i %.2f
        """               % (self.stats["total"],
                             self.stats["code"],
                             round(100 * self.stats["code"] / total, 2),
                             self.stats["codeComment"],
                             round(100 * self.stats["codeComment"] / total, 2),
                             self.stats["comment"],
                             round(100 * self.stats["comment"] / total, 2),
                             self.stats["blank"],
                             round(100 * self.stats["blank"] /total, 2),
                             self.stats["doc"],
                             round(100 * self.stats["doc"] / total, 2))
        return string

if __name__ == "__main__":
    print FileInfo(sys.argv[1])
