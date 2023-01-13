## Testing Simple Variable Assignments


cc0000 = "4305018972893289"    # valid CC
cc0001 = "0005019902565682"    # invalid CC
cc0002 = "4305-0189-7289-3289" # valid CC
cc0002 = "4305 0189 7289 3289" # valid CC

# Testing Dictionary
dict = {}
dict[0] = "4305 0189 7289 3289" # valid CC
dict[1] = "0005019902565682"    # invalid CC

## Testing Conditions
cc = ""
if (cc == "4305 0189 7289 3289"):
  print("success")
if (cc == "0005019902565682"):    # invalid CC
  print('success')
if ("4305 0189 7289 3289" == cc):
  print('success')
if ("0005019902565682" == cc):    # invalid CC
  print('success')

