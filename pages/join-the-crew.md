---
title: Join the Crew
permalink: /join-the-crew/
layout: full-width
description: Maker Faire Orlando is an all-volunteer crew. Take on a real role, build new skills, and help bring the Greatest Show (& Tell) on Earth to life.
image: /assets/images/slider/happy-crew.jpg
carousel: true
carousel-delay: 5000
carousel-controls: true
hero-title: Maker Faire Orlando is <span class="mf-hl">powered by people</span>
hero-meta: Join the crew behind the Greatest Show (&amp; Tell) on Earth
carousel-slides:
  - image: /assets/images/slider/happy-crew.jpg
    caption: The Maker Faire Orlando crew at work
    url:
  - image: /assets/images/slider/2025-volunteer-greeters.jpg
    caption: Crew members welcoming attendees at the gate
    url:
  - image: /assets/images/slider/2025-volunteer-curiousity.jpg
    caption: Volunteers helping makers share what they have built
    url:
scrolltop: true
---

{% comment %}
  Evergreen crew recruitment page. Roles come from _data/crew-roles.yaml.
  Add or retire a role there, not here. Keep this page year-agnostic: no
  dates, no event year, no attendance figures.
{% endcomment %}

{% assign featured_roles = site.data.crew-roles.roles | where: "featured", true %}
{% assign all_roles = site.data.crew-roles.roles | sort: "name" %}

<!-- Lead intro. No heading here on purpose: the carousel hero overlay already
     supplies the page's single <h1>. -->
<section class="mf-prose-section">
  <div class="container">
    <p class="mf-prose mf-lead text-center">Every unforgettable moment at {{ site.data.settings.event_name }} happens because volunteers made it happen: every wide-eyed kid, every packed stage talk, every “how did they build that?” We’re an all-volunteer crew, and we’re always looking for more hands, more ideas, and more heart.</p>
    <p class="mf-prose text-center">You don’t need experience. You need curiosity and a willingness to pitch in. In return, you’ll build real skills, take on leadership, and grow in ways that follow you long after the weekend ends.</p>
    <p class="text-center" style="margin-top:28px;">
      <a class="btn btn-primary" href="mailto:{{ site.data.settings.contact_email }}?subject=I want to join the crew">Email the Crew</a>
    </p>
  </div>
</section>

<!-- Mission -->
<section class="mf-prose-section is-light">
  <div class="container">
    <div class="row text-center">
      <div class="title-w-border-y"><h2>Why We Do This</h2></div>
    </div>
    <p class="mf-prose mf-lead text-center">{{ site.data.settings.event_name }} is produced by The Maker Effect Foundation, a 501(c)(3) public charity with a simple mission: <strong>to activate and amplify the efforts of makers as they learn, build, and work together in their communities.</strong></p>
    <p class="mf-prose text-center">{{ site.data.settings.event_name }} is one way we live that mission: a weekend where thousands of makers show what they’ve made and share what they’ve learned, and where thousands of students discover what they might make next. When you join the crew, you’re not just running an event. You’re helping build a stronger maker community across Central Florida.</p>
  </div>
</section>

<!-- What you'll gain -->
<section class="mf-card-section">
  <div class="container">
    <div class="mf-section-head">
      <h2>Stretch Your Skills. Lead a Team. Grow.</h2>
      <p>Crewing {{ site.data.settings.event_name }} isn’t just giving your time. It’s a chance to build real experience you can carry anywhere. Take on responsibility, learn something new, and flex skills you don’t get to use in your day job.</p>
    </div>
    <div class="mf-info-grid">
      <div class="mf-info-card">
        <i class="mf-info-icon fa-solid fa-compass-drafting" aria-hidden="true"></i>
        <h3>Leadership</h3>
        <p>Own a piece of a large live event, make real decisions, and guide a team to pull it off.</p>
      </div>
      <div class="mf-info-card">
        <i class="mf-info-icon fa-solid fa-screwdriver-wrench" aria-hidden="true"></i>
        <h3>New Skills</h3>
        <p>From event production to AV to people management, pick up hands-on experience with room to learn as you go.</p>
      </div>
      <div class="mf-info-card">
        <i class="mf-info-icon fa-solid fa-handshake" aria-hidden="true"></i>
        <h3>A Real Network</h3>
        <p>Work alongside makers, organizers, and professionals across Central Florida’s creative and tech community.</p>
      </div>
    </div>
  </div>
</section>

<!-- Featured roles (jump links into the full list below) -->
<section class="mf-card-section is-light">
  <div class="container">
    <div class="mf-section-head">
      <h2>Roles We’re Looking to Fill</h2>
      <p>Three spots where the right person makes an outsized difference. Pick one to read the full role.</p>
    </div>
    <div class="mf-info-grid">
      {% for role in featured_roles %}
      <a class="mf-info-card" href="#{{ role.id }}">
        <i class="mf-info-icon {{ role.icon }}" aria-hidden="true"></i>
        <h3>{{ role.name }}</h3>
        <p>{{ role.teaser }}</p>
        <span class="mf-link-arrow">Read the full role</span>
      </a>
      {% endfor %}
    </div>
  </div>
</section>

<!-- No experience needed -->
<section class="mf-prose-section">
  <div class="container">
    <div class="mf-apply-callout">
      <h2>No Experience? No Problem.</h2>
      <p>None of our roles require prior experience. We’re looking for passionate people who want to make a difference, and we’ll train you on everything else. Show up curious, and we’ll take it from there.</p>
    </div>
  </div>
</section>

<!-- Full role descriptions -->
<section class="mf-card-section is-light">
  <div class="container">
    <div class="mf-section-head">
      <h2>The Roles in Detail</h2>
      <p>What each role actually does, and who tends to love it.</p>
    </div>
    <div class="mf-roles mf-crew-roles">
      {% for role in all_roles %}
      <div class="mf-role" id="{{ role.id }}">
        <i class="mf-role-icon {{ role.icon }}" aria-hidden="true"></i>
        <div class="mf-role-body">
          <h3>{{ role.name }}</h3>
          {% for paragraph in role.body %}
          <p>{{ paragraph }}</p>
          {% endfor %}
          {% if role.great_for %}
          <p><strong>Great for:</strong> {{ role.great_for }}</p>
          {% endif %}
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
</section>

<!-- Already attending or exhibiting -->
<section class="mf-prose-section is-dark">
  <div class="container">
    <div class="row text-center">
      <div class="title-w-border-y"><h2>A Booked Weekend Is No Barrier</h2></div>
    </div>
    <p class="mf-prose text-center">Already planning to attend or exhibit? You can still pitch in. We have plenty of ways to help before the event and in the days right after, so even a full weekend doesn’t have to keep you off the crew. Reach out and we’ll find something that fits around your plans.</p>
  </div>
</section>

<!-- Smaller commitment off-ramp -->
<section class="mf-prose-section">
  <div class="container">
    <div class="mf-apply-callout is-open">
      <h2>Only Have a Few Hours?</h2>
      <p>You don’t have to take on a whole role to make a difference. If you’ve only got a few hours over the weekend, our standard volunteer shifts are a perfect way to jump in and help.</p>
      <a class="btn btn-primary" href="{{ '/volunteer/' | relative_url }}">See Volunteer Roles</a>
    </div>
  </div>
</section>

<!-- Final CTA -->
<section class="mf-prose-section is-dark">
  <div class="container">
    <div class="row text-center">
      <div class="title-w-border-y"><h2>Raise Your Hand</h2></div>
    </div>
    <p class="mf-prose text-center">Tell us you’re interested. You don’t need to know which role yet. We’ll talk through what we need and help you find your place on the crew.</p>
    <p class="text-center" style="margin-top:28px;">
      <a class="btn btn-primary" href="mailto:{{ site.data.settings.contact_email }}?subject=I want to join the crew">Email the Crew</a>
      <a class="btn btn-w-ghost" href="{{ '/volunteer/' | relative_url }}" style="margin-left:10px;">Volunteer Info</a>
    </p>
  </div>
</section>
