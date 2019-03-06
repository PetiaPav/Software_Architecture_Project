// this runs after the page has been initialized
$(document).ready(function() {

    $('#external-events .walk-in').each(function() {
        // store data so the calendar knows to render an event upon drop
        $(this).data('event', {
            title: $.trim($(this).text()), // use the element's text as the event title
            stick: true, // maintain when user navigates (see docs on the renderEvent method)
            duration: '00:20:00',
            color: '#257e4a',  //defining the color of the draggeable object
        });
        // make the event draggable using jQuery UI
        $(this).draggable({
            zIndex: 999,
            revert: true,      // will cause the event to go back to its
            revertDuration: 0, //  original position after the drag
        });
    });

    $('#external-events .annual').each(function() {
        // store data so the calendar knows to render an event upon drop
        $(this).data('event', {
            title: $.trim($(this).text()), // use the element's text as the event title
            stick: true, // maintain when user navigates (see docs on the renderEvent method)
            duration: '01:00:00',
            color: '#257e4a' //defining the color of the draggeable object
        });
        // make the event draggable using jQuery UI
        $(this).draggable({
            zIndex: 999,
            revert: true,      // will cause the event to go back to its
            revertDuration: 0, //  original position after the drag
        });
    });

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
            dow: [ 0, 1, 2, 3, 4, 5, 6],   // Days of the week - Sunday to Saturday
            start: "08:00:00",
            end: "20:00:00",
        },

        // Frequency for displaying time slots, in minutes (20 minute partitions)
        slotDuration: "00:20:00",

        allDay: true,

        // Retrieve events using /data route
        events: { url: 'data' },

        // onClick of an event
		eventClick: function(eventObj) {
            $.ajax({
                url: 'data',
                type: 'POST',
                contentType: "application/json; charset=utf-8",
                dataType: 'json',
                data: JSON.stringify({title: eventObj.title, start: eventObj.start}),
                success : function(res){
                    console.log("Response received")
                }
            });
		},

        editable: false, //assured that the events are not extendible
        eventStartEditable  : true,
        eventOverlap: false,
        droppable: true, // this allows things to be dropped onto the calendar
        allDaySlot: false,

    });
});
