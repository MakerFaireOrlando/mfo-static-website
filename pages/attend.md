---
title: Attend Maker Faire Orlando
permalink: /attend/
image: /assets/images/slider/2025-big-cosplay.jpg
layout: full-width
redirect_from:
  - /ticket/
  - /tickets/


carousel: true
carousel-delay: 5000
carousel-controls: false
carousel-slides:
  - image: /assets/images/slider/2025-kid-ghostbusters-cosplay-portrait.jpg
    caption: Family cosplaying at Maker Faire
    url:
scrolltop: true
page_footer_ad: false
---

<!-- Lead intro -->
<section class="mf-prose-section">
  <div class="container">
    <div class="row text-center">
      <div class="title-w-border-y"><h1>Maker Faire Orlando {{ site.data.settings.event_year }}</h1></div>
    </div>
    <p class="mf-prose mf-lead text-center">A non-profit, community-organized, family-friendly celebration of local do-it-yourself science, art, rockets, robots, crafts, technology, music, hands-on activities, and so much more — {% include date-event.html %}.</p>
  </div>
</section>

<!-- Event quick facts -->
<section class="mf-card-section is-light">
  <div class="container">
    <div class="mf-section-head">
      <h2>Plan Your Visit</h2>
      <p>Everything you need to know before you go.</p>
    </div>
    <div class="mf-info-grid">
      <div class="mf-info-card">
        <i class="mf-info-icon fa-solid fa-calendar-days" aria-hidden="true"></i>
        <h3>When</h3>
        <p>{{ site.data.settings.event_dates.day1 | date: "%A, %B %-d" }} &amp; {{ site.data.settings.event_dates.day2 | date: "%A, %B %-d" }}<br>{{ site.data.settings.event_hours }} (both days)</p>
      </div>
      <div class="mf-info-card">
        <i class="mf-info-icon fa-solid fa-location-dot" aria-hidden="true"></i>
        <h3>Where</h3>
        <p>Central Florida Expo Center &amp; Fairgrounds<br>4603 W Colonial Dr, Orlando, FL 32808</p>
      </div>
      <div class="mf-info-card">
        <i class="mf-info-icon fa-solid fa-square-parking" aria-hidden="true"></i>
        <h3>Free Parking</h3>
        <p>On-site parking is <strong>free</strong> all weekend — just bring your sense of curiosity.</p>
      </div>
      <div class="mf-info-card">
        <i class="mf-info-icon fa-solid fa-shapes" aria-hidden="true"></i>
        <h3>250+ Exhibits</h3>
        <p>Explore <a href="/exhibits/">hundreds of exhibits, hands-on activities and competitions</a> to find your favorites!</p>
      </div>
    </div>
    <p class="mf-prose text-center">Plan your weekend with the <a href="/schedule/">Schedule</a> and <a href="/program/">Program</a> — and don’t miss the talks, panels &amp; performances on the <a href="/schedule/">Main Stage</a>!</p>
  </div>
</section>

<!-- Tickets -->
<section class="mf-prose-section" id="tickets">
  <div class="container">
    <div class="row text-center">
      <div class="title-w-border-y"><h2>Tickets</h2></div>
    </div>
    {% if site.data.settings.tickets_on_sale %}
    <p class="mf-prose text-center">Tickets are available on <a href="https://events.humanitix.com/makerfaireorlando">Humanitix</a> or through the form below — Humanitix donates 100% of profits to children’s charities!</p>
    <div class="mf-widget-wrap">
      <script src="https://events.humanitix.com/scripts/widgets/inline.js" type="module"></script>
      <iframe data-checkout="makerfaireorlando"></iframe>
    </div>
    <p class="mf-prose text-center"><small>Student tickets include college students with a current college student ID.</small></p>
    {% else %}
    <div class="mf-apply-callout">
      <span class="mf-status-tag">Coming Soon</span>
      <h2>Tickets Aren’t On Sale Yet</h2>
      <p>Tickets for {{ site.data.settings.event_year }} Maker Faire Orlando will go on sale soon. <a href="{{ site.data.settings.newsletter_url }}">Subscribe to our newsletter</a> and follow us on social media to be the first to know.</p>
    </div>
    {% endif %}
  </div>
</section>

<!-- Discounted & free admission programs -->
<section class="mf-prose-section is-light">
  <div class="container">
    <div class="row text-center">
      <div class="title-w-border-y"><h2>Discounted &amp; Free Admission</h2></div>
    </div>
    <ul class="mf-checklist">
      <li><strong>Educators:</strong> employees of schools, colleges, universities, and libraries receive free admission with identification. See our <a href="/educators/">Educators page</a> for requirements and restrictions.</li>
      <li><strong>Field Trip Day:</strong> on {{ site.data.settings.event_dates.edu_day | date: "%A, %B %-d" }}, students, teachers, and homeschool families enjoy a one-of-a-kind day of hands-on learning. <a href="/field-trip-day/">Learn more</a>.</li>
      <li><strong>Title I schools:</strong> registered groups from Title I schools receive free admission. See our <a href="/educators/">Educators page</a> for details.</li>
      <li><strong>First Responders, Active Military &amp; Veterans:</strong> free admission with identification — just bring your ID to the ticket booth for a free ticket per eligible person.</li>
      <li><strong>Making For All:</strong> individuals with an EBT card receive admission for only $5 per person, per day. Bring your EBT card to the ticket booth.</li>
    </ul>
  </div>
</section>

<!-- Good to know -->
<section class="mf-prose-section">
  <div class="container">
    <div class="row text-center">
      <div class="title-w-border-y"><h2>Good to Know</h2></div>
    </div>
    <ul class="mf-checklist">
      <li><strong>Weekend Passes</strong> cannot be shared between attendees.</li>
      <li><strong>Single Day Passes</strong> can be used on a single day — either Saturday or Sunday.</li>
      <li>You’ll receive an email confirmation after purchase with a link to print your tickets, or simply show them on your mobile device at the gate.</li>
      <li>No outside food or beverages are permitted through the gates unless you have special medical, dietary, or religious requirements. A wide variety of for-purchase food options will be available.</li>
      <li>Strollers, backpacks, and a bottle of water are allowed.</li>
      <li>No pets, for their safety. Trained service animals as defined by the ADA are welcome.</li>
      <li><strong>Anti-Harassment:</strong> we have a zero-tolerance policy for harassment of any kind. Please review our <a href="/anti-harassment/">Anti-Harassment Policy</a>.</li>
      <li>Follow us on social media or <a href="{{ site.data.settings.newsletter_url }}">subscribe to our newsletter</a> for announcements.</li>
    </ul>
  </div>
</section>

{% include cta-panel-widget.html cta_text="Questions? Email Us" cta_url="mailto:makers@makerfaireorlando.com" %}
