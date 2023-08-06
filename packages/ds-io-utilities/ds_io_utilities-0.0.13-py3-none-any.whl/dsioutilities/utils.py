from alidaargparser import get_asset_property

def input_or_output(name):

    dir = get_asset_property(name, property="direction")
    
    # TODO remove if else when multidataset supported
    if dir is not None:
        return dir
    else:
        if name == "input_dataset" or name == "input-dataset":
            return "input"
        else: 
            return "output"
