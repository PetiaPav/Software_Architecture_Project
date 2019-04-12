//variable declaration
var myDialog; 
var current_event_object;
var removed_events = [];
var counter = 0;

// this runs after the page has been initialized
$(document).ready(function() {

     //defining the dialog
     myDialog = $('#event-modal').dialog({
        modal: true, 
        title: 'none', 
        width:350,
        autoOpen: false
    });

    $('#external-events .walk-in').each(function() {
        // store data so the calendar knows to render an event upon drop
        $(this).data('event', {
            title: 'Walk-in', // use the element's text as the event title
            stick: true, // maintain when user navigates (see docs on the renderEvent method)
            duration: '00:20:00',
            color: '#257e4a',  //defining the color of the draggeable object
            _id: 'walk-in'
        });
        // make the event draggable using jQuery UI
        $(this).draggable({
            zIndex: 999,
            revert: true,      // will cause the event to go back to its
            revertDuration: 0,  //  original position after the drag
        });
    });

    $('#external-events .annual').each(function() {
        // store data so the calendar knows to render an event upon drop
        $(this).data('event', {
            title: 'Annual', // use the element's text as the event title
            stick: true, // maintain when user navigates (see docs on the renderEvent method)
            duration: '01:00:00',
            color: '#257e4a', //defining the color of the draggeable object
            _id: 'annual'
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

        // Define header properties and buttons
        header: {
				left: 'prev,next today',
				center: 'title',
				right: 'agendaWeek,agendaDay'
			},

        // Default view upon opening calendar is weekly view
        defaultView: 'agendaWeek',
        firstDay: 1, // start week on Monday

        eventLimit: true, // allow "more" link when too many events

        // Limit hours visible per day
        minTime: '08:00:00',
        maxTime: '20:00:00',

        // Height of calendar
        contentHeight: 1000,


        // Grey out non-business hours
        businessHours: {
            dow: [ 0, 1, 2, 3, 4, 5, 6],   // Days of the week - Sunday to Saturday
            start: '08:00:00',
            end: '20:00:00'
        },

        // Frequency for displaying time slots, in minutes (20 minute partitions)
        slotDuration: '00:20:00',

        allDay: false,

        events: {
            url: 'doctor_schedule',
            editable: false,
            startEditable: false
        },    

        editable: false, //assured that the events are not extendible
        eventStartEditable  : true,
        eventOverlap: false,
        droppable: true, // this allows things to be dropped onto the calendar
        allDaySlot: false,

        //Open modal when an event is clicked and handle remove event functionality
        //If the event is a booked appointment send to backend to display an info page
        eventClick: function (eventObj){
            
            if(eventObj.color == 'orange'){
                $.ajax({
                    url: 'show_doctor_appointment_details',
                    type: 'POST',
                    contentType: 'application/json; charset=utf-8',
                    data: JSON.stringify({
                        title: eventObj.title,
                        start: eventObj.start
                    }),
                    success : function(res){
                        console.log('Response received')
                        console.log('Redirecting to ' + res)
                        window.location.href = res
                    }
                });
            }else{
                $('#calendar').fullCalendar('updateEvent', eventObj);

                //Set information to be displayed
                $('#appointment-type').html(eventObj.title);
                $('#startTime').html(moment(eventObj.start).format('MMM Do h:mm A'));
                $('#endTime').html(moment(eventObj.end).format('MMM Do h:mm A'));
                
                current_event_object = eventObj;
                myDialog.dialog('open');
            }
        },

        eventRender: function(eventObj){
            if(eventObj._id == 'walk-in'){
                eventObj._id = 'w' + get_counter();
            }else if (eventObj._id == 'annual'){
                eventObj._id = 'a' + get_counter();
            }
        }

    });
});

//method to send information to the back-end in a readable format
function send_to_backend(){
    var myEvents = $('#calendar').fullCalendar('clientEvents');
    var new_event;
    var list_of_events = [];
    var added_events = [];
    var i;
    
    //get the newly added events
    for(i = 0; i < myEvents.length; ++i) {
        if(myEvents[i].color == '#257e4a'){
            added_events.push(myEvents[i]);
        }
    }

    //add the newly added events to the schedule
    for(i = 0; i < added_events.length; i++) {
        new_event = {title: added_events[i].title, day: added_events[i].start.format('d'), time: added_events[i].start.format(), id: 'new-availability'};
        list_of_events.push(new_event);
    }

    //add the removed events from original schedule
    for(i = 0; i < removed_events.length; ++i) {
        new_event = {title: removed_events[i].title, day: removed_events[i].start.format('d'), time: removed_events[i].start.format(), id: 'removed-availability'};
        list_of_events.push(new_event);
    }

    $.ajax({
        url: 'doctor_update_schedule',
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        data: JSON.stringify(list_of_events),
        success : function(data){
            window.location.href = data['url']
        }
    });
    
}

//on-click method for Remove modal button
function remove_event(){
    
    //keep track of initial schedule events that have been removed
    if(current_event_object.color != '#257e4a'){
        removed_events.push(current_event_object);
    }

    $('#calendar').fullCalendar('removeEvents', current_event_object._id);
    myDialog.dialog('close');
}

//on-click method for Keep modal button
function keep_event() {
    myDialog.dialog('close');
}

//counter for unique ids
function get_counter() {
    counter++;
    return counter;
}
