SERVER_URL = "https://ec2-18-203-236-54.eu-west-1.compute.amazonaws.com/"

function newConsultationRequestHandler() {
    console.log("received new consultation request handler")
    const options = {
        body: "We received a new consultation request. Head over to the consultation overview to view it."
    }
    new Noty({ type: 'info',
layout: 'topRight', text: "New Consultation Request" }).show()
    const n = new Notification("New Consultation Request", options)
}


function registerDoctor() {
    var doctor_socket = io.connect(SERVER_URL + "/patient")

    doctor_socket.on("connect", () => {
        console.log("[Patient] Connected!")
    })

    doctor_socket.on("take_picture_intent", () => {
        window.location.href="./camera.html?patientId="
    })


}

function redirectToIndex() {
    window.location.href="./patient_details.html"
}