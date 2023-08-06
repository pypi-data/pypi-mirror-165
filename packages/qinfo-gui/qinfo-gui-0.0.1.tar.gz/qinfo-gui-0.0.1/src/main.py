from modulefinder import packagePathMap
import gi
import qinfo
import os
from math import trunc
import sys
import time
import threading 
from defines import Defines
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Window(Gtk.Window):
    
    def get_values(self) -> str:
        config = self.config
        if config is None:
            sys.exit(1)
    
        # --------------------------------- Hostname --------------------------------- #
        if config["display_hostname"]:
            hostnamestring = f"Hostname:\t\t{qinfo.hostname()}\n"
        else:
            hostnamestring = ""

        # ------------------------------------ CPU ----------------------------------- #
        if config["display_cpu"]:
            cpuline = f"CPU:\t\t\t\t{qinfo.cpu_model()} ({qinfo.core_count()} cores, {qinfo.thread_count()} threads)\n"
        else:
            cpuline = ""
        
        # ------------------------------------ RAM ----------------------------------- #
        if config["display_mem"]:
            available_memory = qinfo.avalible_memory()
            total_memory = qinfo.total_memory()
            used_memory = total_memory - available_memory

            if config["display_gb"]:
                used_memory = (total_memory - available_memory) / Defines.KILOBYTE_GIGABYTE_CONVERSION
                total_memory = qinfo.total_memory() / Defines.KILOBYTE_GIGABYTE_CONVERSION
                unit = "GB"
                ramline = f"Memory:\t\t\t{used_memory:.2f}/{total_memory:.2f} {unit}\n"

            else:
                unit = "kB"
                ramline = f"Memory:\t\t\t{used_memory}/{total_memory} {unit}\n"
        else:
            ramline = ""

        # -------------------------------- motherboard ------------------------------- #
        if config["display_board"]:
            boardline = f"Motherboard:\t\t{qinfo.motherboard_model()}\n"
        else:
            boardline = ""
        
        # ----------------------------- Operating System ----------------------------- #
        if config["display_os"]:
            osline = f"Operating System:\t{qinfo.os_name()}\n"
        else:
            osline = ""

        # ------------------------------ Kernel Release ------------------------------ #
        if config["display_kernel"]:
            kernelline = f"Kernel Release:\t\t{qinfo.kernel_release()}\n"
        else:
            kernelline = ""

        # ------------------------------ Root Birthdate ------------------------------ #
        if config["display_rootfs_birth"]:
            rootfsbirthdate = qinfo.rootfs_age()
            birthyear = rootfsbirthdate["year"]
            birthmonth = rootfsbirthdate["month"]
            birthday = rootfsbirthdate["day"]
            if not config["date_order"]:
                birthstring = f"Root (/) Birth:\t\t{birthmonth}/{birthday}/{birthyear}\n"
            else:
                birthstring = f"Root (/) Birth:\t\t{birthyear}/{birthmonth}/{birthday}\n"
        else: 
            birthstring = ""

        # ---------------------------------- Uptime ---------------------------------- #
        if config["display_uptime"]:
            uptime = qinfo.uptime()
            uptime_days = trunc(uptime / Defines.SECOND_DAY_CONVERSION)
            uptime_hours = trunc(uptime / Defines.SECOND_HOUR_CONVERSION % Defines.HOUR_DAY_CONVERSION)
            uptime_minutes = trunc(uptime / Defines.SECOND_MINUTE_CONVERSION % Defines.MINUTE_HOUR_CONVERSION)
            uptime_seconds = trunc(uptime % Defines.SECOND_MINUTE_CONVERSION)
            uptimestring = "System Uptime:\t"
            
            if uptime_days > 0:
                uptimestring += f"{uptime_days:.0f} days "
            if uptime_hours > 0:
                uptimestring += f"{uptime_hours:.0f} hours "
            if uptime_minutes > 0:
                uptimestring += f"{uptime_minutes:.0f} minutes "
            if uptime_seconds > 0:
                uptimestring += f"{uptime_seconds:.0f} seconds"
            uptimestring += "\n"
        else:
            uptimestring = ""

        # --------------------------------- Username --------------------------------- #
        if config["display_username"]:
            usernameline = f"Username:\t\t{qinfo.username()}\n"
        else:
            usernameline = ""
        
        # ----------------------------------- Shell ---------------------------------- #
        if config["display_shell"]:
            shellline = f"Shell:\t\t\t{qinfo.shell()}\n"
        else:
            shellline = ""

        

        # ---------------------------- Entire Info String ---------------------------- #
        return f"{cpuline}{ramline}{boardline}{osline}{hostnamestring}{usernameline}{kernelline}{shellline}{uptimestring}{birthstring}"
    
    def get_logo(self) -> str:
        config = self.config
        if config["display_logo"]:
            logo = qinfo.logo()
        else:
            logo = ""
        return logo
    
    def get_packages(self) -> str:
        if self.config["display_pkg_count"]:
            packages = qinfo.packages()
            pkglist = "Packages:\t\t\t"
            pacmanpkg = packages["pacman"]
            aptpkg = packages["apt"]
            apkpkg = packages["apk"]
            flatpakpkg = packages["flatpak"]
            snappkg = packages["snap"]
            if pacmanpkg > 0:
                pkglist += f"{pacmanpkg} (Pacman) "
            if aptpkg > 0:
                pkglist += f"{aptpkg} (Apt) "
            if apkpkg > 0:
                pkglist += f"{apkpkg} (Apk)"
            if flatpakpkg > 0:
                pkglist += f"{flatpakpkg} (Flatpak)"
            if snappkg > 0:
                pkglist += f"{snappkg} (Snap)"

            pkglist += "\n"
        else:
            pkglist = ""
        
        return pkglist

    def set_margin(self,object, left, right, top, bottom):
        object.set_margin_top(top)
        object.set_margin_left(left)
        object.set_margin_right(right)
        object.set_margin_bottom(bottom)
    
    def __init__(self):

        self.silent = False
        self.config_file = os.path.join(os.environ.get("HOME"), ".config/.qinfo.conf")
        self.config = qinfo.parse_config(self.config_file, self.silent)
        self.packages = self.get_packages() # get packages only once as it's the slowest
        if self.config is None:
            sys.exit(1)
        super().__init__(title="qinfo-gui")

        hbox = Gtk.Box(spacing=10)
        hbox.set_homogeneous(False)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox.set_homogeneous(False)
        
        
    
        hbox.pack_start(vbox, True, True, 0)

        self.info = Gtk.Label(label=self.get_values())
        self.info.set_margin_top(50)
        self.set_margin(self.info, 20,20,10,10)
        self.logo = Gtk.Label()
        self.logo.set_markup(f"<tt>{self.get_logo()}</tt>")
        self.set_margin(self.logo, 0,0,15,5)
        self.logo.set_justify(Gtk.Justification.LEFT)
        # Update info every 3 seconds
        x = threading.Thread(target=self.update_info)
        x.daemon = True
        x.start()
        vbox.pack_start(self.logo, False, True,0)
        vbox.pack_start(self.info, False, True, 0)

        # label1 = Gtk.Label(
        #     label="logoplaceholder"
        # )
        # label1.set_line_wrap(True)
        # label1.set_justify(Gtk.Justification.LEFT)
        # label1.set_max_width_chars(32)
        # vbox_right.pack_start(label1, True, True, 0)


        self.add(hbox)
    
    def stop(self):
      Gtk.main_quit()

    def update_info(self):
        
        while True:
            self.info.set_text(f"{self.get_values()}{self.packages}")
            while Gtk.events_pending():
                    Gtk.main_iteration()
            time.sleep(3)


        

def main() -> int:
    window = Window()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()

if __name__ == "__main__":
    sys.exit(main())