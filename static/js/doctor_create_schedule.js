// this runs after the page has been initialized
$(document).ready(function() {

    $('#external-events .walk-in').each(function() {
        // store data so the calendar knows to render an event upon drop
        $(this).data('event', {
            title: $.trim($(this).text()), // use the element's text as the event title
            stick: true, // maintain when user navigates (see docs on the renderEvent method)
            duration: '00:20:00',
            color: '#257e4a'  //defining the color of the draggeable object
        });
        // make the event draggable using jQuery UI
        $(this).draggable({
            zIndex: 999,
            revert: true,      // will cause the event to go back to its
            revertDuration: 0  //  original position after the drag
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
            revertDuration: 0  //  original position after the drag
        });
    });

    $('#calendar').fullCalendar({
        // Define fullcalendar license key
        schedulerLicenseKey: 'CC-Attribution-NonCommercial-NoDerivatives',

        // Have an empty header
        header: false,

        // Default view upon opening calendar is weekly view
        defaultView: 'agendaWeek',
        
        columnHeaderFormat: 'dddd',

        eventLimit: true, // allow "more" link when too many events

        // Limit hours visible per day
        minTime: "08:00:00",
        maxTime: "20:00:00",

        // Height of calendar
        contentHeight: 1000,


        // Grey out non-business hours
        businessHours: {
            dow: [0, 1, 2, 3, 4, 5, 6],   // Days of the week - Sunday to Saturday
            start: "08:00:00",
            end: "20:00:00"
        },

        // Frequency for displaying time slots, in minutes (20 minute partitions)
        slotDuration: "00:20:00",

        allDay: true,

        // Test set of events
        events: {},

        editable: false, //assured that the events are not extendible
        eventStartEditable  : true,
        eventOverlap: false,
        droppable: true, // this allows things to be dropped onto the calendar
        allDaySlot: false,

        //Making the week generic with no dates
        viewRender: function() {
            $('.fc-day-header.fc-sun').html('Sunday');
            $('.fc-day-header.fc-mon').html('Monday');
            $('.fc-day-header.fc-tue').html('Tuesday');
            $('.fc-day-header.fc-wed').html('Wednesday');
            $('.fc-day-header.fc-thu').html('Thursday');
            $('.fc-day-header.fc-fri').html('Friday');
            $('.fc-day-header.fc-sat').html('Saturday');
        },

        //Open modal when an event is clicked and handle remove event functionality
        //TO BE CONTINUED/FIXED, Remembers previous event id's
        eventClick: function (eventObj){
            //Set information to be displayed
            $('#appointment-type').html(eventObj.title);
            $("#startTime").html(moment(eventObj.start).format('MMM Do h:mm A'));
            $("#endTime").html(moment(eventObj.end).format('MMM Do h:mm A'));
                
            //Open modal 
            var myDialog = $("#event-modal").dialog({
                modal: true, 
                title: eventObj.title, 
                width:350
            });

            // To keep availability simply close the modal
            $('.keep-button').click(function() {
                $(myDialog).dialog('close');
            });

            // To remove the availability and close the modal
            $('.remove-button').click( function(){
                $('#calendar').fullCalendar('removeEvents', eventObj._id);
                $(myDialog).dialog('close');
            });
        },

    });
});
