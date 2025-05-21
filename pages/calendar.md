---
title: Calendar Test
layout: default
permalink: /calendar/
fullcalendar: true
---

# Calendar Test 
This is my test of fullcalendar


<div id='calendar'></div>

<script>

    document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'multiMonthFourMonth',
        views: {
            multiMonthFourMonth: {
            type: 'multiMonth',
            duration: { months: 2 }
            }
        },
        multiMonthMaxColumns: 1,
        validRange: {
            start: '2025-05-01',
            end: '2025-10-01'
        },
        
    });

    calendar.addEvent({
              title: '27: May 1 to May 8',
              start: '2025-05-01',
              allDay: true,
              backgroundColor: 'green'
            });
    calendar.addEvent({
                title: '9: 5/2 to 5/9',
                start: '2025-05-02',
                allDay: true,
                backgroundColor: 'yellow',
                borderColor: 'yellow',
                textColor: 'black'
                });
    calendar.addEvent({
                title: '3 villas 5/3 to 5/10',
                start: '2025-05-03',
                allDay: true,
                backgroundColor: 'red'
                });
    calendar.addEvent({
                title: '22 villas',
                start: '2025-05-04',
                allDay: true
                });
    calendar.addEvent({
                title: '42 villas',
                start: '2025-05-05',
                allDay: true
                });

    calendar.render();
    });
</script>

