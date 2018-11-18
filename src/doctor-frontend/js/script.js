$(() => {
                registerDoctor()
                showPatientList()
            })

            function newConsultationRequestHandler() {
                console.log("received new consultation request handler")
                const options = {
                    body: "We received a new consultation request. Head over to the consultation overview to view it."
                }
                new Noty({ type: 'info',
    layout: 'topRight', text: "New Consultation Request" }).show()
                const n = new Notification("New Consultation Request", options)
            }

        function updatePatientList(data) {
            data = JSON.parse(data)
            patientList = data["consultations"].map((x) => getPatientListEntry(x, data["patients"][x["patientId"]])).reduce((prev, next) => prev + next)
            header = "<div class=\"section-heading\">"
                        + "<h2 class=\"entry-title\">Requested Consultations</h2>"
                        + "</div><!-- .section-heading -->"
            show(header + patientList)
        }

        function show(html) {
            $("#content").html(html)
        }

        function getPatientListEntry(entry, person) {
            let image = person["image"]
            return $("#patientEntry")
                        .html().replace(/{name}/g, person["givenName"] + " " + person["familyName"])
                        .replace(/{birthdate}/g, person["birthdate"])
                        .replace(/{location}/g, (entry["message"] || " ").replace("\n", "<br />"))
                        .replace(/{image}/g, image)
        }

        function showPatientList() {
            console.log("Sending request!", SERVER_URL + "/api/consultations")
            $.get(SERVER_URL + "/api/consultations").done((data, status, jqHxr) => {
                console.log("got result!")
                updatePatientList(data)
            })
            .fail((xhr, textStatus, errorThrown) => {
                const options = {
                    body: "Failed to receive consultation list!"
                }
                new Noty({ type: 'alert',
    layout: 'topRight',text: "Error: Failed to download consultation list" }).show()
                const n = new Notification("Error: Failed to download consultation list!", options)

            })
        }