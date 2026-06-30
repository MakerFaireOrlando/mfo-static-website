---
title: About Maker Faire Orlando
layout: full-width
permalink: /about/
description: Maker Faire Orlando is a community-organized, family-friendly celebration of science, art, technology, and hands-on making, produced by The Maker Effect Foundation.
image: /assets/images/slider/2025-ghostbusters.jpg
carousel: true
carousel-delay: 5000
carousel-controls: true
carousel-slides:
  - image: /assets/images/slider/2025-ghostbusters.jpg
    caption: Meet your heroes!
    url: /exhibits/

  - image: /assets/images/slider/2025-exploding-heads.jpg
    caption: Learn how to make something!
    url: /exhibits/categories/hands-on-workshop/

  - image: /assets/images/slider/2025-dumpster-fire.jpg
    caption: See racing action!
    url: /power-racing/
---

<!-- Lead intro -->
<section class="mf-prose-section">
  <div class="container">
    <div class="row text-center">
      <div class="title-w-border-y"><h1>About Maker Faire Orlando</h1></div>
    </div>
    <p class="mf-prose mf-lead text-center">A community-organized, family-friendly celebration of local do-it-yourself science, art, rockets, robots, crafts, technology, music, and hands-on activities.</p>
    <p class="mf-prose text-center">Maker Faire Orlando is an event where people show what they’re making and share what they’re learning. It’s produced by <a href="http://themakereffect.org/" title="The Maker Effect Foundation">The Maker Effect Foundation</a>, a 501(c)(3) public charity that funds maker programs in local schools, community groups, and makerspaces across Central Florida.</p>
  </div>
</section>

<!-- What is a Maker -->
<section class="mf-prose-section is-light">
  <div class="container">
    <div class="row text-center">
      <div class="title-w-border-y"><h2>What Is a Maker?</h2></div>
    </div>
    <p class="mf-prose text-center">We are parents, students, scientists, and garage tinkerers. We are young and old, and we all share a love for innovation, creativity, and inspiring others to make something — anything — as long as it makes people happy.</p>
  </div>
</section>

<!-- Maker Faire around the world -->
<section class="mf-prose-section">
  <div class="container">
    <div class="row text-center">
      <div class="title-w-border-y"><h2>Maker Faire Around the World</h2></div>
    </div>
    <p class="mf-prose">
      <a href="https://makerfaire.com/">Maker Faire</a> originated in 2006 in the San Francisco Bay Area as a project of the editors of <a href="https://makezine.com/">Make: magazine</a>. It has since grown into a significant <a href="https://makerfaire.com/map/">worldwide network</a> of both flagship and independently-produced events. Read more on <a href="https://makerfaire.com/makerfairehistory/">Maker Faire history</a>, the <a href="https://makerfaire.com/maker-movement/">Maker Movement</a>, and how to <a href="https://makerfaire.com/global/">start a Maker Faire</a> or a <a href="https://makerfaire.com/global/school/">School Maker Faire</a> where you live.
    </p>
  </div>
</section>

{% capture cta_event_text %}{% include date-event.html %} – {{ site.data.settings.event_hours }}{% endcapture %}
{% include cta-panel-widget.html cta_text=cta_event_text cta_subtext=site.data.settings.event_location_descr cta_url=site.data.settings.cta_event_url %}
