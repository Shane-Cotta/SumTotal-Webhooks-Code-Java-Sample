package com.sumtotal.webhooks.controller;


import java.util.logging.Logger;
import javax.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;
import com.sumtotal.webhooks.service.Listener;

@RestController
@RequestMapping("/api")
public class ListenerController {
	
	@Autowired
	Listener listener;

	@Autowired
	Environment env;

	private static java.util.logging.Logger log = Logger.getLogger("ListenerController");

	@PostMapping("/listenevent")
	public @ResponseBody String Listener(HttpServletRequest requestBody,
			@RequestHeader("X-SUMT-Signature") String signature) throws Exception {

		String payload = requestBody.getReader().lines().reduce("", String::concat);
		String secretKey = env.getProperty("application.secretKey");
		log.info("Listener Post Method invoked");
		log.info("Payload :" + payload);
		log.info("secretKey :" + secretKey);
		log.info("signature :" + signature);

		return listener.ListenEvent(signature, payload, secretKey);

	}

}
