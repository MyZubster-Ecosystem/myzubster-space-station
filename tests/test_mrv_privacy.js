const assert = require('assert');
const MrvPrivacySanitizer = require('../privacy/mrv_privacy_sanitizer');

async function runPrivacySanitizerTests() {
    const sanitizer = new MrvPrivacySanitizer();
    const rawData = {
        sensorId: 'TEST_SENSOR_04',
        ph: 7.42,
        dissolvedOxygenMgL: 8.15,
        turbidityNtu: 1.28,
        sampleTimestamp: '2026-09-04T07:45:00Z',
        batteryLevel: 94.5,
        operatorName: 'Test Operator',
        operatorEmail: 'operator@example.invalid',
        rawWalletAddress: 'TEST_WALLET_PLACEHOLDER',
        internalIp: '192.0.2.1'
    };
    const { safeExport, redactedAuditLog } = sanitizer.sanitizeForMrvExport(rawData);
    assert.strictEqual(safeExport.environmentalEvidence.ph, 7.42);
    assert.strictEqual(safeExport.environmentalEvidence.dissolvedOxygenMgL, 8.15);
    assert.strictEqual(safeExport.environmentalEvidence.sensorId, 'TEST_SENSOR_04');
    assert(!('rawWalletAddress' in safeExport.environmentalEvidence));
    assert(!('rawWalletAddress' in safeExport.operationalMetadata));
    assert(!('internalIp' in safeExport.operationalMetadata));
    assert(safeExport.operationalMetadata.operatorName.startsWith('anon_'));
    assert(safeExport.operationalMetadata.operatorEmail.startsWith('anon_'));
    assert.notStrictEqual(safeExport.operationalMetadata.operatorName, 'Test Operator');
    assert.strictEqual(redactedAuditLog.length, 4);
    assert.strictEqual(safeExport.provenanceHash.length, 64);
    assert.strictEqual(safeExport.privacyCompliant, true);
    console.log('MRV privacy tests passed');
}
runPrivacySanitizerTests().catch(error => {
    console.error('Test failed:', error);
    process.exit(1);
});
