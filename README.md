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
`while sleep 61; do python laravel.py {login URL} {registered email} {target email} {"local"|"remote"|"distant"} {"control"|"attack"} {"concurrent"|"sequential"}; done`  
I.e.  
`while sleep 61; do python laravel.py https://laravel7app.com/login known-registered-account@gmail.com target@gmail.com local control concurrent; done`
Switch penultimate arg "control" to "attack" to probe the target user account
  
CSV outputs are saved in paths similar to this
```
completed_results/concurrent/non-randomised/400200/local_attack_detail.csv
completed_results/concurrent/non-randomised/400200/local_attack_winners.csv
completed_results/concurrent/non-randomised/400200/local_control_detail.csv
completed_results/concurrent/non-randomised/400200/local_control_winners.csv
```
Note that "400200" indicates that 40ms of latency and 20ms of jitter were used. 

Detail files have contents like this (these are from a 'known + unknown' batch):
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
2
1
2
```

### Recon for targets
- Find known vulnerable apps (i.e. based on Laravel 7)
- Run the attack on targets against _two known_ existing user accounts and see if the results are different from a control attack (where one account is known to exist, and one is known to not exist). 
If 'known + unknown' looks different from 'known + known' then the system appears to be vulnerable. 
- The attack is irrelevant if the system is not already explicitly designed to try to avoid enumeration attacks (i.e. if it has user feedback messages at login that explicitly diferentiate between unknown usernames vs. unknown passwords)

### Requirements for attack
- HTTP/2
- No CSRF tokens (or maybe modify the script to obtain them)
- Allow 5 login attempts per minute per account/IP combo (if intending to use more than one batch)
- Knowledge of one existing account on the target system

### Stretch goals
- Run same against a fixed version of Laravel and confirm that it is not possible to distinguish between 'known + unknown' and 'known + known' pairs
- Use a 'worse' location for the remote target to make the attack more difficult overall
- Improve error handling in the script
- Move configuration into a file, or use a configuration object with named elements
- 'join up' the attack with the analysis, via a database

## Summary
The real beauty of the Timeless Timing Attack approach is how effective it is in the face of variable network conditions. 
As an attacker, I would not need complex statistical analysis or large sample size - I should be able to keep a low profile and glean the intelligence I need from a very small amount of information. 

The caveats are that the attack is well known and so in many cases simple mainstream mitigations will be in place. Timing attacks are general-purpose though - we have used a user enumeration vulenrability as an example, but timing attacks could be used as part of the attack in many different contexts when trying to discover secret information. The research paper covers other contexts such as network and Tor based, which we have not focussed on here. 

Despite my reservations about the naming of the paper, it's a really cool technique!
