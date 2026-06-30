---
title: The Greatest Show (& Tell) on Earth!
permalink: /
layout: full-width
image: /assets/images/slider/welcome-to-maker-faire.jpg  
scrolltop: true
carousel: true
carousel-delay: 5000
carousel-controls: true
carousel-slides:
  - image: /assets/images/slider/2025-rebels.jpg
    caption: The Greatest Show (& Tell) on Earth!
  - image: /assets/images/slider/2025-cosplay-exhibit.jpg
    caption: Meet Award-Winning Cosplay Makers!
    url: /exhibits/categories/cosplay/
  - image: /assets/images/slider/2025-synths.jpg
    caption: Make Music!
  - image: /assets/images/slider/2025-dumpster-fire.jpg
    caption: Pow-Pow-Power Racing!
    url: /power-racing/
---

{% capture cta_event_text %}{% include date-event.html %} – {{ site.data.settings.event_hours }}{% endcapture %}{% include cta-panel-widget.html cta_text=cta_event_text cta_subtext=site.data.settings.event_location_descr cta_url=site.data.settings.cta_event_url %}

{% include what-is-maker-faire.html %}

{% include category-cards.html %}

{% include get-involved-cards.html %}


{% if site.data.settings.featured_makers %}
{% include featured-makers-grid.html %}
{% endif %}


{% if site.data.settings.event_shirt_promo %}
{% include event-shirt.html %}
{% endif %}

{% if site.data.settings.call_for_makers_open %}
{% include call-for-makers-widget.html %}
{% endif %}


{% comment %}

<section class="content-panel">
<div class="container">
<div class="row">
<div class="col-xs-12 text-center padbottom">
<h2>Save The Dates!</h2>
</div>
</div>
<div class="row">
<div class="col-sm-3"></div>
<div class="col-sm-6 text-center">
<img class="aligncenter size-full " src="assets/images/site-branding/2021/MFO2021_Round_logo_V3_w_date.png" alt="MFO2021 Logo" width="340" height="340"><p></p>
<p style="margin: 20px 30px 5px 30px">Maker Faire Orlando is back for 2021! We are excited to bring the maker community back together so that everyone can show off their projects, meet new makers and reconnect with some of your favorite makers from prior years.</p>
<p style="margin: 5px 30px 5px 30px;font-weight: bold;text-align: center"><a href="/exhibit-at-maker-faire-orlando">Interested in Exhibiting?</a></p>
</div>
</div>
</div>
<div class="flag-banner"></div>
</section>
{% endcomment %}


{% comment %}
<section class="content-panel">
<div class="container">


    <div class="row text-center">
      <div class="title-w-border-y">
      <h2>Maker Faire Orlando 2022 Program</h2>
      </div>
    </div>

<div class="row">
<div class="col-sm-6 text-center">
<a href="/assets/images/program/MFO_2022_Program.pdf"><img src="/assets/images/program/MFO_2022_Program_Page_1-web.jpg" alt="Maker Faire Orlando 2022 event program page 1" width="400" /></a>
</div>

<div class="col-sm-6 text-center">
<a href="/assets/images/program/MFO_2022_Program.pdf"><img src="/assets/images/program/MFO_2022_Program_Page_2-web.jpg" alt="Maker Faire Orlando 2022 event program page 2" width="400" /></a>

</div>
</div>
</div>
<div class="flag-banner"></div>
</section>
{% endcomment %}

{% include sponsors-marquee.html %}
