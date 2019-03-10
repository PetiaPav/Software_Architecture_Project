// this runs after the page has been initialized
$(document).ready(function() {
    var startOfWeek;
    var endOfWeek;

    $('#calendar').fullCalendar({
        // Define fullcalendar license key
        schedulerLicenseKey: 'CC-Attribution-NonCommercial-NoDerivatives',

        // Define header properties and buttons
        header: {
				left: 'prev,next today',
				center: 'title',
				right: 'agendaWeek,agendaDay'
			},

        // Default view upon opening calendar is weekly view
        defaultView: 'agendaWeek',

        eventLimit: true, // allow "more" link when too many events

        // Limit hours visible per day
        minTime: "08:00:00",
        maxTime: "20:00:00",

        // Height of calendar
        contentHeight: 1000,


        // Grey out non-business hours
        businessHours: {
            dow: [0, 1, 2, 3, 4, 5, 6],   // Days of the week - Mon to Fri
            start: "08:00:00",
            end: "20:00:00",
        },

        // Frequency for displaying time slots, in minutes (20 minute partitions)
        slotDuration: "00:20:00",

        allDay: true,

        events: {
             url: 'data'
        },

        // onClick of an event
		eventClick: function(eventObj) {
            $.ajax({
                url: 'event',
                type: 'POST',
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify({
                    id: eventObj.id,
                    start: eventObj.start,
                    end: eventObj.end
                }),
                success : function(res){
                    console.log("Response received")
                    console.log("Redirecting to " + res)
                    window.location.href = res
                }
            });
		},
    });
});
