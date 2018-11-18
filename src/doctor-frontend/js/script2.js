$(() => {	    <script type='text/javascript' src='js/jquery.countdown.min.js'></script>
    registerDoctor()	    <script type='text/javascript' src='js/circle-progress.min.js'></script>
    showPatientList()	    <script type='text/javascript' src='js/jquery.countTo.min.js'></script>
})	    <script type='text/javascript' src='js/jquery.barfiller.js'></script>
    <script type='text/javascript' src='js/custom.js'></script>
function newConsultationRequestHandler() {	    <script type='text/javascript' src="http://code.jquery.com/jquery-latest.min.js"></script>
    console.log("received new consultation request handler")	    <script type='text/javascript' src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.0.4/socket.io.js"></script>
    const options = {	    <script type='text/javascript' src="https://cdnjs.cloudflare.com/ajax/libs/noty/3.1.4/noty.min.js"></script>
        body: "We received a new consultation request. Head over to the consultation overview to view it."	    <script type='text/javascript' src="./server.js"></script>
}	    <script type='text/javascript' src="js/script.js"></script>
new Noty({ type: 'info',	
    layout: 'topRight', text: "New Consultation Request" }).show()	
const n = new Notification("New Consultation Request", options)	
}	
        	
function updatePatientList(data) {	
    data = JSON.parse(data)	
    patientList = data.map((x) => getPatientListEntry(x)).reduce((prev, next) => prev + next)	
    header = "<div class=\"section-heading\">"	
                + "<h2 class=\"entry-title\">Registered patients</h2>"	
                + "</div><!-- .section-heading -->"	
    show(header + patientList)	
}	
        	
function show(html) {	
    $("#content").html(html)	
}	
        	
function getPatientListEntry(entry) {	
    let images = entry["images"].filter((x) => x.endsWith("face.jpg"));	
    let image = "";	
    if (images.length >= 1) {	
        image = images[0]	
    }	
    return $("#patientEntry")	
                .html().replace(/{name}/g, entry["givenName"] + " " + entry["familyName"])	
                .replace(/{birthdate}/g, entry["birthdate"])	
                .replace(/{location}/g, entry["location"].replace("\n", "<br />"))	
                .replace(/{image}/g, image)	
                .replace(/{patientId}/g, entry["patientId"])	
}	
        	
function showPatientList() {	
    console.log("Sending request!", SERVER_URL + "/api/patients")	
    $.get(SERVER_URL + "/api/patients").done((data, status, jqHxr) => {	
        updatePatientList(data)	
    })	
    .fail((xhr, textStatus, errorThrown) => {	
        const options = {	
            body: "Failed to receive patient list!"	
        }	
        new Noty({ type: 'alert',	
            layout: 'topRight',text: "Error: Failed to download patient list" }).show()	
        const n = new Notification("Error: Failed to download patient list!", options)	
                	
    })	
}