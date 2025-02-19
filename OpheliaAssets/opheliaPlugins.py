from featureTesting import opheliaPluginLoader

plugins = opheliaPluginLoader.loadPlugins()
def getPluginsKeys():
    return plugins.keys