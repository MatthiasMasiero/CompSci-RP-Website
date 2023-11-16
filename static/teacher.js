// // from a tutorial (https://youtu.be/qp7PdguA0Vg)
document.addEventListener("DOMContentLoaded", () => {
    // loop through all the column headers
    document.querySelectorAll(".search-input").forEach((inputField) => {
        // fetch all the rows in the table
        const tableRows = inputField
        .closest("table")
        .querySelectorAll("tbody > tr");
        // fetch the current header and all the headers together
        const headerCell = inputField.closest("th");
        const otherHeaderCells = headerCell.closest("tr").children;
        // get the index of the current header cell selected
        const columnIndex = Array.from(otherHeaderCells).indexOf(headerCell);
        // get all the cells in the same column as the current header cell
        const searchableCells = Array.from(tableRows).map(
        (row) => row.querySelectorAll("td")[columnIndex]
        );
        
        // event listener for the input field (runs as you type)
        inputField.addEventListener("input", () => {
            // get the input value (what you're typing in)
            const searchQuery = inputField.value.toLowerCase();
            
            // loop through all the cells in the column
            for (const tableCell of searchableCells) {
                // get the entire row of the current cell
                const row = tableCell.closest("tr");
                // get the value of the current cell
                // const value = tableCell.textContent.toLowerCase().replace(",", "");
                const value = tableCell.children[0].value.toLowerCase();
                
                // if the value of the cell doesn't match the search query, hide the row

                row.style.visibility = null;
                
                if (value.search(searchQuery) === -1) {
                    row.style.visibility = "collapse";
                }
            }
        });
    });



        
    // loop through all the buttons with the class "addbutton"
    document.querySelectorAll(".addbutton").forEach((button) => {
    // add an event listener to each button
    button.addEventListener("click", () => {
        // the button is in a table cell
        // when the button is clicked, increment the value of the 5th cell in the row
        
        // get the value of the 5th cell in the row
        const cell = parseInt(
            button.closest("tr").querySelectorAll("td")[5].querySelector("input")
            .value
            );
            // increment the value of the 5th cell in the row
            button.closest("tr").querySelectorAll("td")[5].querySelector("input").value = cell + 1;
            
        });
    });
    
    // loop through all the buttons with the class "subtractbutton"
    document.querySelectorAll(".subtractbutton").forEach((button) => {
    // add an event listener to each button
    button.addEventListener("click", () => {
        // the button is in a table cell
        // when the button is clicked, decrement the value of the 5th cell in the row
        
        // get the value of the 5th cell in the row
        const cell = parseInt(
            button.closest("tr").querySelectorAll("td")[5].querySelector("input")
            .value
            );
            // increment the value of the 5th cell in the row
            button
            .closest("tr")
            .querySelectorAll("td")[5]
            .querySelector("input").value = cell - 1;
            
        });
    });
});
            