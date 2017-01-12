-- file : config.lua
local module = {}

module.SSID = "ssid"
module.PASS = "password"

module.HOST = "192.168.0.254"  
module.PORT = 7777

module.ID = node.chipid()

module.SLEEPTIME = 8 * 60 * 1000000 -- 8 minutes

module.ENDPOINT = "nodemcu/"  
return module  
