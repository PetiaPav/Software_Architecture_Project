//variable declaration
var myDialog; 
var current_event_object;

// this runs after the page has been initialized
$(document).ready(function() {
    
    //defining the dialog
    myDialog = $("#event-modal").dialog({
        modal: true, 
        title: "none", 
        width:350,
        autoOpen: false
    });

    $('#external-events .walk-in').each(function() {
        // store data so the calendar knows to render an event upon drop
        $(this).data('event', {
            title: $.trim($(this).text()), // use the element's text as the event title
            stick: true, // maintain when user navigates (see docs on the renderEvent method)
            duration: '00:20:00',
            color: '#257e4a',  //defining the color of the draggeable object
            _id: "walk-in"
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
            color: '#257e4a', //defining the color of the draggeable object
            _id: "annual"
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
        eventClick: function (eventObj){
            if(eventObj._id == "walk-in"){
                eventObj._id = "w" + get_counter();
            }else if (eventObj._id == "annual"){
                eventObj._id = "a" + get_counter();
            }
            $('#calendar').fullCalendar('updateEvent', eventObj);

            //Set information to be displayed
            $('#appointment-type').html(eventObj.title);
            $("#startTime").html(moment(eventObj.start).format('MMM Do h:mm A'));
            $("#endTime").html(moment(eventObj.end).format('MMM Do h:mm A'));
                
            myDialog.dialog('open');
            current_event_object = eventObj;
           
        }
    });
});

//method to send information to the back-end in a readable format
function send_to_backend(){
    var myEvents = $('#calendar').fullCalendar('clientEvents');

    var new_event;
    var list_of_events = [];

    var i;
    for(i = 0; i < myEvents.length; ++i) {
        new_event = {title: myEvents[i].title, day: myEvents[i].start.format('d'), time: myEvents[i].start.format('HH:mm')};
        list_of_events.push(new_event);
    }
    
    $.ajax({
        url: '/doctor_schedule',
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        dataType: 'json',
        data: JSON.stringify(list_of_events),
        success : function(data){
            window.location.href = data['url']
        }
    });
    
}

//on-click method for Remove modal button
function remove_event(){
    $('#calendar').fullCalendar('removeEvents', current_event_object._id);
    myDialog.dialog('close');
}

//on-click method for Keep modal button
function keep_event() {
    myDialog.dialog('close');
}

//counter for unique ids
counter = 0;
function get_counter() {
    counter++;
    return counter;
}