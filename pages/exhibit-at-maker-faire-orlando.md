---
title: Apply to Exhibit!
permalink: /exhibit-at-maker-faire-orlando/
layout: full-width
image: /assets/images/cfm_brassroots_exhibit.jpg
redirect_from: /exhibit
carousel: true
carousel-delay: 5000
carousel-controls: false
carousel-slides:
  - image: /assets/images/cfm_brassroots_exhibit.jpg
    caption: Brassroots Leather exhibiting at Maker Faire Orlando
    url:
---

<!-- Lead intro -->
<section class="mf-prose-section">
  <div class="container">
    <div class="row text-center">
      <div class="title-w-border-y"><h1>Maker Faire Orlando Can’t Happen Without Makers!</h1></div>
    </div>
    <p class="mf-prose mf-lead text-center">We need people willing to share the things they create and their passion for making. Join us <strong>{% include date-event-short.html %}</strong> for our public days, and on <strong>{% include date-edu-short.html %}</strong> for <a href="/field-trip-day/">Field Trip Day</a>, to help inspire thousands in our community.</p>
  </div>
</section>

<!-- Application status (data-driven: open shows the Apply button) -->
<section class="mf-prose-section is-light">
  <div class="container">
    {% if site.data.settings.call_for_makers_open %}
    <div class="mf-apply-callout is-open">
      <span class="mf-status-tag">Now Open</span>
      <h2>Applications Are Open!</h2>
      <p>Ready to share what you make? Submit your exhibit application for {{ site.data.settings.event_year }} Maker Faire Orlando.</p>
      <a class="btn btn-primary" href="{{ site.data.settings.cfm_url }}">Apply to Exhibit</a>
    </div>
    {% else %}
    <div class="mf-apply-callout">
      <span class="mf-status-tag">Opening Soon</span>
      <h2>Call for Makers Opens Later This Summer</h2>
      <p>We haven’t opened the {{ site.data.settings.event_year }} exhibit application process yet. Check back later this summer and follow us on social media for the announcement!</p>
    </div>
    {% endif %}
  </div>
</section>

<!-- Ways to take part -->
<section class="mf-card-section">
  <div class="container">
    <div class="mf-section-head">
      <h2>Ways to Take Part</h2>
      <p>There’s a place for every kind of maker at Maker Faire Orlando.</p>
    </div>
    <div class="mf-info-grid">
      <div class="mf-info-card">
        <i class="mf-info-icon fa-solid fa-lightbulb" aria-hidden="true"></i>
        <h3>Makers &amp; Community Groups</h3>
        <span class="mf-info-fee is-free">Free</span>
        <p>Individuals and community groups exhibit free of charge — bring a project, demo, or craft and share what you’ve made and learned.</p>
      </div>
      <div class="mf-info-card">
        <i class="mf-info-icon fa-solid fa-tag" aria-hidden="true"></i>
        <h3>Selling Makers</h3>
        <span class="mf-info-fee">$150 fee</span>
        <p>Planning to sell products you make at the event? A $150 seller fee applies for individuals selling their handmade goods.</p>
      </div>
      <div class="mf-info-card">
        <i class="mf-info-icon fa-solid fa-rocket" aria-hidden="true"></i>
        <h3>Businesses &amp; Startups</h3>
        <p>Companies, service/retail businesses, and advertisers should sponsor — startups, reach out about phase-based discounts.</p>
        <a class="mf-link-arrow" href="/become-a-sponsor/">Become a sponsor</a>
      </div>
      <div class="mf-info-card">
        <i class="mf-info-icon fa-solid fa-robot" aria-hidden="true"></i>
        <h3>Combat Robots</h3>
        <p>Combat robot competitors register on buildersdb — you’ll be emailed a special form once accepted, so you don’t need this application.</p>
        <a class="mf-link-arrow" href="https://www.robotruckus.org">Robot Ruckus</a>
      </div>
    </div>
  </div>
</section>

<!-- What you'll need to apply -->
<section class="mf-prose-section">
  <div class="container">
    <div class="row text-center">
      <div class="title-w-border-y"><h2>What You’ll Need to Apply</h2></div>
    </div>
    <ul class="mf-checklist">
      <li><strong>Maker / group info</strong> — name, image (logo or photo), website, and social media pages.</li>
      <li><strong>Exhibit info</strong> — name, description, images, website, and social media pages.</li>
      <li><strong>Availability</strong> — ideally available all weekend, plus Field Trip Day on Friday.</li>
      <li><strong>Requirements</strong> — power, water, light/sound levels, safety needs, and setup time.</li>
    </ul>
    <p class="mf-prose text-center" style="margin-top: 28px;">Choose photos and descriptions that will be compelling to attendees — for inspiration, browse our <a href="/exhibits/">maker exhibits</a>. You can edit your application after submitting, and our team will reach out if more detail is needed. Please add <a href="mailto:makers@makerfaireorlando.com">makers@makerfaireorlando.com</a> to your contacts so our emails reach your inbox.</p>
  </div>
</section>

<!-- How exhibits are selected -->
<section class="mf-prose-section is-dark">
  <div class="container">
    <div class="row text-center">
      <div class="title-w-border-y"><h2>How Exhibits Are Selected</h2></div>
    </div>
    <p class="mf-prose text-center">Maker Faire Orlando is a curated event. We select exhibits based on proposal completeness, content, diversity, items sold, and other factors. Applications are reviewed and approved <strong>in batches</strong> — not in the order received — and we’ll contact you at the email you provide if we need more information or once a decision is made. We’re an all-volunteer team and appreciate your patience as we process hundreds of applications. We can’t fit every application, so highlight your exhibit with great photos, video, and description.</p>
  </div>
</section>

{% include cta-panel-widget.html cta_text="Have questions? Email Us" cta_url="mailto:makers@makerfaireorlando.com" %}
