const form = document.getElementById("predictionForm");

const loading = document.getElementById("loading");
const result = document.getElementById("result");
const error = document.getElementById("error");

const predictionText = document.getElementById("predictionText");
const confidenceText = document.getElementById("confidenceText");


form.addEventListener("submit", async function (event) {

    event.preventDefault();

    result.classList.add("hidden");
    error.classList.add("hidden");
    loading.classList.remove("hidden");


    const income = Number(document.getElementById("income").value);
    const age = Number(document.getElementById("age").value);
    const loan = Number(document.getElementById("loan").value);
    const loanToIncome = Number(
        document.getElementById("loanToIncome").value
    );


    const data = {
        Income: income,
        Age: age,
        Loan: loan,
        "Loan to Income": loanToIncome
    };


    try {

        const response = await fetch(
            "http://127.0.0.1:5000/predict",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            }
        );


        if (!response.ok) {
            throw new Error("Server returned an error");
        }


        const resultData = await response.json();


        loading.classList.add("hidden");
        result.classList.remove("hidden");


        if (Number(resultData.prediction) === 1) {
            predictionText.textContent = "⚠️ Likely to Default";
        } else {
            predictionText.textContent = "✅ Unlikely to Default";
        }


        confidenceText.textContent =
            "Confidence: " +
            (Number(resultData.confidence) * 100).toFixed(2) +
            "%";

    }

    catch (err) {

        loading.classList.add("hidden");
        error.classList.remove("hidden");

        error.textContent =
            "Could not connect to the backend. Make sure Flask is running.";

        console.error(err);
    }

});

