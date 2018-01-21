import getopt as opt
import urllib.request as request
import urllib.error as urlerror
import sys, subprocess

class Parser:
    def __init__(self, argv):
        self.argv = argv
        # Need parameter
        self.downloadCmd = 'wget '
        self.version     = 0
        self.proxy       = '127.0.0.1:8080'
        self.save_path   = '.'
        self.sublimeUrl = [['Linux_x86-64', 'https://download.sublimetext.com/sublime_text_3_build_3143_x64.tar.bz2'],
                            ['Linux_x86', 'https://download.sublimetext.com/sublime_text_3_build_3143_x32.tar.bz2'],
                            ['Windows_x86-64', 'https://download.sublimetext.com/Sublime%20Text%20Build%203143%20x64%20Setup.exe'],
                            ['Windows_x86', 'https://download.sublimetext.com/Sublime%20Text%20Build%203143%20Setup.exe'],
                            ['OS X', 'https://download.sublimetext.com/Sublime%20Text%20Build%203143.dmg']]
    pass
    def usage(self):
        print("%s: [-h|--help]"%(self.argv[0]))
    def parse(self):
        # Verify the input parameter
        try:
            opts, args = opt.getopt(self.argv, "h",
                                          ["help"])
        except opt.GetoptError as err:
            print(err)
            Help.usage(argv[0])
            sys.exit()
        # Get every parameter
        link = self.sublimeUrl[self.verion][1]
        self.save_path = "./" + link.split('/')[3]
        self.downloadCmd = 'wget -O ' + sefl.save_path + ' ' + link
        print(self.downloadCmd)
        

class Downloader:
    def __init__(self, parser):
        self.parser = parser
    def download(self):
        # check the file exist ?
        print("downloading")
        #self.parser.parse()
        #read = subprocess.getstatusoutput(self.parser.downloadCmd)
        #index = read[1].find("Linux repos")
        #link = read[1][index:index+1024]
        
        print(read)

def main(argv):
    parser = Parser(argv)
    downloader = Downloader(parser)
    downloader.download()
if __name__ == "__main__":
    main(sys.argv)
