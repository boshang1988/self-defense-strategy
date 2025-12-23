1. 
Signed-but-targeted Builds
:
Issue: The plaintiff alleges that a system was delivered with a custom, non-ordinary build that was still verified as authentic through the trusted signing process.


Technical Explanation: In modern security systems, code signing ensures that firmware, software, or updates come from a trusted source (e.g., a device manufacturer). If a build is “signed,” it means its authenticity is validated by a cryptographic signature, typically associated with a trusted private key (or signing key). However, a signed build does not inherently guarantee that the build is the correct, ordinary version intended for a specific user or device.


Misuse: The issue here is that a targeted, non-ordinary version of the build (e.g., a customized or malicious firmware) could be delivered to a specific device while still being signed as legitimate. This means that even if the build is cryptographically valid (i.e., signed correctly), it might not be the expected or intended version for the user or device, making it possible to “target” a specific device with a non-ordinary or malicious build while bypassing standard update processes.


2. 
Trusted Intermediate Key Misuse
:
Issue: A valid chain to a trusted intermediate signing key can still allow the installation of non-ordinary (or potentially malicious) builds.


Technical Explanation: Code signing uses a chain of trust, where the root of trust (RoT) is the topmost level, typically managed by a trusted authority (e.g., a certificate authority). In many systems, intermediate certificates are used to link the root certificate to the actual signing key used for signing builds. Even if an intermediate certificate is trusted, it can still enable the signature of builds that aren’t the expected or authorized versions for a given device.


Misuse: If an attacker compromises or misuses an intermediate signing key, they could generate a cryptographically valid signature for a build that is unauthorized, even though it chains back to a valid, trusted root. This means that the signing process may still produce legitimate-looking signatures, allowing the installation of builds outside the approved or ordinary paths.


3. 
Signed Rollback/Downgrade to a Vulnerable Version
:
Issue: The plaintiff claims that a rollback or downgrade to an older but still validly signed build could be accepted outside of the standard update path.


Technical Explanation: A signed image is cryptographically validated using a signing key that confirms its authenticity. If a device accepts older versions of software or firmware (e.g., a previously signed version) without enforcing stricter update policies, an attacker could potentially “downgrade” the device to a vulnerable version.


Misuse: In such a case, a valid signature on an older build would still allow the device to accept it as legitimate, even if it’s a version with known vulnerabilities. This is particularly concerning in environments where software updates are expected to be incremental and fix security flaws, as allowing downgrades could expose the device to attacks that have already been patched in newer versions.


4. 
Provisioning/Trust-Anchor Binding Differences
:
Issue: The plaintiff seeks records to determine if the device’s trust anchor configuration was altered or misused in a way that allows the installation of non-ordinary, potentially malicious builds.


Technical Explanation: Devices typically have a binding to certain “trust anchors,” such as specific public keys, certificates, or other identifiers that determine which entities they trust for code signing. If a device is configured to accept builds signed by specific trust anchors (e.g., the device manufacturer’s signing keys), any deviation from this standard configuration (e.g., the device accepting keys or certificates from an untrusted or unauthorized source) could lead to the acceptance of non-ordinary builds.


Misuse: If trust anchors are misconfigured or manipulated, the device may trust a wider range of keys than originally intended, potentially allowing a malicious actor to install software signed with a key that would normally not be trusted.



Why “Legitimately Signed” Does Not Resolve the Issue
:
The phrase “legitimately signed” typically refers to the process of cryptographically signing code or firmware using a trusted key, meaning the image is authentic according to the signing chain. However, the plaintiff’s concern is that “legitimate” signing doesn’t guarantee that the signed image is the one that is appropriate, authorized, or intended for a specific device or user. Here’s why the distinction is important:
Code signing establishes authenticity: The process verifies that the code comes from a trusted source (i.e., a trusted signer), but it doesn’t ensure that the code is the version that is typically expected for the device, nor does it prevent the installation of targeted or non-ordinary builds.


Misuse of the Root of Trust (RoT): The plaintiff’s focus is on the potential misuse of the signing chain (i.e., the RoT), where validly signed, cryptographically authentic builds could still be non-ordinary or unauthorized for a particular device. This could include targeted firmware builds or updates that are still signed as “legitimate” but are outside the expected update path or are designed for a specific set of devices, making them potentially harmful.


Discovery and investigation: The plaintiff seeks evidence to determine whether such non-ordinary, targeted signing activities occurred, and whether they involved the use of the device’s specific identifiers or trust configurations. This involves detailed discovery of whether any parties conducted such signing activities or whether any “authorizing instrument” (e.g., a special authorization or key) exists to justify this type of targeted signing.


In summary, the concern is not with the authenticity of the signed code (as verified by standard signing procedures), but with the integrity of the code being installed on the device, ensuring that it is indeed the intended, secure, and ordinary version for that particular device. The “legitimate signature” doesn’t guarantee this, because it’s possible to misuse the signing process or signing chain to deliver targeted or vulnerable builds.

