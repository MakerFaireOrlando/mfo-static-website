---
title: Event Schedule
layout: schedule
permalink: /schedule/
redirect_from: "/eventschedule/"
redirect_from: "/event-schedule/"
isotope-schedule: true
---

# Event Schedule




Use the schedule below to plan your weekend to catch the panel talks and other scheduled activities! Note that most of the [exhibits](/exhibits) and [hands-on activities](/exhibits/?categories/hands-on-workshop/) at Maker Faire Orlando happen continuously throughout the weekend. <BR>

Check out the [event program](/program) for a printable map, schedule and more!<br><br>


<div class="mtm">
  <div class="mtm-search">
    <div class="container">
	  <div class="row">
        <div class="col-md-4">
            <label class="search-filter-label">Search:</label>
            <input type="text" class="quicksearch form-control" id="maker-search-input" placeholder="Looking for a specific Event?">
        </div>

        <div class="col-md-4">
          <label class="search-filter-label">Filter by category:</label>
          <select class="schedule-filters-select form-control" id="makers-category-select">
            <option value="" selected="">show all</option>
            <option value=".power-racing-track">Power Racing</option>
            <option value=".main-stage">Main Stage</option>
            <option value=".outdoor-stage">Outdoor Stage</option>
            <option value=".robot-ruckus">Robot Ruckus</option>
          </select>
    	  </div>

        <div class="col-md-4">
          <label class="search-filter-label">Filter by day:</label>
          <select class="schedule-filters-select-day form-control" id="makers-category-select">
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

    {% for event in site.data.schedule %}
       
        <div class="item {% if event.location %}{{event.location | prepend: " " | slugify}}{% endif %}
            {% if event.date %}{{event.date | date: "%A" | slugify}}{% endif %}" >

             {%- if event.location -%}
              <a name="{{event.slug}}"></a>
            {%- endif -%}
            <div class="container">
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


Event schedule subject to change at any time based on the availability of exhibiting makers, special guests, and venue conditions.


## Need Tickets?
Hop over to our [tickets](/attend/) page for more information including our free ticket programs for first responders, educators, and veterans!



