---
title: Attend Maker Faire Orlando
permalink: /attend/
image: /assets/images/slider/family-makey-gate.jpg  
layout: default
redirect_from:
  - /ticket/
  - /tickets/


carousel: true
carousel-delay: 5000
carousel-controls: false
carousel-slides:
  - image: /assets/images/slider/family-makey-gate.jpg  
    caption: Family at Maker Faire
    url:
scrolltop: true
---

# Maker Faire Orlando {{site.event_year}} - {{site.event_date_descr_month_day}}
#### Maker Faire Orlando is a non-profit, community-organized, family-friendly celebration featuring local do-it-yourself science, art, rockets, robots, crafts, technology, music, hands-on-activities, and more.


Saturday, November 4 & Sunday, November 5 - 10AM to 5PM (Both Days)

Central Florida Expo Center & Fairgrounds
4603 W Colonial Dr, Orlando, FL 32808

**Parking is FREE!**

Explore more than [200 Exhibits and Hands-on Activities](/makers) to find your favorites!

Check out the [Event Program, Map & Schedule](/program) to plan your weekend!


---

## Win a Professional 3D Printer!
By purchasing a ticket to Maker Faire Orlando online **by November 3rd, 2022**, you are automatically entered to win a DeltaMaker 3D Printer!*  

![3D Printer giveaway](/assets/images/deltamaker-giveaway.jpg)



---

## Tickets
Tickets available on [Humanitix](https://events.humanitix.com/makerfaireorlando) or use the ticket form below - Humanitix donates 100% of profits to children's charities!


---

<iframe id="iframe-container" src="https://events.humanitix.com/makerfaireorlando/tickets?w=true&p=%23353337" width="100%" height="600px" frameborder="0"></iframe>
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

---
{%comment%}
### Looking for an Exclusive Experience with Makers, Interactive Artists & BattleBots Teams?
Check out the [Maker Faire Orlando & Robot Ruckus VIP Fundraiser](https://events.humanitix.com/mfo2022-vip-fundraiser) happening after-hours on Saturday the 5th after the first day of Maker Faire Orlando. This event requires a separate ticket. [Learn More](https://events.humanitix.com/mfo2022-vip-fundraiser)

---
{%endcomment%}

Follow us on social media or [subscribe to our email newsletter]( {{ site.newsletter_url }} ) for announcements.

**Homeschool educators receive free admission** to Maker Faire Orlando {{site.event_year}} with identification and documentation.
Please see our [Homeschool Programs page](/homeschool) for more information including requirements and restrictions.

**Employees of schools, colleges, universities, and libraries** receive free admission to Maker Faire Orlando {{site.event_year}} with identification.
Please see our [Educators page](/educators) for more information including requirements and restrictions.

**Registered groups from Title I schools receive free admission** to Maker Faire Orlando {{site.event_year}}.
Please see our [Educators page](/educators) for more information.

**First Responders, Active Military and Veterans receive free admission** to Maker Faire Orlando {{site.event_year}} with identification. Simply bring your identification to the ticket booth at the event to receive a free ticket per eligible person with identification.

**Anti-Harassment Policy** Maker Faire Orlando has a zero-tolerance policy for harassment of any kind. Please see our [Anti-Harassment Policy](/anti-harassment) for more information.

---

**Questions? Email <makers@makerfaireorlando.com>**

---
{%comment%}
*No Purchase Necessary. Tickets must be purchased by 11/4/2021. To receive a single entry for the DeltaMaker 3D Printer giveaway, mail your contact information (name, email address and phone number) to Maker Faire Orlando 3D Printer Giveaway c/o The Maker Effect Foundation, PO Box 3142, Windermere, FL 34786. Entries must be postmarked no later than 11/4/2021.
{%endcomment%}
