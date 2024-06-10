import pluggy

hookspec = pluggy.HookspecMarker("pss-app")
hookimpl = pluggy.HookimplMarker("pss-app")


class GuiPlugin:
    @hookspec
    def init_gui(self):
        pass
