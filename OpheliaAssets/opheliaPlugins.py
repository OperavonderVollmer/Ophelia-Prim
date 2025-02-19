from features import opheliaPluginLoader

plugins = opheliaPluginLoader.loadPlugins()
def getPluginsKeys():
    return plugins.keys