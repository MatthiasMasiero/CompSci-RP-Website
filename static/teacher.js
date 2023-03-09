$.get("data.csv", function(data) {
    // parse the data from data.csv into the html table
    var htmlTable = document.getElementById("table");
    var dataRows = data.split("\n");
    // console.log(dataRows);
    var initialRows = htmlTable.rows.length;
    for (var i = 0; i < dataRows.length; i++) {
        var newRow = htmlTable.insertRow(i + initialRows);
        var insertRow = dataRows[i].split(",");
        for (var j = 0; j < insertRow.length; j++) {
            var newCell = newRow.insertCell(j);
            newCell.innerHTML = insertRow[j];
            if (j == 2) newCell.contentEditable = true;
        }
        var buttons = newRow.insertCell(3);
        buttons.innerHTML = "<button id='add' contenteditable='false' onclick='btnAction()''>Add</button><button id='subtract' contenteditable='false' onclick='btnAction()''>Subtract</button>";
    }
});

function btnAction() {
    var button = event.target;
    var row = button.parentNode.parentNode;
    var cell = row.cells[2];
    var value = parseInt(cell.innerHTML);
    if (button.id == "add") {
        cell.innerHTML = value + 1;
    } else if (button.id == "subtract") {
        cell.innerHTML = value - 1;
    }
}