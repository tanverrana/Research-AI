// ==========================================
// TOOL SWITCHING
// ==========================================

function switchTool(tool) {

    const analysisSection =
        document.getElementById("analysisSection");

    const titleSection =
        document.getElementById("titleSection");

    const analysisTab =
        document.getElementById("analysisTab");

    const titleTab =
        document.getElementById("titleTab");


    if (tool === "analysis") {

        analysisSection.classList.remove("hidden");

        titleSection.classList.add("hidden");

        analysisTab.classList.add("active");

        titleTab.classList.remove("active");

    }


    if (tool === "title") {

        titleSection.classList.remove("hidden");

        analysisSection.classList.add("hidden");

        titleTab.classList.add("active");

        analysisTab.classList.remove("active");

    }

}



// ==========================================
// RESEARCH ANALYSIS
// ==========================================

async function generateResearch() {

    const topic =
        document.getElementById("researchTopic").value.trim();

    const field =
        document.getElementById("researchField").value;

    const button =
        document.getElementById("researchButton");

    const loading =
        document.getElementById("researchLoading");

    const result =
        document.getElementById("researchResult");

    const output =
        document.getElementById("researchOutput");


    if (!topic) {

        alert("Please enter a research topic.");

        return;

    }


    button.disabled = true;

    button.style.opacity = "0.6";

    loading.style.display = "flex";

    result.style.display = "none";


    try {

        const response = await fetch(
            "/generate-research",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    topic: topic,
                    field: field
                })
            }
        );


        const data = await response.json();


        if (!data.success) {

            throw new Error(
                data.error || "Something went wrong."
            );

        }


        output.textContent = data.result;

        result.style.display = "block";


        result.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });


    } catch (error) {

        alert(
            "Error: " + error.message
        );

    } finally {

        button.disabled = false;

        button.style.opacity = "1";

        loading.style.display = "none";

    }

}



// ==========================================
// TITLE GENERATOR
// ==========================================

async function generateTitles() {

    const topic =
        document.getElementById("titleTopic").value.trim();

    const button =
        document.getElementById("titleButton");

    const loading =
        document.getElementById("titleLoading");

    const result =
        document.getElementById("titleResult");

    const output =
        document.getElementById("titleOutput");


    if (!topic) {

        alert("Please enter your research idea.");

        return;

    }


    button.disabled = true;

    button.style.opacity = "0.6";

    loading.style.display = "flex";

    result.style.display = "none";


    try {

        const response = await fetch(
            "/generate-title",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    topic: topic
                })
            }
        );


        const data = await response.json();


        if (!data.success) {

            throw new Error(
                data.error || "Something went wrong."
            );

        }


        output.textContent = data.result;

        result.style.display = "block";


        result.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });


    } catch (error) {

        alert(
            "Error: " + error.message
        );

    } finally {

        button.disabled = false;

        button.style.opacity = "1";

        loading.style.display = "none";

    }

}



// ==========================================
// COPY RESULT
// ==========================================

async function copyResult(elementId) {

    const element =
        document.getElementById(elementId);

    const text =
        element.innerText;


    try {

        await navigator.clipboard.writeText(text);

        alert("Result copied to clipboard.");

    } catch (error) {

        alert("Unable to copy result.");

    }

}