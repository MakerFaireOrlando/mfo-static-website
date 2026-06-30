---
title: Volunteer at Maker Faire Orlando!
layout: full-width
image: /assets/images/slider/2025-volunteer-greeters.jpg
permalink: /volunteer/
redirect_from: /volunteers/
carousel: true
carousel-delay: 5000
carousel-controls: true
carousel-slides:
  - image: /assets/images/slider/2025-volunteer-greeters.jpg
    caption: Volunteer at Maker Faire Orlando
    url:
  - image: /assets/images/slider/2025-volunteer-curiousity.jpg
    caption: Lend a hand and meet amazing makers
    url:
  - image: /assets/images/slider/2025-volunteer-galactus-centered.jpg
    caption: Be part of the crew behind the magic
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
    <div class="mf-card-grid">

      <a class="mf-card">
        <div class="mf-card-media" style="background-image:url('{{ '/assets/images/slider/family-makey-gate.jpg' | relative_url }}')">
          <span class="mf-card-label">Free Admission</span>
        </div>
        <div class="mf-card-body">
          <p>Work at least a 4-hour shift and get free admission for that day. Volunteer for setup day? Come back for a full day Saturday or Sunday.</p>
        </div>
      </a>

      <a class="mf-card">
        <div class="mf-card-media" style="background-image:url('{{ '/assets/images/slider/happy-crew.jpg' | relative_url }}')">
          <span class="mf-card-label">Volunteer T&#8209;Shirt</span>
        </div>
        <div class="mf-card-body">
          <p>Every volunteer takes home an official {{ site.data.settings.event_year }} Maker Faire Orlando volunteer t-shirt.</p>
        </div>
      </a>

      <a class="mf-card">
        <div class="mf-card-media" style="background-image:url('{{ '/assets/images/slider/learn-to-solder.jpg' | relative_url }}')">
          <span class="mf-card-label">Give Back</span>
        </div>
        <div class="mf-card-body">
          <p>Help inspire thousands in our community and be part of the team that brings the Greatest Show (&amp; Tell) on Earth to life.</p>
        </div>
      </a>

      <a class="mf-card">
        <div class="mf-card-media" style="background-image:url('{{ '/assets/images/educator-page-header-bok-academy.jpg' | relative_url }}')">
          <span class="mf-card-label">Service Hours</span>
        </div>
        <div class="mf-card-body">
          <p>Community service hours are available through The Maker Effect Foundation, a 501(c)(3) public charity.</p>
        </div>
      </a>

    </div>
  </div>
</section>

<!-- Volunteer roles -->
<section class="mf-card-section">
  <div class="container">
    <div class="mf-section-head">
      <h2>Volunteer Roles</h2>
      <p>Here’s a taste of what you might be doing on your shift.</p>
    </div>
    <div class="mf-roles">
      <div class="mf-role">
        <i class="mf-role-icon fa-solid fa-people-group" aria-hidden="true"></i>
        <div class="mf-role-body">
          <h3>General Volunteer <span class="mf-role-age">Ages 13+</span></h3>
          <p>Pitch in wherever you’re needed — wayfinding, info booths, and general event tasks.</p>
        </div>
      </div>
      <div class="mf-role">
        <i class="mf-role-icon fa-solid fa-face-smile" aria-hidden="true"></i>
        <div class="mf-role-body">
          <h3>Greeter <span class="mf-role-age">Ages 13+</span></h3>
          <p>The first friendly face guests see — welcome attendees, scan tickets, and hand out programs and maps.</p>
        </div>
      </div>
      <div class="mf-role">
        <i class="mf-role-icon fa-solid fa-eye" aria-hidden="true"></i>
        <div class="mf-role-body">
          <h3>Exhibit Supervision <span class="mf-role-age">Ages 13+</span></h3>
          <p>Keep an eye on assigned exhibits alongside our Area Captains — monitoring activity, managing lines, and keeping things safe and fun.</p>
        </div>
      </div>
      <div class="mf-role">
        <i class="mf-role-icon fa-solid fa-dolly" aria-hidden="true"></i>
        <div class="mf-role-body">
          <h3>Maker Roadie <span class="mf-role-age">Ages 18+</span></h3>
          <p>Help with load-in and load-out — moving materials, setting up equipment, and supporting the production team.</p>
        </div>
      </div>
      <div class="mf-role">
        <i class="mf-role-icon fa-solid fa-headset" aria-hidden="true"></i>
        <div class="mf-role-body">
          <h3>Production Support <span class="mf-role-age">Ages 18+</span></h3>
          <p>Work one-on-one with a Producer behind the scenes — delivering supplies, managing schedules, and solving issues on the go.</p>
        </div>
      </div>
      <div class="mf-role">
        <i class="mf-role-icon fa-solid fa-star" aria-hidden="true"></i>
        <div class="mf-role-body">
          <h3>Special Skills</h3>
          <p>Have a skill to share — especially photography or videography — or questions about volunteering? <a href="mailto:makers@makerfaireorlando.com">Email us</a> and we’ll find the right fit.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Sign up -->
<section class="mf-prose-section is-light" id="signup">
  <div class="container">
    <div class="row text-center">
      <div class="title-w-border-y"><h2>Sign Up to Volunteer</h2></div>
    </div>
    {% if site.data.settings.volunteer_open %}
    <p class="mf-prose text-center">Register for open shifts below — General Volunteer, Greeter, and more. Having trouble registering, or did your availability change? <a href="mailto:makers@makerfaireorlando.com">Email us</a>.</p>
    <div class="mf-widget-wrap">
      <script src="https://events.humanitix.com/scripts/widgets/inline.js" type="module"></script>
      <iframe data-checkout="{{ site.data.settings.volunteer_checkout }}"></iframe>
    </div>
    {% else %}
    <div class="mf-apply-callout">
      <span class="mf-status-tag">Opening Soon</span>
      <h2>Volunteer Registration Opens This Fall</h2>
      <p>Volunteer registration typically opens in September. Check back here or follow us on social media for the announcement. Already registered and have questions? <a href="mailto:makers@makerfaireorlando.com">Email us</a>.</p>
    </div>
    {% endif %}
  </div>
</section>

