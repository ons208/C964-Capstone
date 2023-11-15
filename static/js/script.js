// script.js

// updateAccuracyMetrics retrieve the data from backend and generate the data onto the frontend
function updateAccuracyMetrics() {
    // Fetch accuracy metrics from the /accuracy_metrics
    fetch('/accuracy_metrics')
        .then(response => response.json())
        .then(data => {
            // Update HTML elements with accuracy metrics
            document.getElementById('mae').textContent = data.mae;
            document.getElementById('mse').textContent = data.mse;
            document.getElementById('rmse').textContent = data.rmse;
            document.getElementById('mean_rmse').textContent = data.mean_rmse
            document.getElementById('r_squared').textContent = data.r_squared;
            document.getElementById('adjusted_r_squared').textContent = data.adjusted_r_squared;
        })
        .catch(error => console.error('Error fetching accuracy metrics:', error));
}

// Call updateAccuracyMetrics to update metrics when the page loads
window.onload = updateAccuracyMetrics;

// Track if the form has been submitted
let formSubmitted = false;

// event listener for form submission
document.querySelector('form').addEventListener('submit', function (event) {
    // Check if the form has not been submitted
    if (!formSubmitted) {
        event.preventDefault(); // Prevent the form from submitting

        // Display a "Calculating..." message to show users the application is working
        const calculating = document.querySelector('.calculating');
        calculating.textContent = "Calculating..."

        // Get user input
        const Age = parseInt(document.getElementById('age').value, 10);
        const education = document.getElementById('education').value;
        const occupation = document.getElementById('occupation').value;
        const years = parseInt(document.getElementById('years').value, 10);

        // Get the selected metric
        const selectedMetric = document.querySelector('input[name="range"]:checked').value;
        document.getElementById('selected_metric').value = selectedMetric;

        // Perform a POST request to the backend with user input
        fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ Age, education, occupation, years, selected_metric: selectedMetric })
        })
        .then(response => response.json())
        .then(data => {
            // Delay the display of result
            setTimeout(function () {
                calculating.textContent = '';
                const predictedDiv = document.querySelector('.predicted');
                const predictedSalary = predictedDiv.querySelector('h4.result');
                const lowerBound = predictedDiv.querySelector('p.result');
                const upperBound = predictedDiv.querySelector('p.result');

                // Check if the elements before adding the 'show' class
                if (predictedSalary) {
                    predictedSalary.textContent = `Predicted Salary: ${data.predicted_salary}`;
                    predictedSalary.classList.add('show');
                    predictedDiv.classList.add('show');
                }
                if (lowerBound) {
                    lowerBound.classList.add('show');
                }
                if (upperBound) {
                    upperBound.textContent = `Salary Range: between ${data.lower_bound} and ${data.upper_bound}`;
                    upperBound.classList.add('show');
                }
            }, 100); // Adjust the delay time as needed (in milliseconds)

            // Set the formSubmitted variable to true
            formSubmitted = true;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        console.error('Form already submitted');
    }
});

// Another Event listener for the "Predict Salary" button, for resubmitting
const predictButton = document.querySelector('button[type="submit"]');
predictButton.addEventListener('click', function () {
    formSubmitted = false;
});
