mqtt = require("mqtt")
app = require("application")  
config = require("config")

-- connect to access point
wifi.setmode(wifi.STATION)
wifi.sta.config(config.SSID, config.PASS)
wifi.sta.connect()
print("Waiting 5 secs before connecting to MQTT server...")


function start()
    tmr.alarm(0, 5000, 1, function() 
        if wifi.sta.getip() ~= nil then 
            tmr.stop(0)
            print("Successfully connected to the Internet")
            print(wifi.sta.getip())
            app.start()
        else 
            print("Not connected to network") 
        end
    end)
end
start()
