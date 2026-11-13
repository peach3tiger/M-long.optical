/*
 * ChatGPT Ads (OpenAI Pixel) conversion events for manhlongoptical.com.
 *
 * Loaded once per page by a marker block that tools/oai-conversions.py places
 * right after the existing OpenAI Pixel snippet in <head>. This file never
 * loads the Pixel, never calls oaiq("init"), and never sends page_viewed;
 * those stay exactly as they are in each page.
 *
 * Events (shapes per developers.openai.com/ads/supported-events and
 * /ads/conversion-tracking):
 *   WhatsApp link (wa.me, api.whatsapp.com, whatsapp.com/send) -> lead_created
 *   Zalo link (zalo.me)                                        -> lead_created
 *   Phone link (tel:)                                          -> lead_created
 *   Google Maps directions (/maps/dir, /maps/search)           -> custom "directions_click"
 * Google Maps place/review links (/maps/place, maps.app.goo.gl) are NOT directions
 * and send nothing. No form or booking flow exists on the site, so no form lead
 * and no appointment_scheduled event is sent from here.
 *
 * No personal data is sent: no name, phone, email, link URL or form content.
 *
 * One click = at most one event:
 *   - this file installs a single listener even if it is loaded twice (window flag);
 *   - the listener resolves the click to the one nearest <a href> (closest), so an
 *     icon or label inside a link counts once, and each link maps to one category;
 *   - only real user clicks count (event.isTrusted).
 * Separate clicks are separate contacts and are each counted; there is no time window.
 *
 * WhatsApp reference code (internal store-sales signal; NOT OpenAI attribution):
 *   Separate listener, added after the event code below and independent of it: the
 *   lead_created / directions_click logic above it is byte-for-byte unchanged.
 *   Signal = the Pixel's first-party __oppref cookie (the Pixel writes it from the ad
 *   landing URL, 30 days, only while measurement consent is granted). The cookie VALUE
 *   is never read into a variable, stored or sent; only its presence is tested.
 *   No cookie -> link untouched and any stored code deleted (expired/revoked/never set).
 *   With the cookie, a wa.me click gets one line put BEFORE the pre-filled message
 *   (so the customer's cursor stays where the original template ends):
 *     "Ref: C-XXXXXX"  this tab session started from a URL with oppref
 *     "Ref: R-XXXXXX"  cookie from an earlier ad click; came back another way
 *   XXXXXX: 6 random chars (crypto.getRandomValues, rejection sampling, 31^6 codes),
 *   never derived from oppref, no personal data; localStorage "mlo_wa_ref", 30-day
 *   expiry restarted on each ad landing. One browser keeps one code.
 *   Runs in the window bubble phase, i.e. after every document-level click listener
 *   (GA4, Meta, OpenAI events) has seen the ORIGINAL href; skips clicks whose default
 *   was prevented and non-primary buttons. href is restored right after the click.
 */
(function (w, d) {
  if (w.__mloOaiConversions) return;
  w.__mloOaiConversions = true;

  function host(u) { return u.hostname.toLowerCase().replace(/^www\./, ''); }

  function classify(href) {
    if (!href) return null;
    if (/^tel:/i.test(href)) return 'lead';
    var u;
    try { u = new URL(href, d.baseURI); } catch (err) { return null; }
    var h = host(u), p = u.pathname.toLowerCase();
    if (h === 'wa.me' || h === 'api.whatsapp.com' || (h === 'whatsapp.com' && p.indexOf('/send') === 0)) return 'lead';
    if (h === 'zalo.me') return 'lead';
    var isGoogle = /^google\.[a-z.]+$/.test(h);
    if (isGoogle && (p.indexOf('/maps/dir') === 0 || p.indexOf('/maps/search') === 0)) return 'directions';
    if (/^maps\.google\.[a-z.]+$/.test(h) && (u.searchParams.has('daddr') || p.indexOf('/maps/dir') === 0)) return 'directions';
    return null;
  }

  d.addEventListener('click', function (e) {
    if (!e.isTrusted || typeof w.oaiq !== 'function') return;
    var el = e.target;
    if (!el || typeof el.closest !== 'function') return;
    var a = el.closest('a[href]');
    if (!a) return;
    if (a.closest('[data-track-scope="nearby-attractions"]')) return; // nearby landmarks card: not store directions
    var kind = classify(a.getAttribute('href'));
    try {
      if (kind === 'lead') {
        w.oaiq('measure', 'lead_created', { type: 'customer_action' });
      } else if (kind === 'directions') {
        w.oaiq('measure', 'custom', { type: 'custom' }, { custom_event_name: 'directions_click' });
      }
    } catch (err) { /* tracking must never block the link */ }
  }, true);
})(window, document);

/* WhatsApp reference code: see header. Independent of the event listener above. */
(function (w, d) {
  if (w.__mloWaRef) return;
  w.__mloWaRef = true;

  var REF_KEY = 'mlo_wa_ref', VISIT_KEY = 'mlo_ad_visit', TTL = 30 * 864e5, LEN = 6;
  var ALPHABET = '23456789ABCDEFGHJKMNPQRSTUVWXYZ'; // 31 chars, no 0/O, 1/I/L
  var CODE_RE = /^[2-9A-HJKMNP-Z]{6}$/;
  var TAG_RE = /^Ref: [CR]-[2-9A-HJKMNP-Z]{6}(\n|$)/;

  function readSaved() {
    try {
      var v = JSON.parse(w.localStorage.getItem(REF_KEY) || 'null');
      return (v && typeof v.c === 'string' && CODE_RE.test(v.c) && typeof v.e === 'number') ? v : null;
    } catch (err) { return null; }
  }
  function save(v) { try { w.localStorage.setItem(REF_KEY, JSON.stringify(v)); } catch (err) { /* blocked */ } }
  function forget() { try { w.localStorage.removeItem(REF_KEY); } catch (err) { /* blocked */ } }

  // At load (deferred, before the Pixel SDK loads): an ad landing URL marks this tab
  // session and restarts the stored code's 30-day expiry (same rule as the cookie).
  try {
    if (/[?&]oppref=[^&#]/.test(w.location.search)) {
      w.sessionStorage.setItem(VISIT_KEY, '1');
      var s0 = readSaved();
      if (s0 && s0.e > Date.now()) save({ c: s0.c, e: Date.now() + TTL });
    }
  } catch (err) { /* storage blocked: visit counts as R- */ }

  function hasAdClick() {
    try { return /(?:^|;\s*)__oppref=[^;\s]/.test(d.cookie || ''); } catch (err) { return false; }
  }

  function newCode() {
    if (!(w.crypto && w.crypto.getRandomValues)) return null;
    var c = '', buf = new Uint8Array(16), i;
    while (c.length < LEN) {
      w.crypto.getRandomValues(buf);
      for (i = 0; i < buf.length && c.length < LEN; i++) {
        if (buf[i] < 248) c += ALPHABET.charAt(buf[i] % 31); // 248 = 8 * 31: no modulo bias
      }
    }
    return c;
  }

  function refBody() {
    var now = Date.now(), saved = readSaved();
    if (saved && saved.e > now) return saved.c;
    var c = newCode();
    if (c) save({ c: c, e: now + TTL });
    return c;
  }

  // New href, or null to leave the link untouched.
  function withRef(href) {
    var u;
    try { u = new URL(href, d.baseURI); } catch (err) { return null; }
    if (u.hostname.toLowerCase().replace(/^www\./, '') !== 'wa.me') return null;
    if (!hasAdClick()) { forget(); return null; }
    var text = u.searchParams.get('text');
    if (text && TAG_RE.test(text)) return null; // already tagged
    var body = refBody();
    if (!body) return null;
    var visit = false;
    try { visit = w.sessionStorage.getItem(VISIT_KEY) === '1'; } catch (err) { visit = false; }
    var line = 'Ref: ' + (visit ? 'C-' : 'R-') + body;
    var msg = text ? line + '\n\n' + text : line;
    return 'https://wa.me' + u.pathname + '?text=' + encodeURIComponent(msg);
  }

  w.addEventListener('click', function (e) {
    if (!e.isTrusted || e.defaultPrevented || e.button !== 0) return;
    var el = e.target;
    if (!el || typeof el.closest !== 'function') return;
    var a = el.closest('a[href]');
    if (!a) return;
    try {
      var href = a.getAttribute('href');
      var tagged = withRef(href);
      if (tagged) {
        a.setAttribute('href', tagged);
        setTimeout(function () { a.setAttribute('href', href); }, 0);
      }
    } catch (err) { /* never block the link */ }
  }, false);
})(window, document);
