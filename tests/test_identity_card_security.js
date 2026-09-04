const assert = require('assert');
const IdentityCardRenderer = require('../identity/identity_card_renderer');
const renderer = new IdentityCardRenderer();
const card = renderer.buildCardModel({
    identityId: 'id/<script>',
    displayName: '<script>alert(1)</script>',
    handle: '"><img src=x onerror=alert(1)>',
    avatarUrl: 'javascript:alert(1)'
});
const html = renderer.renderCardHtml(card);
const svg = renderer.exportCardSvg(card);
assert(!html.includes('<script>'));
assert(!svg.includes('<script>'));
assert(!html.includes('javascript:'));
assert(html.includes('rel="noopener noreferrer"'));
assert(card.deepLink.includes(encodeURIComponent('id/<script>')));
assert.throws(() => new IdentityCardRenderer('http://example.com'), /HTTPS/);
console.log('Identity card security tests passed');
