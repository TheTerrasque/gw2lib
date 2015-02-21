from gw2lib.webapi import SimpleAPIClient, API_CACHE
from gw2lib.mumble import GW2MumbleData
from gw2lib.common import genItemChatCode

def test_api():
    """
    Simple Web API test
    """
    API_CACHE.load() #Not needed, but with it module can reuse cache between runs
    
    api1 = SimpleAPIClient()
    api2 = SimpleAPIClient("v2")
    
    item = 23349
    
    print "25", api2.items(item).name, "has Chatcode:", genItemChatCode(item, 25)
    
    print api2.items(item).name, "is used in recepies:"
    for recipe_id in api2.recipes.search(input=item):
        item_id = api2.recipes(recipe_id).output_item_id
        print " *", api2.items(item_id).name, "[%s]" % api2.items(item_id).type

    print api2.items(item)

    print "\nGuild tag:", api1.guild_details(guild_name="Nectarines").tag
    print "Guild ID :", api1("guild_details", guild_name="Nectarines").guild_id #Alternative access
    print "Help url for api2.items() is", api2.items.get_help_url()

    API_CACHE.save() #Not needed, but with it module can reuse cache between runs

def test_mumble():
    """
    Simple Mumble API test
    """
    m = GW2MumbleData()
    
    m.update()
    print "Identity", m.identity
    print "Extra", m.extra
    
    print "Player direction X is", m.extra.player_direction.x # x, y, z

    for x in ["name", "context", "identity", "description", "uiVersion", "uiTick"]:
        print " *", x, ":", getattr(m.data, x)
    
print "Testing mumble link\n"
test_mumble()

print "\nTesting API\n"
test_api()