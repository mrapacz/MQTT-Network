local module = {}

function module.set_temp()
    t = require("ds18b20")
    t.setup(gpio03)
end

function module.get_temperature()
    
    temp = t.read() --used to trigger measuring
    return t.read()
end

return module