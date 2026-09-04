const crypto = require('crypto');
class MrvPrivacySanitizer {
    constructor({ pseudonymKey = process.env.MRV_PSEUDONYM_KEY } = {}) {
        if (typeof pseudonymKey !== 'string' || pseudonymKey.length < 32) throw new Error('MRV_PSEUDONYM_KEY must contain at least 32 characters');
        this.pseudonymKey = pseudonymKey;
        this.version = 'v1.3.0';
        this.rulesetId = 'NULLIFY_MRV_SAFE_EXPORT_RULESET';
        this.classificationMap = {
            ph: 'ENVIRONMENTAL', dissolvedOxygenMgL: 'ENVIRONMENTAL', waterTempC: 'ENVIRONMENTAL', turbidityNtu: 'ENVIRONMENTAL',
            flowRateLps: 'ENVIRONMENTAL', sampleTimestamp: 'ENVIRONMENTAL', sensorId: 'ENVIRONMENTAL',
            batteryLevel: 'OPERATIONAL', firmwareVersion: 'OPERATIONAL', signalRssi: 'OPERATIONAL',
            operatorName: 'PERSONAL', operatorEmail: 'PERSONAL', operatorPhone: 'PERSONAL',
            walletPrivateKey: 'SENSITIVE', rawWalletAddress: 'SENSITIVE', internalIp: 'SENSITIVE', gpsHomeCoordinates: 'SENSITIVE'
        };
    }
    _pseudonymise(value) {
        return `anon_${crypto.createHmac('sha256', this.pseudonymKey).update(String(value)).digest('hex').substring(0, 24)}`;
    }
    sanitizeForMrvExport(rawDataset) {
        if (!rawDataset || typeof rawDataset !== 'object' || Array.isArray(rawDataset)) throw new TypeError('rawDataset must be an object');
        const environmentalEvidence = {};
        const operationalMetadata = {};
        const redactedAuditLog = [];
        for (const [key, value] of Object.entries(rawDataset)) {
            const classification = this.classificationMap[key] || 'SENSITIVE';
            if (classification === 'ENVIRONMENTAL') environmentalEvidence[key] = value;
            else if (classification === 'OPERATIONAL') operationalMetadata[key] = value;
            else if (classification === 'PERSONAL') {
                operationalMetadata[key] = this._pseudonymise(value);
                redactedAuditLog.push({ field: key, action: 'PSEUDONYMISED', classification });
            } else redactedAuditLog.push({ field: key, action: 'STRIPPED', classification });
        }
        const safeExport = {
            exportId: `MRV_SAFE_${crypto.randomUUID()}`,
            rulesetVersion: this.version,
            environmentalEvidence,
            operationalMetadata,
            privacyCompliant: true,
            exportedAt: new Date().toISOString()
        };
        safeExport.provenanceHash = crypto.createHash('sha256').update(JSON.stringify(safeExport)).digest('hex');
        return { safeExport, redactedAuditLog };
    }
}
module.exports = MrvPrivacySanitizer;
