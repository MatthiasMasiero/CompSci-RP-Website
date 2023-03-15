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
        const value = tableCell.textContent.toLowerCase().replace(",", "");

        // if the value of the cell doesn't match the search query, hide the row
        row.style.visibility = null;

        if (value.search(searchQuery) === -1) {
          row.style.visibility = "collapse";
        }
      }
    });
  });
});
