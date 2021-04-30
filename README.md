# Scenario
Securely share the results of a lab test via QR code. For example, COVID tests should provide a simple POSITIVE, NEGATIVE, PENDING or INCONCLUSIVE result.

## Running Prototype
```
docker run --rm docker.pkg.github.com/narcismpap/labx/labx:latest
docker run --rm --entrypoint pytest docker.pkg.github.com/narcismpap/labx/labx:latest
```

## Intial Assumptions
This QR code can be generated at two steps in the process:
1) before the results are available from the lab, meaning the QR code acts just as a secure key to access results via a query to a live server
2) after tests results are available, the resulting state can be encoded in the QR code for secure, completely offline verifications

## Design Considerations
While creating the architectural plan for this system, we must take into consideration a number of critical elements:

1) Ensure safe access to results, exclusively to the intended recipients and trusted third parties (in other words, prevent enumeration attacks)
2) Potentially allow for offline checks where possible, as network conditions, access or latency can have detrimental access when testing large crowds
3) Implement modern cryptographic standards (at least 128 bits) which utilise key properties of asymmetric cryptography
4) Maintain a compact payload, which can comfortably fit in a QR code (printed or on mobile)
5) Should be readable by any off-the-shelf modest hardware with a camera and compatible software

Unfortunately, points `3)` and `4)` are mutually exclusive. To implement even a simple `PKCS#1` for completely offline, vetted asymmetric signatures will require a much larger amount of storage than a basic QR code can accommodate.

## QR Code Contents
The results must be consumed by a client-facing app in our control, a Native or progressive web app (PWA). 
This application will use the device hardware camera to scan the QR code and display the results on the screen.

### QR Payload Design
The payload will be available as a single string of characters, separated by `|`, with fixed positions for attributes.

```
# Example Payload
00|a7738550-d543-4f78-b464-1f3e4c6690d5|1619818359|John Snow00000000000|3|9618d8811f3627afdab84cfe6b98f9f0
```

```
POS     SIZE    CONTENTS
0 	    2 	    Message Version (default 00), goes to 99
1	    36	    id, unique secure random uuid
2       10      Unix timestamp
3  	    20	    Patient identifier (or name?), right padded with 0
4		1	    Result ENUM, potential for expanded payload in subsequent revisions
```

## Encryption Standard
```
Not possible with QR Code Distribution
```
Both RSA (key >=3072 bits) and ECDSA (ECC key >= 256 bits) fulfil the cryptographic requirement of 128 bits. Unfortunately, ECDSA could be trickier to implement within client-facing applications and libraries are less popular than RSA.

For maximum compatibility with all potential QR code consumers, RSA 3072 will be used for QR code encryption and verification. The entire payload could be encrypted using RSA private key. Base64 encoded output can be provided as a network response, yet it is not possible to safely embed the signature within the message

## Pseudo-Secure Hashing
As proper signatures, such as the ones provided by `PKCS#1` are not possible to implement inside a QR Code, a compromise must be considered. To find the ideal middle ground, we must analyze the potential attack vectors:

1) MOST LIKELY: A person forging the contents of the QR using simple to access tools
2) LESS LIKELY: Skilled engineer extracting the known blake2b secret from the application binary

Based on this threat model, while offering a shared-secret HMAC-based signature system is prone to an attack from an adversary capable of extracting data from application binaries, it provides at least a minimal level of defence against forged QR Codes.


London, Apr 2021.
