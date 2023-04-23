# Danganronpa Online Area List Maker by Yuzuru #
# Please contact the following if you encounter any bugs
# Discord: Yuzuru#2897, Gmail: <yuzuru.aceattorneyonline@gmail.com>


from src.constant import Constant

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List


@dataclass
class TableData:
    # Commonly Used
    area: str = field(default="Area_")
    background: str = field(default="gs4")
    background_tod: str = field(default='')
    reachable_areas: str = field(default="")
    scream_range: str = field(default="")
    default_description: str = field(default="No Description Written.")

    # Uncommonly Used
    rp_getareas_allowed: bool = field(default=False)
    locking_allowed: bool = field(default=True)
    lobby_area: bool = field(default=False)
    private_area: bool = field(default=False)

    # Rarely Used
    afk_delay: int = field(default=0)
    afk_sentto: int = field(default=0)
    bglock: bool = field(default=False)
    bullet: bool = field(default=True)
    cbg_allowed: bool = field(default=True)
    change_reachability_allowed: bool = field(default=True)
    gm_iclock_allowed: bool = field(default=True)
    iniswap_allowed: bool = field(default=True)
    global_allowed: bool = field(default=True)
    has_lights: bool = field(default=True)
    visible_areas: str = field(default="")
    restricted_chars: str = field(default="")
    rollp_allowed: bool = field(default=True)
    rp_getarea_allowed: bool = field(default=True)
    song_switch_allowed: bool = field(default=True)

    # For Program
    area_id: str = field(default="Area ID")

    # == Functions: TableData Related == #

    def __len__(self):
        return len(self.get_parameters_list())

    def get_dict_from_parameters(self) -> dict:
        return asdict(self)

    def get_parameters_list(self) -> list:
        return list(asdict(self).keys())

    def new_table(self) -> dict:
        new_data = asdict(self)
        generated_id = Constant.id_generator()
        new_data['area'] = f"Area_{generated_id}"
        new_data['reachable_areas'] = f"Area_{generated_id}"
        new_data['area_id'] = f"Area_{generated_id}"
        return new_data

    # == Functions: Export Preparation 1 Related == #

    def prepare_reachable(self) -> List[str]:
        get_data = asdict(self)
        get_reachable = get_data['reachable_areas']
        modified_reachable = [item.strip() for item in get_reachable.split(',')]
        return modified_reachable

    def prepare_scream(self) -> List[str]:
        get_data = asdict(self)
        get_scream = get_data['scream_range']
        modified_scream = [item.strip() for item in get_scream.split(',')]
        return modified_scream

    def prepare_tod(self) -> Dict[str, str]:
        try:
            get_data = asdict(self)
            tod_list = get_data['background_tod'].split(",")
            tod_dict = {item.split(":")[0].strip(): item.split(":")[1].strip() for item in tod_list}
        except KeyError:
            tod_dict = {}
        return tod_dict

    # == Functions: Export Preparation 2 Related == #

    def add_hub_to_list(self, hub_document: Dict[str, Any], reach_scream_list: List[str]) -> List[str]:
        if hub_document['area'] not in reach_scream_list:
            reach_scream_list.insert(0, hub_document['area'])

        else:
            reach_scream_list.pop(reach_scream_list.index(hub_document['area']))

            if len(reach_scream_list) <= 0:
                reach_scream_list = ["<ALL>"]
            else:
                reach_scream_list.insert(0, hub_document['area'])

        return reach_scream_list

    def remove_hub_from_list(self, hub_document: Dict[str, Any], reach_scream_list: List[str]) -> List[str]:
        if hub_document['area'] in reach_scream_list:
            reach_scream_list.pop(reach_scream_list.index(hub_document['area']))

        return reach_scream_list

    # == Functions: Export == #

    def export(self, hub_document: Dict[str, Any]) -> Dict[str, Any]:
        get_data = asdict(self)
        bool_params = ["rp_getareas_allowed", "locking_allowed", "lobby_area", "private_area", "bglock",
                       "bullet", "cbg_allowed", "change_reachability_allowed", "gm_iclock_allowed", "iniswap_allowed",
                       "global_allowed", "has_lights", "rollp_allowed", "rp_getarea_allowed", "song_switch_allowed"]
        number_params = ["afk_delay", "afk_sentto"]

        # Initial Checks to Check
        for k, v in get_data.items():
            if k == bool_params:
                try:
                    v = bool(v)
                    get_data[k] = v
                except ValueError:
                    get_data[k].pop()

            if k == number_params:
                try:
                    v = int(v)
                    get_data[k] = v
                except ValueError:
                    get_data[k].pop()

        # Change Reachable Areas Data
        if not get_data['reachable_areas']:
            get_data.pop('reachable_areas')

        else:
            reachable_areas = self.prepare_reachable()
            new_reachable_areas = self.add_hub_to_list(hub_document, reachable_areas)
            get_data['reachable_areas'] = ", ".join(new_reachable_areas)

        # Change Scream Range Data
        if not get_data['scream_range']:
            get_data.pop('scream_range')

        else:
            scream_range = self.prepare_scream()
            if not hub_document['area'] == get_data['area']:
                new_scream_range = self.remove_hub_from_list(hub_document, scream_range)
            else:
                new_scream_range = scream_range
            get_data['scream_range'] = ", ".join(new_scream_range)

        # Change Background Time of Day
        if not get_data['background_tod']:
            get_data.pop('background_tod')
        else:
            background_tod = self.prepare_tod()
            if not background_tod:
                get_data.pop('background_tod')
            else:
                get_data['background_tod'] = background_tod

        # So everyone could see the areas
        if not get_data['visible_areas']:
            get_data['visible_areas'] = "<REACHABLE_AREAS>"

        # Why would you use this
        if get_data['restricted_chars']:
            get_data['restricted_chars'] = ', '.join([item.strip() for item in get_data[restricted_chars].strip(',')])

        # Removes Blank Spaces
        get_data['area'] = get_data['area'].strip()
        get_data['default_description'] = get_data['default_description'].strip()
        get_data['background'] = get_data['background'].strip()
        get_data.pop('area_id')

        return get_data
