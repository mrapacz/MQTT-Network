local module = {}

function module.set_temp()
    t = require("ds18b20")
    t.setup(gpio03)
end

function module.get_temperature()
    
    temp = t.read()
    while(temp == 85) do
        temp = t.read()
    end
    return temp
end

return module