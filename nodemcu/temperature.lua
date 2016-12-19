local module = {}

function module.set_temp()
    t = require("ds18b20")
    t.setup(gpio03)
end

function module.get_temperature()
    local ERROR = 85 -- a constant symbolizing an error during measurement of temperature

    temp = ERROR
    while(temp == ERROR) do
        temp = t.read()
    end
    return temp
end

return module
