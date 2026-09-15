package org.careflow.integration.abdm;

import org.careflow.integration.ExternalSystemAdapter;
import org.springframework.stereotype.Component;
import java.util.Map;

@Component
public class AbdmAdapter implements ExternalSystemAdapter {
    @Override
    public String systemName() {
        return "ABDM";
    }

    @Override
    public Map<String, Object> query(String operation, Map<String, Object> request) {
        // TODO: replace with authorized ABDM SDK/API client after onboarding.
        return Map.of("system", "ABDM", "operation", operation, "status", "NOT_CONNECTED");
    }
}
