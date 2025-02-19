# Follow The Green XP Python3 Plugin Interface
#
from traceback import print_exc
import xp
from followthegreen import ShowTaxiways

RELEASE = "1.3.0a"

class PythonInterface:

    def __init__(self):
        self.Name = "Show taxiways"
        self.Sig = "showtaxiways.xppython3"
        self.Desc = "Show taxiways, highlight taxiway network. (Rel. " + RELEASE + ")"
        self.enabled = False
        self.trace = True  # produces extra debugging in XPPython3.log for this class
        self.menuIdx = None
        self.showTaxiways = None
        self.showTaxiwaysCmdRef = None

    def XPluginStart(self):
        self.showTaxiwaysCmdRef = xp.createCommand('xppython3/showtaxiways/toggle', 'Show / hide taxiway network')
        xp.registerCommandHandler(self.showTaxiwaysCmdRef, self.showTaxiwaysCmd, 1, None)
        self.menuIdx = xp.appendMenuItemWithCommand(xp.findPluginsMenu(), self.Name, self.showTaxiwaysCmdRef)
        if self.trace:
            print(self.Name, "PI::XPluginStop: menu added.")
        if self.trace:
            print(self.Name, "PI::XPluginStart: started.")
        return self.Name, self.Sig, self.Desc

    def XPluginStop(self):
        if self.showTaxiwaysCmdRef:
            xp.unregisterCommandHandler(self.showTaxiwaysCmdRef,
                                        self.showTaxiwaysCmd,
                                        1, None)
            self.showTaxiwaysCmdRef = None
        if self.menuIdx:
            xp.removeMenuItem(xp.findPluginsMenu(), self.menuIdx)
            self.menuIdx = None
            if self.trace:
                print(self.Name, "PI::XPluginStop: menu removed.")
        if self.showTaxiways:
            try:
                self.showTaxiways.stop()
                self.showTaxiways = None
                if self.trace:
                    print(self.Name, "PI::XPluginStop: stopped.")
            except:
                if self.trace:
                    print(self.Name, "PI::XPluginStop: exception.")
                print_exc()
        return None

    def XPluginEnable(self):
        try:
            self.showTaxiways = ShowTaxiways(self)
            self.enabled = True
            if self.trace:
                print(self.Name, "PI::XPluginEnable: enabled.")
            return 1
        except:
            if self.trace:
                print(self.Name, "PI::XPluginEnable: exception.")
            print_exc()
        return 0

    def XPluginDisable(self):
        try:
            if self.enabled and self.showTaxiways:
                self.showTaxiways.disable()
                self.showTaxiways = None

            self.enabled = False
            if self.trace:
                print(self.Name, "PI::XPluginDisable: disabled.")
            return None
        except:
            if self.trace:
                print(self.Name, "PI::XPluginDisable: exception.")
            print_exc()
            self.enabled = False
            return None
        self.enabled = False
        return None

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
        pass


    def showTaxiwaysCmd(self, *args, **kwargs):
        # pylint: disable=unused-argument
        if not self.enabled:
            print(self.Name, "PI::showTaxiwaysCmd: not enabled.")
            return 0

        # When mapped on a keystroke, showTaxiways only starts on begin of command (phase=0).
        # Phase=1 (continuous press) and phase=2 (release key) are ignored.
        # If phase not found, report it in log and assume phase=0 (i.e. work will be done.)
        commandPhase = 0
        if len(args) > 2:
            commandPhase = args[1]
            if self.trace:
                print(self.Name, "PI::showTaxiwaysCmd: COMMAND PHASE", commandPhase)
        else:
            print(self.Name, "PI::showTaxiwaysCmd: NO COMMAND PHASE", len(args))

        if not self.showTaxiways:
            try:
                self.showTaxiways = ShowTaxiways(self)
                if self.trace:
                    print(self.Name, "PI::showTaxiwaysCmd: created.")
            except:
                if self.trace:
                    print(self.Name, "PI::showTaxiwaysCmd: exception.")
                print_exc()
                return 0

        if self.showTaxiways and commandPhase == 0:
            if self.trace:
                print(self.Name, "PI::showTaxiwaysCmd: available.")
            try:
                self.showTaxiways.start()
                if self.trace:
                    print(self.Name, "PI::showTaxiwaysCmd: started.")
                return 1
            except:
                if self.trace:
                    print(self.Name, "PI::showTaxiwaysCmd: exception(2).")
                print_exc()
                return 0
        elif not self.showTaxiways:
            print(self.Name, "PI::showTaxiwaysCmd: Error: could not create ShowTaxiways.")

        return 0
