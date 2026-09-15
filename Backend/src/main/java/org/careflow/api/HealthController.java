package org.careflow.api;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.Map;

@RestController
public class HealthController {
    @GetMapping("/v1/health")
    public Map<String, Object> health() {
        return Map.of(
            "status", "UP",
            "service", "careflow-api",
            "mode", "prototype"
        );
    }
}
