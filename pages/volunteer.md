---
title: Volunteer at Maker Faire Orlando!
layout: full-width
image: /assets/images/volunteer-solder.jpg
permalink: /volunteer/
redirect_from: /volunteers/
carousel: true
carousel-delay: 5000
carousel-controls: false
hero-title: Volunteer With Us
hero-meta: Join the team that makes the magic happen
carousel-slides:
  - image: /assets/images/volunteer-solder.jpg
    caption: Learn-To-Solder
    url:
---

<!-- Lead intro -->
<section class="mf-prose-section">
  <div class="container">
    <div class="row text-center">
      <div class="title-w-border-y"><h1>We Need You!</h1></div>
    </div>
    <p class="mf-prose mf-lead text-center">Volunteering at {{ site.data.settings.event_name }} is a great way to give back to your local community — and to experience the event without buying a ticket.</p>
  </div>
</section>

<!-- Volunteer perks -->
<section class="mf-card-section is-light">
  <div class="container">
    <div class="mf-section-head">
      <h2>Why Volunteer?</h2>
      <p>Give a little time, get a lot back.</p>
    </div>
    <div class="mf-info-grid">
      <div class="mf-info-card">
        <i class="mf-info-icon fa-solid fa-ticket" aria-hidden="true"></i>
        <h3>Free Admission</h3>
        <p>Work at least a 4-hour shift and get free admission for that day. Volunteer for setup day? Come back for a full day Saturday or Sunday.</p>
      </div>
      <div class="mf-info-card">
        <i class="mf-info-icon fa-solid fa-shirt" aria-hidden="true"></i>
        <h3>Volunteer T-Shirt</h3>
        <p>Every volunteer takes home an official {{ site.data.settings.event_year }} Maker Faire Orlando volunteer t-shirt.</p>
      </div>
      <div class="mf-info-card">
        <i class="mf-info-icon fa-solid fa-hands-holding-heart" aria-hidden="true"></i>
        <h3>Give Back</h3>
        <p>Help inspire thousands in our community and be part of the team that brings the Greatest Show (&amp; Tell) on Earth to life.</p>
      </div>
      <div class="mf-info-card">
        <i class="mf-info-icon fa-solid fa-graduation-cap" aria-hidden="true"></i>
        <h3>Service Hours</h3>
        <p>Community service hours are available through The Maker Effect Foundation, a 501(c)(3) public charity.</p>
      </div>
    </div>
  </div>
</section>

<!-- Good to know -->
<section class="mf-prose-section">
  <div class="container">
    <div class="row text-center">
      <div class="title-w-border-y"><h2>Good to Know</h2></div>
    </div>
    <ul class="mf-checklist">
      <li><strong>Age:</strong> volunteers must be 13 or older — some roles require 16+ or 18+.</li>
      <li><strong>No-cost registration:</strong> we use the Humanitix platform, which issues a “ticket,” but there’s no charge to you.</li>
      <li><strong>Special skills or questions?</strong> If you have a skill-set (especially photography/videography) or any questions, email <a href="mailto:makers@makerfaireorlando.com">makers@makerfaireorlando.com</a>.</li>
    </ul>
  </div>
</section>

<!-- Sign up -->
<section class="mf-prose-section is-light" id="signup">
  <div class="container">
    <div class="row text-center">
      <div class="title-w-border-y"><h2>Sign Up to Volunteer</h2></div>
    </div>
    {% if site.data.settings.volunteer_open %}
    <p class="mf-prose text-center">Register for open shifts below — General Volunteer, Greeter, and more. Having trouble registering, or did your availability change? Email <a href="mailto:makers@makerfaireorlando.com">makers@makerfaireorlando.com</a>.</p>
    <div class="mf-widget-wrap">
      <script src="https://events.humanitix.com/scripts/widgets/inline.js" type="module"></script>
      <iframe data-checkout="{{ site.data.settings.volunteer_checkout }}"></iframe>
    </div>
    {% else %}
    <div class="mf-apply-callout">
      <span class="mf-status-tag">Opening Soon</span>
      <h2>Volunteer Registration Opens This Fall</h2>
      <p>Volunteer registration typically opens in September. Check back here or follow us on social media for the announcement. Already registered and have questions? Email <a href="mailto:makers@makerfaireorlando.com">makers@makerfaireorlando.com</a>.</p>
    </div>
    {% endif %}
  </div>
</section>

