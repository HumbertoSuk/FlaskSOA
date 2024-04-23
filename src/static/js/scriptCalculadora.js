        // Agregamos JavaScript para mostrar/ocultar la calculadora
        const calculatorButton = document.getElementById("toggle-calculator");
        const calculatorContainer = document.querySelector(".calculator-container");

        let calculatorVisible = false;

        calculatorButton.addEventListener("click", () => {
            calculatorVisible = !calculatorVisible;
            calculatorContainer.style.display = calculatorVisible ? "block" : "none";
        });

       

        const display = document.getElementById("display");
    const buttons = document.querySelectorAll(".calculator button");
    const operatorDisplay = document.querySelector(".operator-display");

    let currentInput = "";
    let currentOperator = "";
    let shouldClearDisplay = false;

    buttons.forEach((button) => {
        button.addEventListener("click", () => {
            const buttonText = button.textContent;

            if (buttonText.match(/[0-9]/)) {
                if (shouldClearDisplay) {
                    display.value = "";
                    shouldClearDisplay = false;
                }
                display.value += buttonText;
            } else if (buttonText === ".") {
                // Verificar si el punto decimal ya está en el número
                if (!display.value.includes(".") && display.value !== "") {
                    display.value += buttonText;
                }
            } else if (buttonText === "C") {
                display.value = "";
                currentInput = "";
                currentOperator = "";
                updateOperatorDisplay("");
            } else if (buttonText === "=") {
                if (currentOperator && currentInput) {
                    const result = calculate(parseFloat(currentInput), currentOperator, parseFloat(display.value));
                    display.value = result;
                    currentInput = result;
                    currentOperator = "";
                    shouldClearDisplay = true;
                    updateOperatorDisplay("");
                }
            } else {
                currentOperator = buttonText;
                currentInput = display.value;
                shouldClearDisplay = true;
                updateOperatorDisplay(currentOperator);
            }
        });
    });

    function calculate(num1, operator, num2) {
        switch (operator) {
            case "+":
                return num1 + num2;
            case "-":
                return num1 - num2;
            case "*":
                return num1 * num2;
            case "/":
                if (num2 !== 0) {
                    return num1 / num2;
                } else {
                    return "Error: División por cero";
                }
            default:
                return num2;
        }
    }

    function updateOperatorDisplay(operator) {
        operatorDisplay.textContent = operator;
    }