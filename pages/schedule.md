---
title: Event Schedule
layout: schedule
permalink: /schedule/
redirect_from: "/eventschedule/"
redirect_from: "/event-schedule/"
isotope-schedule: true
---

# Event Schedule

{% include schedule-update-warning.html %}

{% include schedule-in-progress-notice.html %}

Plan your weekend around the panel talks, demos and other scheduled activities below. Most [exhibits](/exhibits) and [hands-on activities](/exhibits/?categories/hands-on-workshop/) run continuously all weekend, so you can catch those in between.

The [event program](/program) has a printable map, schedule and more — it's usually posted about a week before the event.

[Field Trip Day](/field-trip-day) on {% include date-edu-short.html %} is only for pre-registered school groups and homeschool families.


<div class="mtm">
  <div class="mtm-search">
    <div class="container">
	  <div class="row">
        <div class="col-md-4">
            <label class="search-filter-label">Search:</label>
            <input type="text" class="quicksearch form-control" id="maker-search-input" placeholder="Looking for a specific Event?">
        </div>

        <div class="col-md-4">
          <!-- "Location", not "category": this dropdown filters on the event's
               stage/location. The id, class and ?category= deep link still say
               category and are left alone — schedule-filter.js and the CSS
               match on them, and old links to /schedule/?category=<slug> are
               out in the world. -->
          <label class="search-filter-label">Filter by location:</label>
          <select class="schedule-filters-select form-control" id="makers-category-select">
            <option value="" selected="">show all</option>
            {%- comment -%}
              The stages come from _data/schedule-stages.json, which the producer
              dashboard publishes beside _data/schedule.json. Do not type options
              here: a stage added in the builder would get none, which is how this
              dropdown once offered stages from a venue ago. `value` is the slug of
              the event's `location`, which is the class each row below carries.
            {%- endcomment -%}
            {%- for stage in site.data['schedule-stages'] %}
            <option value=".{{ stage.value }}">{{ stage.label }}</option>
            {%- endfor %}
          </select>
    	  </div>

        <div class="col-md-4">
          <label class="search-filter-label">Filter by day:</label>
          <select class="schedule-filters-select-day form-control" id="makers-day-select">
            <option value="" selected="">show all</option>
            <option value=".friday">Friday</option>
            <option value=".saturday">Saturday</option>
            <option value=".sunday">Sunday</option>
          </select>
    	  </div>

      </div><!-- #row -->
   </div><!-- #container -->
 </div><!-- #mtm-search -->
</div>

<div class="events-container" id="events">

    {%- comment -%}
      A heading starts each new day, so the list reads as Friday / Saturday /
      Sunday rather than one unbroken run of cards. The events come out of
      _data/schedule.json in date order, so "the day changed since the last
      row" is all it takes to know where a day begins. The heading carries the
      same day class as the rows below it; schedule-filter.js hides a heading
      whose whole day has been filtered away.
    {%- endcomment -%}
    {%- assign current_day = "" -%}
    {% for event in site.data.schedule %}
        {%- assign event_day = event.date | date: "%Y-%m-%d" -%}
        {%- if event_day != current_day -%}
        {%- assign current_day = event_day -%}
        <div class="day-heading {{ event.date | date: '%A' | slugify }}">
          <span class="day-heading-day">{{ event.date | date: "%A" }}</span>
          <span class="day-heading-date">{{ event.date | date: "%B %-d" }}</span>
        </div>
        {%- endif %}
        <div class="item {% if event.location %}{{event.location | prepend: " " | slugify}}{% endif %}
            {% if event.date %}{{event.date | date: "%A" | slugify}}{% endif %}" >

             {%- if event.location -%}
              <a name="{{event.slug}}"></a>
            {%- endif -%}
            <div class="container-fluid">
                <div class="row">
                    <div class="col-sm-2">
                       <b>{{event.date | date: "%A"}}<br>{{event.date | date: "%l:%M&nbsp;%P"}}
                        {% if event.enddate %}- {{event.enddate | date: "%l:%M&nbsp;%P"}}{% endif %}</b>

                         <br>
                        {% if event.location %}<br><b>{{event.location}}</b>{% endif %}
                    </div>
                    <div class="col-sm-2">
                        {% if event.url %}
                          <a href="{{event.url}}">
                        {% endif %}
                        <b>{{event.title}}</b>
                        {% if event.url %}
                          </a>
                        {% endif %}
                       
                    </div>
                    <div class="col-sm-5 text-wrap">
                        {{event.description}}<br>
                        {%- if event.guests -%}<br>Featuring: <br>{%- endif -%}
                         {%- for guest in event.guests -%}
                            {%-if guest.url -%}<a href="{{guest.url}}" target="_blank">{%- endif -%}
                              {{ guest.name }}
                            {%-if guest.url -%}</a>{%- endif -%}
                            {%- unless forloop.last -%}<br>{% endunless -%}
                         {%- endfor -%}   
                    </div>
                    <div class="col-sm-3">
                      {% if event.image %}
                        {% if event.url %}<a href="{{event.url}}">{% endif %}
                        <img src="{{event.image}}" style="padding:10px; max-width:100%;">
                        {% if event.url %}</a>{% endif %}
                      {% else %}
                        <img src="/assets/images/site-branding/makey.png" alt="Makey robot" style="padding:10px; max-width:100%">
                      {% endif %}
                    </div>
                </div>
            </div>


        </div>
{% endfor %}
</div>

<p id="schedule-no-results" style="display:none">No events match your search.</p>


Event schedule subject to change at any time based on the availability of exhibiting makers, special guests, and venue conditions.


## Need Tickets?
Hop over to our [tickets](/attend/) page for more information including our free ticket programs for first responders, educators, and veterans!



