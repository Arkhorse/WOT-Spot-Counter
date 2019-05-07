import logging
import BigWorld
from debug_utils import LOG_CURRENT_EXCEPTION
from Avatar import PlayerAvatar
from skeletons.gui.app_loader import IAppLoader, GuiGlobalSpaceID
from gui.app_loader.settings import APP_NAME_SPACE
from BattleFeedbackCommon import BATTLE_EVENT_TYPE
from gui.battle_control.controllers import feedback_events

class MOD:
    ID = 'spotCounter'
    PACKAGE_ID = '0.01'
    NAME = 'Spotted Counter'
    VERSION = '001'

#CONFIG_FILES = [
#    '${resource_dir}/config.json',
#    '${config_file}'
#]

LOG_FILE = '${log_file}'

_logger = logging.getLogger(MOD.NAME)
def getLogLevel(name):
    logLevel = {
        'CRITICAL':     logging.CRITICAL,
        'ERROR':        logging.ERROR,
        'WARNING':      logging.WARNING,
        'INFO':         logging.INFO,
        'DEBUG':        logging.DEBUG,
        'NOTSET':       logging.NOTSET
    }
    return logLevel.get(name, logging.INFO)

SOUND_LIST = ['soundSpotted', 'soundAssist']
TEXT_LIST = ['UI_message_Spotted_text']
COLOR = ['#0000FF', '#A52A2B', '#D3691E', '#6595EE', '#FCF5C8', '#00FFFF', '#28F09C', '#FFD700', '#008000', '#ADFF2E', '#FF69B5', '#00FF00', '#FFA500', '#FFC0CB', '#800080', '#FF0000', '#8378FC', '#DB0400', '#80D639', '#FFE041', '#FFFF00', '#FA8072']
MENU = ['UI_menu_blue', 'UI_menu_brown', 'UI_menu_chocolate', 'UI_menu_cornflower_blue', 'UI_menu_cream', 'UI_menu_cyan', 'UI_menu_emerald', 'UI_menu_gold', 'UI_menu_green', 'UI_menu_green_yellow', 'UI_menu_hot_pink', 'UI_menu_lime',
        'UI_menu_orange', 'UI_menu_pink', 'UI_menu_purple', 'UI_menu_red', 'UI_menu_wg_blur', 'UI_menu_wg_enemy', 'UI_menu_wg_friend', 'UI_menu_wg_squad', 'UI_menu_yellow', 'UI_menu_nice_red']
GENERATOR = {
    BATTLE_EVENT_TYPE.SPOTTED     : ['UI_message_Spotted_text', 'messageColorSpotted']
}
_logging.debug('Generator Finished')
class Spot(object):
    def __init__(self):
        self.format_str = {}
        self.format_recreate()
        _logging.debug('Spotted init')

    def format_recreate(self):
        self.format_str = {
            'icons'         : '',
            'names'         : '',
            'vehicles'      : '',
            'icons_names'   : '',
            'icons_vehicles': '',
            'full'          : '',
            'damage'        : ''
        }

    @staticmethod
    def sound(assist_type):
        BigWorld.player().soundNotifications.play(config.data[SOUND_LIST[assist_type]])

    def textGenerator(self, event):
        text, color = GENERATOR[event]

    def post_message(self, events):
        g_sessionProvider = BigWorld.player().guiSessionProvider
        self.format_recreate()
        for data in events:
            feedbackEvent = feedback_events.PlayerFeedbackEvent.fromDict(data)
            eventID = feedbackEvent.getBattleEventType()
            if eventID in [BATTLE_EVENT_TYPE.SPOTTED]:
                vehicleID = feedbackEvent.getTargetID()
                icon = '<img src="img://%s" width="%s" height="%s" />' % (g_sessionProvider.getArenaDP().getVehicleInfo(vehicleID).vehicleType.iconPath.replace('..', 'gui'))
                target_info = g_sessionProvider.getCtx().getPlayerFullNameParts(vID=vehicleID)
                if eventID == BATTLE_EVENT_TYPE.SPOTTED:
                    if config.data['sound']: assist.sound(0)
                else:
                    if config.data['sound']: assist.sound(1)
                text, color = self.textGenerator(eventID)
                inject.message(text, color)
        _logging.debug('Spotted message')

spot = SPOTTED()


@inject.hook(PlayerAvatar, 'onBattleEvents')
@inject.log
def onBattleEvents(func, *args):
    func(*args)
    spot.post_message(args[1])