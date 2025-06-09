---
title: Event Schedule
layout: schedule
permalink: /schedule/
redirect_from: "/eventschedule/"
redirect_from: "/event-schedule/"
isotope: true
---

# Event Schedule


#### Stay Tuned for exciting announcements with scheduled activities, special guests, panel discussions, musical performances and more!

{% comment %}
Use the schedule below to plan your weekend to catch the panel talks and other scheduled activities! Note that most of the [exhibits](/exhibits) and [hands-on activities](/makers/?category=hands-on-workshop) at Maker Faire Orlando happen continuously throughout the weekend. <BR>

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
            <option value=".spirit-building">Spirit Building</option>
          </select>
    	  </div>

        <div class="col-md-4">
          <label class="search-filter-label">Filter by day:</label>
          <select class="schedule-filters-select-day form-control" id="makers-category-select">
            <option value="" selected="">show all</option>
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
       
        <div class="item {% if event.location %}
                            {{event.location | prepend: " " | slugify}}
                          {% endif %}
                          {% if event.date %}
                            {{event.date | date: "%A" | slugify}}
                          {% endif %}" >

             {% if event.location %}
              <a name="{{event.slug}}"></a>
            {% endif %}
            <div class="container" style="width=100%">
                <div class="row">
                    <div class="col-sm-2">
                      {% if event.image %}
                        {% if event.url %}
                          <a href="{{event.url}}">
                        {% endif %}
                        <img src="{{event.image}}" style="padding:10px; max-width:100%;">
                        {% if event.url %}
                          </a>
                        {% endif %}
                      {% else %}
                      <img src="/assets/images/site-branding/makey.png" style="padding:10px; max-width:100%;">
                      {% endif %}
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
                    <div class="col-sm-4 text-wrap">
                        {{event.description}}
                    </div>
                    <div class="col-sm-2">
                        {{event.location}}
                    </div>
                    <div class="col-sm-2">
                        <b>{{event.date | date: "%A"}} {{event.date | date: "%l:%M&nbsp;%P"}}
                        {% if event.enddate %}- {{event.enddate | date: "%l:%M&nbsp;%P"}}{% endif %}</b>
                    </div>
                </div>
            </div>


        </div>
{% endfor %}
</div>


Event schedule subject to change at any time based on the availability of exhibiting makers, special guests, and venue conditions.


## Need Tickets?
Hop over to our [tickets](/attend) page for more information including our free ticket programs for first responders, educators, and veterans!
{% endcomment %}


