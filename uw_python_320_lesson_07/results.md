# Testing results
function|count|mean|std|min|25%|50%|75%|max
-----|-----|-----|-----|-----|-----|-----|-----|-----|
mp_status|19.0|43.586265|19.901307|38.463416|38.703593|38.915025|39.388241|125.744301
mp_user|20.0|5.876570|0.210199|5.700778|5.761945|5.839886|5.890636|6.667695
regular_status|20.0|152.193667|0.902397|151.072951|151.715737|151.918427|152.415009|154.998458
regular_user|20.0|1.640083|0.221664|1.527072|1.562673|1.595387|1.626221|2.567136

# How it was ran
Docker container running MongoDB for the server. test_main.py was ran with 10 iterations each session to come up with results

# Notes
Computer fell asleep during one of the iterations so I had to remove a row. I think that happened on another session, hence the high STD on mp_status
I didn't get to play with batch size, so the values used were 128 for the regular functions and length of csv file / CPUs for multiprocessing
I believe I have optimal batch size for multiprocessing, but I could improve the old method runtime by testing that.
