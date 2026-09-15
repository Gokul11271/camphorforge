package org.careflow.integration;

import java.util.Map;

public interface ExternalSystemAdapter {
    String systemName();

    default Map<String, Object> query(String operation, Map<String, Object> request) {
        throw new UnsupportedOperationException("Adapter operation not implemented");
    }

    default void send(String operation, Map<String, Object> request) {
        throw new UnsupportedOperationException("Adapter operation not implemented");
    }
}
