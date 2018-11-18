SERVER_URL = "https://15530701.ngrok.io"

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
    var doctor_socket = io.connect(SERVER_URL + "/doctor")

    doctor_socket.on("connect", () => {
        console.log("[DOCTOR] Connected!")
    })
    doctor_socket.on("new_consultation_request", newConsultationRequestHandler)
    
    doctor_socket.on("show_patient_overview", (patient_id) => {
        window.location.href="./patient_details.html?patientId=" + patient_id
    })

    doctor_socket.on("show_consultation_list", () => {
        window.location.href="./consultation_list.html"
    })

    doctor_socket.on("show_patient_list", () => {
        window.location.href="./patient_list.html"
    })

    doctor_socket.on("patient_data", (data) => {
        console.log("[DOCTOR] patient data", data)
    })
}