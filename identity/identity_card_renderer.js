const ALLOWED_AVATAR_PROTOCOLS = new Set(['http:', 'https:']);
function escapeMarkup(value) {
    return String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}
function safeAvatarUrl(value) {
    const fallback = '/assets/avatars/default_cadet.svg';
    if (!value) return fallback;
    if (String(value).startsWith('/')) return String(value);
    try {
        const parsed = new URL(String(value));
        return ALLOWED_AVATAR_PROTOCOLS.has(parsed.protocol) ? parsed.href : fallback;
    } catch { return fallback; }
}
class IdentityCardRenderer {
    constructor(baseUrl = 'https://spacestation.myzubster.io') {
        const parsed = new URL(baseUrl);
        if (parsed.protocol !== 'https:') throw new Error('baseUrl must use HTTPS');
        this.baseUrl = parsed.href.replace(/\/$/, '');
    }
    buildCardModel(identityRecord) {
        if (!identityRecord || typeof identityRecord.identityId !== 'string' || !identityRecord.identityId.trim()) throw new Error('identityId is required');
        const rawId = identityRecord.identityId.trim();
        const abbreviatedId = rawId.length > 12 ? `${rawId.substring(0, 6)}...${rawId.substring(rawId.length - 4)}` : rawId;
        const verified = ['SYSTEM_VERIFIED', 'CRYPTOGRAPHICALLY_PROVEN'].includes(identityRecord.verificationStatus);
        return {
            identityId: rawId,
            abbreviatedId,
            displayName: identityRecord.displayName || 'Cadet',
            handle: identityRecord.handle ? `@${String(identityRecord.handle).replace(/^@+/, '')}` : `@${rawId.substring(0, 8)}`,
            archetypeSpecies: identityRecord.archetypeSpecies || 'Cosmic Pioneer',
            entityType: identityRecord.isSimulatedEntity ? 'SIMULATED' : 'HUMAN',
            verificationBadge: verified ? 'VERIFIED' : 'UNVERIFIED',
            deepLink: `${this.baseUrl}/id/${encodeURIComponent(rawId)}`,
            nativeProtocolLink: `myz://identity/${encodeURIComponent(rawId)}`,
            avatarUrl: safeAvatarUrl(identityRecord.avatarUrl),
            createdAt: identityRecord.createdAt || new Date().toISOString()
        };
    }
    exportCardSvg(cardModel) {
        const entity = cardModel.entityType === 'SIMULATED' ? 'SIMULATED' : 'HUMAN';
        const badge = cardModel.verificationBadge === 'VERIFIED' ? 'VERIFIED' : 'UNVERIFIED';
        return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 450 600" width="450" height="600">
<rect width="450" height="600" rx="20" fill="#0a0e17" stroke="#00e5ff" stroke-width="4"/>
<text x="30" y="50" fill="#00e5ff" font-family="monospace" font-size="14">MYZUBSTER SPACE STATION</text>
<text x="370" y="50" fill="#666" font-family="monospace" font-size="12">${escapeMarkup(cardModel.abbreviatedId)}</text>
<text x="225" y="320" fill="#fff" font-family="sans-serif" font-size="24" text-anchor="middle">${escapeMarkup(cardModel.displayName)}</text>
<text x="225" y="350" fill="#00e5ff" font-family="monospace" font-size="16" text-anchor="middle">${escapeMarkup(cardModel.handle)}</text>
<text x="225" y="385" fill="#8892b0" font-family="sans-serif" font-size="14" text-anchor="middle">${escapeMarkup(cardModel.archetypeSpecies)}</text>
<text x="150" y="441" fill="#00e5ff" font-family="monospace" font-size="12">${entity}</text>
<text x="300" y="441" fill="#00ffaa" font-family="monospace" font-size="12">${badge}</text>
<text x="225" y="555" fill="#8892b0" font-family="monospace" font-size="10" text-anchor="middle">${escapeMarkup(cardModel.deepLink)}</text>
</svg>`;
    }
    renderCardHtml(cardModel) {
        const entity = cardModel.entityType === 'SIMULATED' ? 'simulated' : 'human';
        const badge = cardModel.verificationBadge === 'VERIFIED' ? 'verified' : 'unverified';
        return `<div class="myz-identity-card responsive-card ${entity}">
<div class="card-header"><span class="station-mark">MYZUBSTER SPACE STATION</span><span class="short-id">${escapeMarkup(cardModel.abbreviatedId)}</span></div>
<div class="card-avatar"><img src="${escapeMarkup(safeAvatarUrl(cardModel.avatarUrl))}" alt="${escapeMarkup(cardModel.displayName)}" /></div>
<div class="card-body"><h3 class="display-name">${escapeMarkup(cardModel.displayName)}</h3><span class="handle">${escapeMarkup(cardModel.handle)}</span><p class="archetype">${escapeMarkup(cardModel.archetypeSpecies)}</p>
<div class="badges-row"><span class="badge badge-entity ${entity}">${entity.toUpperCase()}</span><span class="badge badge-verif ${badge}">${badge.toUpperCase()}</span></div></div>
<div class="card-footer"><a href="${escapeMarkup(cardModel.deepLink)}" class="qr-link" target="_blank" rel="noopener noreferrer">🔗 PUBLIC PROFILE</a></div></div>`;
    }
}
module.exports = IdentityCardRenderer;
