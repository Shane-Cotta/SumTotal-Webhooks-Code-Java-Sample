package com.sumtotal.webhooks.service;

import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.Formatter;
import java.util.logging.Logger;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import org.springframework.stereotype.Service;

@Service
public class Listener {
	
	private static java.util.logging.Logger log = Logger.getLogger("Listener");
	private static final String HMAC_SHA1_ALGORITHM = "HmacSHA1";

	public String ListenEvent(String signature, String payload, String secretKey) throws Exception {
		
		Boolean signatureValid = false;
		if (secretKey != null && secretKey != "") {
			// regenerating the payload signature and validating with payload signature in request.header
			signatureValid = this.ValidateSignature(signature, payload, secretKey);
			
			// signatureValid - true when both payload signatures are matched , will be false when they are not matched
			if (signatureValid) {
				log.info(
						"validated the secretkey with the payload signature and result is matched and secretkey is : "
								+ secretKey);
				return ("Success and validated the secretkey with the payload signature and result is matched and secretkey is :"
						+ secretKey);
			} else {
				log.info(
						"validated the secretkey with the payload signature and result is NOT matched and secretkey is : "
								+ secretKey);
				return ("Success and validated the secretkey with the payload signature and result is NOT matched and secretkey is : "
						+ secretKey);
			}
		} else {
			log.info("not validated the secret key as secretkey is empty");
			return ("Success and not validated the secret key as secretkey is empty");
		}
	   
	}

	public Boolean ValidateSignature(String signature, String payload, String secretKey) throws Exception {

		if (signature == null || payload == null || signature.isEmpty() || payload.isEmpty()) {
			throw new Exception("Exception: Payload/Signature is null or empty.");
		}

		// getting timestamp value from existing payload signature
		String[] signatureParts = signature.split(",");
		String timeStamp = signatureParts[0].split("=")[1];
		
		// regenerating the payload signature using secretKey, payload and timestamp
		String signatureFromPayload = GetPayloadSignature(payload, secretKey, timeStamp);
		log.info("signatureFromPayload :" + signatureFromPayload);

		// validating the generated payload signature with payload signature in request.header
		return signatureFromPayload.equals(signature);
	}

	public String GetPayloadSignature(String payLoad, String secretKey, String timestamp)
			throws NoSuchAlgorithmException, InvalidKeyException {

		String payloadToSign = String.join(".", timestamp, payLoad);
		String signatureVal = "";

		SecretKeySpec signingKey = new SecretKeySpec(secretKey.getBytes(), HMAC_SHA1_ALGORITHM);
		Mac mac = Mac.getInstance(HMAC_SHA1_ALGORITHM);
		mac.init(signingKey);
		signatureVal = toHexString(mac.doFinal(payloadToSign.getBytes()));

		return String.format("t=%s,v1=%s", timestamp, signatureVal);
	}

	private static String toHexString(byte[] bytes) {
		Formatter formatter = new Formatter();

		for (byte b : bytes) {
			formatter.format("%02x", b);
		}
		String hexString = formatter.toString();
		formatter.close();
		return hexString;
	}
}
