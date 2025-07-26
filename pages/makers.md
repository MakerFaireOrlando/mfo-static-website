---
title: Exhibits
layout: full-width
permalink: /makers/
isotope: true
redirect-from:
  - /exhibits/
scrolltop: true
---
<div class="container">
{% if site.data.settings.maker_exhibits_holdover %}
<h1>Maker Exhibits from {{site.event_year | minus: 1 }}</h1>

  {% if site.data.settings.call_for_makers_open %}
  We haven't started approving exhibits for Maker Faire Orlando {{site.event_year}}, but you can see our past exhibits below get a feel for the event!<br><br>
  {% else %}
  We haven't opened our Call For Makers yet for {{site.event_year}}, but you can see our past exhibits below to see the type of exhibits you can find at Maker Faire Orlando!<br><br>
  {% endif %}

{% else %}
<h1>Maker Exhibits</h1>
{% endif %}

<p>Interested in Exhibiting at Maker Faire Orlando? <a href="/exhibit-at-maker-faire-orlando/">Learn more about exhibiting!</a> </p>

<p>Want to see all the BattleBots and other combat robots participating in <a href="http://www.robotruckus.org">Robot Ruckus</a>? Head over to the <a href="http://www.robotruckus.org">Robot Ruckus website</a> for details and check out the <a href="/makers/?category=combat-robots">Combat Robots category</a> on this page!</p>



</div>

<div class="mtm">
  <div class="mtm-search">
    <div class="container">
	   <div class="row">
      <div class="col-md-6">
      	<label class="search-filter-label">Search:</label>
      	<input type="text" class="quicksearch form-control" id="maker-search-input" placeholder="Looking for a specific Exhibit or Maker?">
      </div>

    	<div class="col-md-4">
    		<label class="search-filter-label">Filter by category:</label>
    		<select class="filters-select form-control" id="makers-category-select">
     		<option value="*" selected="">show all</option>
        {% include category-options.html %}
    		        </select>
    	</div><!-- #col -->
      <div class="col-md-2">
        <label class="search-filter-label">Explore:</label>
        <button id="shuffle">Shuffle Exhibits</button>
      </div>

	   </div><!-- #row -->
   </div><!-- #container -->
 </div><!-- #mtm-search -->
</div>

<div class="exhibits-container" id="exhibits">
  {% for exhibit in site.exhibits %}

      <div class="item{% for category in exhibit.categories -%}
                        {% if category.name %}
                          {{- category.slug | prepend: " "-}}
                        {% endif %}
                        {%- endfor -%}">

        {%comment%}<div class="excerpt-container">{{exhibit.description}}</div>{%endcomment%}
        <div class="img-container"><a href="{{exhibit.url}}">
          <img src="{{exhibit.image-primary.medium}}" alt="{{exhibit.title}}" style="width:300px; height:auto"></a>
        </div>
        <div class="title-container"><a href="{{exhibit.url}}">{{exhibit.title}}</a></div>
        <div class="description-container" style="display:none">{{exhibit.description}}</div>
      </div>


{% comment %}
        <div id="{{ exhibit.slug }}">
          <img src="{{ exhibit.image-primary.small }}">
        <a href="{{ exhibit.url }}">{{ exhibit.name }}</a>
        </div>
{% endcomment %}

{% endfor %}
</div>
