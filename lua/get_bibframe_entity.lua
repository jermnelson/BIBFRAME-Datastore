local output={}
local base_keys = redis.call('HGETALL', KEYS[1])
for k,v in pairs(base_keys) do
  output.insert(output, v)
end
local title_key = KEYS[1] .. ':title'
for k,v in pairs(redis.call('HGETALL', title_key)) do
  output.insert(output, v)
end
return output
