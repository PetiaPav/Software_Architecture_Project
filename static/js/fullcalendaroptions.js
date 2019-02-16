// this runs after the page has been initialized

$(document).ready(function() {
    $('#calendar').fullCalendar({
        // put options and callbacks here
        schedulerLicenseKey: 'CC-Attribution-NonCommercial-NoDerivatives',
        defaultView: 'agendaWeek',

        // for example only, events sources should be fetched from the backend
        eventSources: [
        
            // event source : available slots    
                {
                    events: [
                        {
                            title : 'available 1',
                            start : '2019-02-16T08:00:00.000',
                            end : '2019-02-16T08:20:00.000'
                        },
                        {
                            title : 'available 2',
                            start : '2019-02-16T10:00:00.000',
                            end : '2019-02-16T010:20:00.000'
                        },
                        {
                            title : 'available 3',
                            start : '2019-02-16T11:00:00.000',
                            end : '2019-02-16T11:20:00.000'
                        },
                        {
                            title : 'available 4',
                            start : '2019-02-18T08:00:00.000',
                            end : '2019-02-18T08:20:00.000'
                        },
                        {
                            title : 'available 5',
                            start : '2019-02-18T09:20:00.000',
                            end : '2019-02-18T09:40:00.000'
                        }
                    ],
                    color: 'green',
                    textColor: 'black'
                },
                
            // event source : my desired appointment
                {
                    events: [
                        {
                            title : 'desired',
                            start : '2019-02-16T08:40:00.000',
                            end : '2019-02-16T09:00:00.000'
                        },
                        {
                            title : 'desired',
                            start : '2019-02-19T08:00:00.000',
                            end : '2019-02-18T08:20:00.000'
                        },
    
                    ],
                    color: 'red',
                    textColor: 'black'
                }
            ]
            

    })
    
}
    
    );