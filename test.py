from gw2lib.webapi import SimpleClient, API_CACHE
from gw2lib.mumble import GW2MumbleData
from gw2lib.common import genItemChatCode

def test_api():
    """
    Simple Web API test
    """
    API_CACHE.load() #Not needed, but with it module can reuse cache between runs
    
    api2 = SimpleClient("v2") # Using version 2 of the api
    api1 = SimpleClient() # Uses version 1 of the api by default
    
    item = 12452 # Omnomberry Bar
    
    # Get chatcode for 25 omnomberry bars
    print "25", api2.items(item).name, "has Chatcode:", genItemChatCode(item, 25)
    
    print api2.items(item).name, "is used in recepies:"
    for recipe_id in api2.recipes.search(input=item):
        item_id = api2.recipes(recipe_id).output_item_id
        print " *", api2.items(item_id).name, "[%s]" % api2.items(item_id).type

    guild = "Nectarines"

    print "\n%s Guild tag:" % guild, api1.guild_details(guild_name=guild).tag
    print "%s Guild ID :" % guild, api1("guild_details", guild_name=guild).guild_id #Alternative access
    print "\nHelp url for api2.items() is", api2.items.get_help_url()

    API_CACHE.save() #Not needed, but with it module can reuse cache between runs

def test_mumble():
    """
    Simple Mumble API test
    """
    m = GW2MumbleData()
    
    m.update()
    
    #Player identity data
    print "Identity", m.identity
    
    #Extra data, including map info and client's position and looking direction
    print "Extra", m.extra
    
    print "Player direction X is", m.extra.player_direction.x # x, y, z

    # Listing of various set fields in mumble structure
    for x in ["name", "context", "identity", "description", "uiVersion", "uiTick"]:
        print " *", x, ":", getattr(m.data, x)
    
print "Testing mumble link\n"
test_mumble()

print "\nTesting API\n"
test_api()