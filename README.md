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
- Allow 5 login attempts per minute per account/IP combo (if intending to use more than one salvo)
- Knowledge of one existing account on the target system

### Stretch goals
- Run a traditional (sequential) timing attack against the Laravel 7 target and see how much more difficult it is to interpret the results (note that on a real target there are likely to be many more variable factors which might affect a traditional attack more than a tta attack, i.e. server load due to other 'real' users, other traffic. Tta is designed to render such noise irrelevant as each pair is theoretically subjected to the same outside factors)
- Run same against a fixed version of Laravel and confirm that it is not possible to distinguish between 'known + unknown' and 'known + known' pairs
- Use a 'worse' location for the remote target to make the attack more diifcult overall

## Summary
The real beauty of the Timeless Timing Attack approach is how effective it is in the face of variable network conditions. 
As an attacker, I would not need complex statistical analysis or large sample size - I should be able to keep a low profile and glean the intelligence I need from a very small amount of information. 

The caveats are that the attack is well known and so in many cases simple mainstream mitigations will be in place. Timing attacks are general-purpose though - we have used a user enumeration vulenrability as an example, but timing attacks could be used as part of the attack in many different contexts when trying to discover secret information. The research paper covers other contexts such as network and Tor based, which we have not focussed on here. 

Despite my reservations about the naming of the paper, it's a really cool technique!
