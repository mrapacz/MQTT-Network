-- file : application.lua
temperature = require("temperature")
local module = {}  
m = nil

-- Sends json object containing temperature to server
local function send_data()  
    temp = temperature.get_temperature()
    message = "{\"id\":" .. config.ID .. 
            ", \"temperature\":" .. temp .. 
             "}"
    print(message)
    m:publish(config.ENDPOINT .. config.ID, message, 0, 0)
    node.dsleep(10 * 1000000)
end

-- Subscribe to server on own chipid
local function register_myself()  
    m:subscribe(config.ENDPOINT .. config.ID,0,function(conn)
        print("Successfully subscribed to data endpoint.")
    end)
end

local function mqtt_start()  
    m = mqtt.Client(config.ID, 120)
    -- register message callback
    m:on("message", function(conn, topic, data) 
      if data ~= nil then
        print(topic .. ": " .. data)
      end
    end)
    -- register connect callbackr
    m:connect(config.HOST, config.PORT, 0, 1, function(con) 
        print("Connected to MQTT server.")
        register_myself()
        
        tmr.stop(6)
        --tmr.alarm(6, 10000, 1, send_data)
        send_data()
    end) 
end

function module.start() 
  print("Setting up temperature measuring module...")
  temperature.set_temp()
  print("Starting an MQTT client...")
  mqtt_start()
end

return module  
