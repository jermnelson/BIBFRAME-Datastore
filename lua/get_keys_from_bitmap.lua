local bibframe_entity = ARGV[1]
local total_keys = tonumber(ARGV[2])
local global_key = 'global ' .. bibframe_entity
local i = 1
local result = {}
while (i <= total_keys) do
  if redis.call('GETBIT', KEYS[1], i) > 0 then
    local redis_key = bibframe_entity .. ':' .. i
    table.insert(result, redis_key)
  end
  i = i+1
end
return result
