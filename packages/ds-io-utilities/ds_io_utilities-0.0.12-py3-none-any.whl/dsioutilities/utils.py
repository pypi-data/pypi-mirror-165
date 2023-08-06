from alidaargparser import get_asset_property

def input_or_output(name):
    return get_asset_property(name, property="direction")
