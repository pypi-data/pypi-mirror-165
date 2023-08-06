from arklibrary.admin.bundle import Bundle
from arklibrary.blueprints import *


class Admin(Bundle):
    def __init__(self, password=None, player_id=None, map_name=None):
        super().__init__()
        # ctrl-x to clear console
        # ctrl-c to copy console
        self.__password = password
        self.player_id = player_id
        self.map_name = map_name

    def player_coords(self, player_id='default'):
        #self.copy_coords()
        # this next line should be a listener running in the background
        #clip = self.driver.app.get_from_clipboard()
        #self.cache[player_id] = [float(c) for c in clip.split()]
        # end of listener running in the background
        pass

    # def return_player(self, player_id='default'):
    #     # wait until the listener on player_coords has finished copying
    #     if player_id != 'default' and player_id in self.cache:
    #         self.teleport_exact(self.cache[player_id])
    #         self.teleport_player_id_to_me(player_id)
    #     self.teleport_exact(self.cache['default'])

    def enable_admin(self):
        self.enable_cheats(self.__password)
        self.gcm()
        self.ghost()
        self.clear_player_inventory(self.player_id)
        return self

    def enable_cheats(self, password):
        self.command(CreativeMode.ENABLE_CHEATS.format(password))
        return self

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        items = []
        for k, v in self.__dict__.items():
            if k and k[0] != "_":
                items.append(f"\033[34m{k}\033[90m=\033[0m{repr(v)}\033[0m")
        args = ', '.join(items)
        return f'<\033[96m{type(self).__name__}\033[0m({args})>\033[0m'
