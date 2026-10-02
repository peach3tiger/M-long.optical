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
