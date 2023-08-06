"""
FunkMan
=======

FunkMan is a package that establishes a connection between DCS and Discord
via an UDP socket.

Features:
- Send simple text messages.
- Send pictures.
- Interface with AIRBOSS class to show LSO grades and trap sheets
- Interface with RANGE class to show bombing and strafing results

"""

from .funkplot.funkplot import FunkPlot
from .funksock.funksock import FunkSocket
from .funkbot.funkbot   import FunkBot

import os
import configparser

class FunkMan():
    
    def __init__(self, ConfigFile="./FunkMan.ini") -> None:

        # Set config file.
        self.ConfigFile=ConfigFile
    
        # Define parameters used later on.
        self.port=None
        self.host=None
        self.token=None
        self.channelIDmain=None
        self.channelIDrange=None
        self.channelIDairboss=None
        self.imagePath=None

        # Read config file.
        _ReadConfig(self)

        # Create funkplot instance.
        self.funkplot=FunkPlot(self.imagePath)

        # Create funkbot instance.
        self.funkbot=FunkBot(self.token, self.channelIDmain)

        # Create funksocket instance.
        self.funksock=FunkSocket(Host=self.host, Port=self.port)

        # Set Bot.
        self.funksock.SetFunkBot(self.funkbot)

        # Set Plot.
        self.funksock.SetFunkPlot(self.funkplot)

        # Set message channel ID.
        self.funksock.SetChannelIdMessage(self.channelIDmain)

        # Set channel ID for range data.
        self.funksock.SetChannelIdRange(self.channelIDrange)

        # Set channel ID for airboss data.
        self.funksock.SetChannelIdAirboss(self.channelIDairboss)
        

    def SetCallbackStart(self, Func, *argv, **kwargs):
        """Callback function called at start."""
        print("callback fman")
        print(argv)
        self.funkbot.SetCallbackStart(Func, *argv, **kwargs)

    def Start(self):
        """
        Start socket and bot.
        """
        self.funkbot.Start(True)
        self.funksock.Start()
        

def _ReadConfig(funkman: FunkMan) -> None:
    """
    Reads the config file.
    """

    # Get the current working directory
    cwd = os.getcwd()

    # Print the current working directory
    print("Current working directory: {0}".format(cwd))

    # Check if config file exists
    try:
        os.path.exists(funkman.ConfigFile)
    except FileNotFoundError:
        print(f"Could not find ini file {funkman.ConfigFile} in {cwd}!")
        quit()

    # Config parser.
    config = configparser.ConfigParser()

    # Read config file.
    config.read(funkman.ConfigFile)

    # Section name of config.
    SectionName="FUNKMAN"

    # Get config parameters:
    funkman.port=int(config[SectionName]['PORT'])
    funkman.host=str(config[SectionName]['HOST'])
    funkman.token=config[SectionName]['TOKEN']
    funkman.channelIDmain=int(config[SectionName]['CHANNELID_MAIN'])
    funkman.channelIDrange=int(config[SectionName]['CHANNELID_RANGE'])
    funkman.channelIDairboss=int(config[SectionName]['CHANNELID_AIRBOSS'])
    funkman.imagePath=str(config[SectionName]['IMAGEPATH'])

    # Debug message.
    text =str(f"------------------------------------")
    text+=str(f"\nReading config file:")
    text+=str(f"\nHost            = {funkman.host}")
    text+=str(f"\nPort            = {funkman.port}")    
    text+=str(f"\nToken           = {funkman.token}")
    text+=str(f"\nChannel Main    = {funkman.channelIDmain}")
    text+=str(f"\nChannel Range   = {funkman.channelIDrange}")
    text+=str(f"\nChannel Airboss = {funkman.channelIDairboss}")
    text+=str(f"\nImage Path      = {funkman.imagePath}")
    text+=str(f"\n------------------------------------")
    print(text)