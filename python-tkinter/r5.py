import vlc
import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
    from Tkinter import ttk
    from Tkinter.filedialog import askopenfilename
    from Tkinter.tkMessageBox import showerror
else:
    import tkinter as Tk
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename
    from tkinter.messagebox import showerror
from os.path import basename, expanduser, isfile, join as joined
from pathlib import Path
import time

_isMacOS   = sys.platform.startswith('darwin')
_isWindows = sys.platform.startswith('win')
_isLinux   = sys.platform.startswith('linux')

if _isMacOS:
    from ctypes import c_void_p, cdll
    try:
        libtk = 'libtk%s.dylib' % (Tk.TkVersion,)
        prefix = getattr(sys, 'base_prefix', sys.prefix)
        libtk = joined(prefix, 'lib', libtk)
        dylib = cdll.LoadLibrary(libtk)
        _GetNSView = dylib.TkMacOSXGetRootControl
        _GetNSView.restype = c_void_p
        _GetNSView.argtypes = c_void_p,
        del dylib

    except (NameError, OSError):  # image or symbol not found
        def _GetNSView(unused):
            return None
        libtk = "N/A"

    C_Key = "Command-"  # shortcut key modifier

else:  # *nix, Xwindows and Windows, UNTESTED

    libtk = "N/A"
    C_Key = "Control-"  # shortcut key modifier


class _Tk_Menu(Tk.Menu):
    _shortcuts_entries = {}
    _shortcuts_widget  = None

    def add_shortcut(self, label='', key='', command=None, **kwds):
        if not key:
            self.add_command(label=label, command=command, **kwds)

        elif _isMacOS:
            # keys show as upper-case, always
            self.add_command(label=label, accelerator='Command-' + key,
                                          command=command, **kwds)
            self.bind_shortcut(key, command, label)

        else:  # XXX not tested, not tested, not tested
            self.add_command(label=label, underline=label.lower().index(key),
                                          command=command, **kwds)
            self.bind_shortcut(key, command, label)

    def bind_shortcut(self, key, command, label=None):
        if self._shortcuts_widget:
            if C_Key.lower() not in key.lower():
                key = "<%s%s>" % (C_Key, key.lstrip('<').rstrip('>'))
            self._shortcuts_widget.bind(key, command)
            # remember the shortcut key for this menu item
            if label is not None:
                item = self.index(label)
                self._shortcuts_entries[item] = key

    def bind_shortcuts_to(self, widget):
        self._shortcuts_widget = widget

    def entryconfig(self, item, **kwds):
        """Update shortcut key binding if menu entry changed.
        """
        Tk.Menu.entryconfig(self, item, **kwds)
        # adjust the shortcut key binding also
        if self._shortcuts_widget:
            key = self._shortcuts_entries.get(item, None)
            if key is not None and "command" in kwds:
                self._shortcuts_widget.bind(key, kwds["command"])


class Player(Tk.Frame):
    _geometry = ''
    _stopped  = None

    def __init__(self, parent, title=None, video=''):
        Tk.Frame.__init__(self, parent)

        self.parent = parent  # == root
        self.parent.title(title or "tkVLCplayer")
        self.video = expanduser(video)

        menubar = Tk.Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = _Tk_Menu(menubar)
        fileMenu.bind_shortcuts_to(parent)  # XXX must be root?

        fileMenu.add_shortcut("Open...", 'o', self.OnOpen)
        fileMenu.add_separator()
        fileMenu.add_shortcut("Play", 'p', self.OnPlay)  # Play/Pause
        fileMenu.add_command(label="Stop", command=self.OnStop)
        fileMenu.add_separator()
        fileMenu.add_shortcut("Mute", 'm', self.OnMute)
        fileMenu.add_separator()
        fileMenu.add_shortcut("Close", 'w' if _isMacOS else 's', self.OnClose)
        if _isMacOS:  # intended for and tested on macOS
            fileMenu.add_separator()
            fileMenu.add_shortcut("Full Screen", 'f', self.OnFullScreen)
        menubar.add_cascade(label="File", menu=fileMenu)
        self.fileMenu = fileMenu
        self.playIndex = fileMenu.index("Play")
        self.muteIndex = fileMenu.index("Mute")

        self.videopanel = ttk.Frame(self.parent)
        self.canvas = Tk.Canvas(self.videopanel)
        self.canvas.pack(fill=Tk.BOTH, expand=1)
        self.videopanel.pack(fill=Tk.BOTH, expand=1)

        # panel to hold buttons
        self.buttons_panel = Tk.Toplevel(self.parent)
        self.buttons_panel.title("")
        self.is_buttons_panel_anchor_active = False

        buttons = ttk.Frame(self.buttons_panel)
        self.playButton = ttk.Button(buttons, text="Play", command=self.OnPlay)
        stop            = ttk.Button(buttons, text="Stop", command=self.OnStop)
        self.muteButton = ttk.Button(buttons, text="Mute", command=self.OnMute)
        self.playButton.pack(side=Tk.LEFT)
        stop.pack(side=Tk.LEFT)
        self.muteButton.pack(side=Tk.LEFT)

        self.volMuted = False
        self.volVar = Tk.IntVar()
        self.volSlider = Tk.Scale(buttons, variable=self.volVar, command=self.OnVolume,
                                  from_=0, to=100, orient=Tk.HORIZONTAL, length=200,
                                  showvalue=0, label='Volume')
        self.volSlider.pack(side=Tk.RIGHT)
        buttons.pack(side=Tk.BOTTOM, fill=Tk.X)


        # panel to hold player time slider
        timers = ttk.Frame(self.buttons_panel)
        self.timeVar = Tk.DoubleVar()
        self.timeSliderLast = 0
        self.timeSlider = Tk.Scale(timers, variable=self.timeVar, command=self.OnTime,
                                   from_=0, to=1000, orient=Tk.HORIZONTAL, length=500,
                                   showvalue=0)  # label='Time',
        self.timeSlider.pack(side=Tk.BOTTOM, fill=Tk.X, expand=1)
        self.timeSliderUpdate = time.time()
        timers.pack(side=Tk.BOTTOM, fill=Tk.X)


        # VLC player
        args = []
        if _isLinux:
            args.append('--no-xlib')
        self.Instance = vlc.Instance(args)
        self.player = self.Instance.media_player_new()

        self.parent.bind("<Configure>", self.OnConfigure)  # catch window resize, etc.
        self.parent.update()

        self.buttons_panel.overrideredirect(True)
        self.parent.minsize(width=502, height=0)

        if _isMacOS:
            # Only tested on MacOS so far. Enable for other OS after verified tests.
            self.is_buttons_panel_anchor_active = True

            # Detect dragging of the buttons panel.
            self.buttons_panel.bind("<Button-1>", lambda event: setattr(self, "has_clicked_on_buttons_panel", event.y < 0))
            self.buttons_panel.bind("<B1-Motion>", self._DetectButtonsPanelDragging)
            self.buttons_panel.bind("<ButtonRelease-1>", lambda _: setattr(self, "has_clicked_on_buttons_panel", False))
            self.has_clicked_on_buttons_panel = False
        else:
            self.is_buttons_panel_anchor_active = False

        self._AnchorButtonsPanel()

        self.OnTick()  # set the timer up

    def OnClose(self, *unused):
        """Closes the window and quit.
        """
        # print("_quit: bye")
        self.parent.quit()  # stops mainloop
        self.parent.destroy()  # this is necessary on Windows to avoid
        # ... Fatal Python Error: PyEval_RestoreThread: NULL tstate

    def _DetectButtonsPanelDragging(self, _):
        """If our last click was on the boarder
           we disable the anchor.
        """
        if self.has_clicked_on_buttons_panel:
            self.is_buttons_panel_anchor_active = False
            self.buttons_panel.unbind("<Button-1>")
            self.buttons_panel.unbind("<B1-Motion>")
            self.buttons_panel.unbind("<ButtonRelease-1>")

    def _AnchorButtonsPanel(self):
        video_height = self.parent.winfo_height()
        panel_x = self.parent.winfo_x()
        panel_y = self.parent.winfo_y() + video_height + 23 # 23 seems to put the panel just below our video.
        panel_height = self.buttons_panel.winfo_height()
        panel_width = self.parent.winfo_width()
        self.buttons_panel.geometry("%sx%s+%s+%s" % (panel_width, panel_height, panel_x, panel_y))

    def OnConfigure(self, *unused):
        self._geometry = ''  # force .OnResize in .OnTick, recursive?

        if self.is_buttons_panel_anchor_active:
            self._AnchorButtonsPanel()

    def OnFullScreen(self, *unused):
        f = not self.parent.attributes("-fullscreen")  # or .wm_attributes
        if f:
            self._previouscreen = self.parent.geometry()
            self.parent.attributes("-fullscreen", f)  # or .wm_attributes
            self.parent.bind("<Escape>", self.OnFullScreen)
        else:
            self.parent.attributes("-fullscreen", f)  # or .wm_attributes
            self.parent.geometry(self._previouscreen)
            self.parent.unbind("<Escape>")

    def OnMute(self, *unused):
        self.volMuted = m = not self.volMuted  # self.player.audio_get_mute()
        self.player.audio_set_mute(m)
        u = "Unmute" if m else "Mute"
        self.fileMenu.entryconfig(self.muteIndex, label=u)
        self.muteButton.config(text=u)
        # update the volume slider text
        self.OnVolume()

    def OnOpen(self, *unused):
        self.OnStop()
        video = askopenfilename(initialdir = Path(expanduser("~")),
                                title = "Choose a video",
                                filetypes = (("all files", "*.*"),
                                             ("mp4 files", "*.mp4"),
                                             ("mov files", "*.mov")))
        self._Play(video)

    def _Pause_Play(self, playing):
        # re-label menu item and button, adjust callbacks
        p = 'Pause' if playing else 'Play'
        c = self.OnPlay if playing is None else self.OnPause
        self.fileMenu.entryconfig(self.playIndex, label=p, command=c)
        # self.fileMenu.bind_shortcut('p', c)  # XXX handled
        self.playButton.config(text=p, command=c)
        self._stopped = False

    def _Play(self, video):
        # helper for OnOpen and OnPlay
        if isfile(video):  # Creation
            m = self.Instance.media_new(str(video))  # Path, unicode
            self.player.set_media(m)
            self.parent.title("tkVLCplayer - %s" % (basename(video),))

            # set the window id where to render VLC's video output
            h = self.videopanel.winfo_id()  # .winfo_visualid()?
            if _isWindows:
                self.player.set_hwnd(h)
            elif _isMacOS:
                v = _GetNSView(h)
                if v:
                    self.player.set_nsobject(v)
                else:
                    self.player.set_xwindow(h)  # plays audio, no video
            else:
                self.player.set_xwindow(h)  # fails on Windows
            self.OnPlay()

    def OnPause(self, *unused):
        """Toggle between Pause and Play.
        """
        if self.player.get_media():
            self._Pause_Play(not self.player.is_playing())
            self.player.pause()  # toggles

    def OnPlay(self, *unused):
        if not self.player.get_media():
            if self.video:
                self._Play(expanduser(self.video))
                self.video = ''
            else:
                self.OnOpen()
        elif self.player.play():  # == -1
            self.showError("Unable to play the video.")
        else:
            self._Pause_Play(True)
            # set volume slider to audio level
            vol = self.player.audio_get_volume()
            if vol > 0:
                self.volVar.set(vol)
                self.volSlider.set(vol)

    def OnResize(self, *unused):
        """Adjust the window/frame to the video aspect ratio.
        """
        g = self.parent.geometry()
        if g != self._geometry and self.player:
            u, v = self.player.video_get_size()  # often (0, 0)
            if v > 0 and u > 0:
                # get window size and position
                g, x, y = g.split('+')
                w, h = g.split('x')
                if u > v:  # ... for landscape
                    # adjust the window height
                    h = round(float(w) * v / u)
                else:  # ... for portrait
                    # adjust the window width
                    w = round(float(h) * u / v)
                self.parent.geometry("%sx%s+%s+%s" % (w, h, x, y))
                self._geometry = self.parent.geometry()  # actual

    def OnStop(self, *unused):
        """Stop the player, resets media.
        """
        if self.player:
            self.player.stop()
            self._Pause_Play(None)
            # reset the time slider
            self.timeSlider.set(0)
            self._stopped = True

    def OnTick(self):
        if self.player:
            t = self.player.get_length() * 1e-3  # to seconds
            if t > 0:
                self.timeSlider.config(to=t)

                t = self.player.get_time() * 1e-3  # to seconds
                # don't change slider while user is messing with it
                if t > 0 and time.time() > (self.timeSliderUpdate + 2):
                    self.timeSlider.set(t)
                    self.timeSliderLast = int(self.timeVar.get())
        # start the 1 second timer again
        self.parent.after(1000, self.OnTick)
        if not self._geometry:
            self.OnResize()

    def OnTime(self, *unused):
        if self.player:
            t = self.timeVar.get()
            if self.timeSliderLast != int(t):
                self.player.set_time(int(t * 1e3))  # milliseconds
                self.timeSliderUpdate = time.time()

    def OnVolume(self, *unused):
        """Volume slider changed, adjust the audio volume.
        """
        vol = min(self.volVar.get(), 100)
        v_M = "%d%s" % (vol, " (Muted)" if self.volMuted else '')
        self.volSlider.config(label="Volume " + v_M)
        if self.player and not self._stopped:
            if self.player.audio_set_volume(vol):  # and self.player.get_media():
                self.showError("Failed to set the volume: %s." % (v_M,))

    def showError(self, message):
        """Display a simple error dialog.
        """
        self.OnStop()
        showerror(self.parent.title(), message)


if __name__ == "__main__":

    _video = ''

    while len(sys.argv) > 1:
        arg = sys.argv.pop(1)
        if arg.lower() in ('-v', '--version'):
            print('%s: %s (%s %s %s)' % (basename(__file__), __version__,
                                         Tk.__name__, Tk.TkVersion, libtk))
            try:
                vlc.print_version()
                vlc.print_python()
            except AttributeError:
                pass
            sys.exit(0)

        elif arg.startswith('-'):
            print('usage: %s  [-v | --version]  [<video_file_name>]' % (sys.argv[0],))
            sys.exit(1)

        elif arg:  # video file
            _video = expanduser(arg)
            if not isfile(_video):
                print('%s error: no such file: %r' % (sys.argv[0], arg))
                sys.exit(1)

    # Create a Tk.App() to handle the windowing event loop
    root = Tk.Tk()
    player = Player(root, video=_video)
    root.protocol("WM_DELETE_WINDOW", player.OnClose)  # XXX unnecessary (on macOS)
    root.mainloop()