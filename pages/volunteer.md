---
title: Volunteer at Maker Faire Orlando!
layout: default
image: /assets/images/volunteer-solder.jpg
permalink: /volunteer/
redirect_from: /volunteers/
carousel: true
carousel-delay: 5000
carousel-controls: false
carousel-slides:
  - image: /assets/images/volunteer-solder.jpg
    caption: Learn-To-Solder
    url:
---




{%comment%}
# Thanks for Volunteering for {{site.event_name}} {{site.event_year}}
The event is now underway and we have closed volunteer registration. If you've already registered and have questions, please email us at <makers@makerfaireorlando.com>
{%endcomment%}


# We Need You!
Volunteering at {{site.event_name}} {{site.event_year}} is a great way to give back to your local community AND to attend the event without needing to buy a ticket!

Volunteers who work at least a 4 hour shift will receive free admission for the day they volunteer (if you volunteer late in the day, you are welcome to enjoy the event before your volunteer shift, and if you volunteer for setup day, you can come back for a full day on either Saturday or Sunday). Volunteers also receive a {{site.event_name}} {{site.event_year}} volunteer t-shirt.

# Volunteer registration typically opens in September, please check back or follow us on social media.

{%comment%}
# Volunteering at {{site.event_name}} {{site.event_year}}


---

### More Details
* {{site.event_name}} volunteers must be 13 years of age or older. (Some roles require 16+ or 18+)
* Community service hours are available from The Maker Effect Foundation, a 501(c)(3) public charity.
* If you have any questions about volunteering at {{site.event_name}}, or if you have a specific skill-set (especially photography/videography) not listed below, please email us at <makers@makerfaireorlando.com>

---

### Sign up to Volunteer
You can register for open volunteer shifts by scrolling to the list of available shifts (General Volunteer, Greeter, etc.) at the bottom of this page. If you have any challenges registering, or if your availability changes, email us at <makers@makerfaireorlando.com>.

Notes:
* We are using the Humanitix platform to register volunteers with a "ticket", but there is no cost involved.
* The Learn to Solder activity will be staffed by a FIRST robotics team this year and does not have any available volunteer shifts.

---
### Volunteer Shifts

<iframe id="iframe-container" src="https://events.humanitix.com/maker-faire-orlando-2023-volunteer-signup/tickets?w=true&p=%23353337" width="100%" height="600px" frameborder="0"></iframe>
<script>
  var humanitix = {
      findPos: function(obj) {
          var curtop = 0;
          if (obj.offsetParent) {
          do {
              curtop += obj.offsetTop;
          } while ((obj = obj.offsetParent));
          return [curtop];
          }
      }
  };
  window.addEventListener('message', function (e) {
      if (e.origin !== "https://events.humanitix.com"){
          return;
      }   
      var messageData = e.data;
      var iframeEl = document.getElementById('iframe-container');
      if (iframeEl && messageData && !isNaN(messageData.scrollHeight)){
          iframeEl.style.height = messageData.scrollHeight + 'px';
      }
      if (iframeEl && messageData && messageData.pageChange) {
        window.scroll(0, humanitix.findPos(iframeEl));
    }

  }, false);
</script>
{%endcomment%}
