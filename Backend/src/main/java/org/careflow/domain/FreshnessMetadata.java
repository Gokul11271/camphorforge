package org.careflow.domain;

import jakarta.persistence.Embeddable;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import java.time.Instant;

@Embeddable
public class FreshnessMetadata {
    private String sourceSystem;
    private String sourceRecordId;
    private Instant observedAt;
    private Instant receivedAt;
    private Instant validUntil;

    @Enumerated(EnumType.STRING)
    private FreshnessClass freshnessClass;

    private Double confidence;

    public FreshnessMetadata() {}

    public FreshnessMetadata(String sourceSystem, String sourceRecordId, Instant observedAt,
                             Instant receivedAt, Instant validUntil, FreshnessClass freshnessClass, Double confidence) {
        this.sourceSystem = sourceSystem;
        this.sourceRecordId = sourceRecordId;
        this.observedAt = observedAt;
        this.receivedAt = receivedAt;
        this.validUntil = validUntil;
        this.freshnessClass = freshnessClass;
        this.confidence = confidence;
    }

    public boolean isFresh() {
        return validUntil != null && Instant.now().isBefore(validUntil);
    }

    public String getSourceSystem() { return sourceSystem; }
    public void setSourceSystem(String sourceSystem) { this.sourceSystem = sourceSystem; }

    public String getSourceRecordId() { return sourceRecordId; }
    public void setSourceRecordId(String sourceRecordId) { this.sourceRecordId = sourceRecordId; }

    public Instant getObservedAt() { return observedAt; }
    public void setObservedAt(Instant observedAt) { this.observedAt = observedAt; }

    public Instant getReceivedAt() { return receivedAt; }
    public void setReceivedAt(Instant receivedAt) { this.receivedAt = receivedAt; }

    public Instant getValidUntil() { return validUntil; }
    public void setValidUntil(Instant validUntil) { this.validUntil = validUntil; }

    public FreshnessClass getFreshnessClass() { return freshnessClass; }
    public void setFreshnessClass(FreshnessClass freshnessClass) { this.freshnessClass = freshnessClass; }

    public Double getConfidence() { return confidence; }
    public void setConfidence(Double confidence) { this.confidence = confidence; }
}
