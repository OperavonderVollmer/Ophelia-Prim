import os, importlib.util

pluginDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugins")

# returns an array of plugins currently in the plugins folder
def loadPlugins():
    #plugins= []
    plugins = {}

    for fileName in os.listdir(pluginDir):
        if fileName.endswith(".py"):
            pluginName = fileName[:-3] # removes py
            pluginName = pluginName.replace("Plugin", "")
            pluginPath = os.path.join(pluginDir, fileName)

            spec = importlib.util.spec_from_file_location(pluginName, pluginPath)
            plugin = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin)

            if hasattr(plugin, "get_plugin"): 
                #plugins.append(plugin.get_plugin())
                plugins.update({pluginName: plugin.get_plugin()})
    
    return plugins
