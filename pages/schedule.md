---
title: Event Schedule
layout: schedule
permalink: /schedule/
redirect_from: "/eventschedule/"
redirect_from: "/event-schedule/"
isotope: true
---

# Event Schedule

<div class="mtm">
  <div class="mtm-search">
    <div class="container">
	  <div class="row">
        <div class="col-md-12">
            <label class="search-filter-label">Search:</label>
            <input type="text" class="quicksearch form-control" id="maker-search-input" placeholder="Looking for a specific Event?">
        </div>
      </div><!-- #row -->
   </div><!-- #container -->
 </div><!-- #mtm-search -->
</div>

<div class="exhibits-container" id="exhibits">
    {% for event in site.data.schedule %}
        <div style="width: 100%" class="item{% for category in exhibit.categories -%}
                          {% if category.name %}
                            {{- category.slug | prepend: " "-}}
                          {% endif %}
                          {%- endfor -%}">
          <table width="100%">
              <tr>
                  <td width="10%"><img src="{{event.image}}" style="padding:10px; max-width:100px;"></td>
                  <td width="20%" align="left" style="padding-left: 5px; padding-right: 10px;"><b>{{event.title}}</b></td>
                  <td width="30%" align="left" style="padding-right: 20px;">{{event.description}}</td>
                  <td width="15%" align="left">{{event.location}}</td>
                  <td width="20%" align="left">
                    {{event.date | date: "%A"}} {{event.date | date: "%l:%M %P"}}
                    {% if event.enddate %}- {{event.enddate | date: "%l:%M %P"}}{% endif %}
                    </td>

              </tr>
          </table>
        </div>
{% endfor %}
</div>

Event schedule subject to change at any time based on the availability of exhibiting makers, special guests, and venue conditions.

{%comment%}

#### Stay Tuned for exciting announcements including the new Maker Faire Stage with special guests, panel discussions, musical performances and more!



Most exhibits and hands-on experiences at Maker Faire Orlando run continuously throughout the event.


For competition times and more, check out our [event program](/program) below which has additional details. Click the images below for a PDF version of the program.


<a href="/assets/images/program/MFO_2022_Program.pdf"><img src="/assets/images/program/MFO_2022_Program_Page_1-web.jpg" alt="Maker Faire Orlando 2022 event program page 1" width="800" /></a>

<br>

<a href="/assets/images/program/MFO_2022_Program.pdf"><img src="/assets/images/program/MFO_2022_Program_Page_2-web.jpg" alt="Maker Faire Orlando 2022 event program page 2" width="800" /></a>


---

## Need Tickets?
Hop over to our [tickets](/attend) page for more information including our free ticket programs for first responders, educators, and veterans and details on how to win a professional 3D printer package from DeltaMaker 3D!


___

## Want Even More Maker Faire & Robot Ruckus fun with special guests and BattleBots Teams?
Check out the [Maker Faire Orlando & VIP Fundraiser](https://events.humanitix.com/mfo2022-vip-fundraiser) happening after-hours on Saturday the 5th after the first day of Maker Faire Orlando. This event requires a separate ticket. [Learn More](https://events.humanitix.com/mfo2022-vip-fundraiser)



---

Exhibiting makers and available experiences are subject to change based on community availablity.

{%endcomment%}
