# Digivote Digital Networked Voting Platform

A Project by David Culbreth for St. Mary's University CS6361 : Computer Network Security

## Project Requirements 
Note that \[SCHN96\] in the description refers to the following book. The book is available online.

- Title: Applied Cryptography
- Author: Bruce Schneier
- Publisher: Wiley, New York, 1996
- ISBN: 0-471-11709-9

### Virtual Election Booth

This project implements the secure election protocol described in \[SCHN96\](Voting with Two Central Facilities).A more theoretical discussion is found in \[SCHN96\]. The implementation will provide a secure way for people to vote online, which el iminates the hassle of physically being present at designated election locations. Since computerized voting will not replace general elections unless there is a protocol that both maintains individual privacy and prevents cheating, the ideal protocol must meet these requirements:
- Only authorized voters can vote. 
- No one can vote more than once. 
- No one can determine for whom anyone else voted. 
- No one can duplicate anyone else's votes. 
- Every voter can make sure that his vote has been taken into account in the final tabulation. 
- Everyone knows who voted and who did not

The design should use two central facilities: Central Tabulating Facility (CTF) and Central 
Legitimization Agency (CLA). CLA's main function is to certify the voters. Each voter will send a message to the CLA asking for a validation number, and CLA will return a random validation number. The CLA retains a list of validation numbers as well as a list of validation numbers' recipients to prevent a voter from voting twice. Then, the CLA completes its task by sending the list of validation number to the CTF. CTF's main function is to count votes. CTF checks the validation number against the list received from the CLA. If the validation number is there, the CTF crosses it off (to prevent someone from voting twice). The CTF adds the identification number to the list of people who voted for a particular candidate and adds one to the tally. After all the votes have been received, the CTF publishes the outcome.

## Setup

If you've followed all of the below instructions, you should be able to just start the whole thing with 
```
docker-compose up --build
``` 
from within the `digivote` root directory. <br/>
Once that has been done, the application should be accessible at `http://digivote.cyber.stmarytx.edu`, and the services at `https://cla.cyber.stmarytx.edu` and `https://ctf.cyber.stmarytx.edu` respectively.

### Generating X.509 Certificates for the CLA and CTF

The Certificates for the CLA and CTF services were omitted on this git repo because they are used for security. Publishing a private key makes it a bit less secure. To generate the certificates, you will need to make the openssl request twice: once for the CLA and once for the CTF. The UI host does not need a key for this demonstration, as it is not the source or destination of any secured information.

For the cla service:
```
cd /.../digivote/digivote-cla/src
openssl req -x509 -nodes -newkey rsa:4096 -keyout cla.key -out cla.crt -days 365 -sha256 -subj "/C=US/ST=Texas/L=San Antonio/O=St. Mary's University/OU=Computer Science Cyberlab/CN=cla.cyber.stmarytx.edu"
```

For the ctf service:
```
cd /.../digivote/digivote-ctf/src
openssl req -x509 -nodes -newkey rsa:4096 -keyout ctf.key -out ctf.crt -days 365 -sha256 -subj "/C=US/ST=Texas/L=San Antonio/O=St. Mary's University/OU=Computer Science Cyberlab/CN=ctf.cyber.stmarytx.edu"
```

As a note, these certificates are self-signed, so your web browser (rightly so) will warn you that the connection is insecure. This is simply because the certificate cannot be validated with a certificate root. If you really want a signed "official" certificate, I guess you can go pay for one.

### Running the application environment

To run the whole 

## Further work for a production environment application

- Acquire certificates signed by a certificate root.
- Deploy CLA and CTF services using a WSGI server 
  - See 

## Debugging notes
- If you are unable to access either of the CLA/CTF services or the UI at their designated sites, you can re-enable the DNS logging within Docker by commenting out these two lines in the `dps` image within `docker-compose.yml`: 
  - ```
    logging:
      driver: none
    ```
  - It is currently only set up to work on a linux machine, due to the volume config:
    - `/etc/resolv.conf:/etc/resolv.conf`

If You encounter the following error in the CLA or CTF:
```
Traceback (most recent call last):
  File "./cla_server.py", line 23, in <module>
    context.load_cert_chain('cla.crt', 'cla.key')
FileNotFoundError: [Errno 2] No such file or directory
```
You likely still need to either
- Run the `openssl` self-signed certificate request found in the section `Generating X.509 Certificates for the CLA and CTF`, or 
- You ran it, but in the wrong spot. Go find your `.crt` and `.key` files, and put them in the appropriate location 
  - The `*.crt.example` will be in the appropriate directories where you need to put them, for reference.
