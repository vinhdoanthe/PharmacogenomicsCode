$(function () {
    $("#all-legends").draggable({
        containment: "window"
    });
});

//Pass jsonFiles Here
var json_GeneralFile = "json/json_GeneralFile.json";
var json_drugData = "json/json_drugData.json";
var json_proteinData = "json/json_proteinData.json";
var json_interactionData = "json/json_interactionData.json"


let drug_xlsxData;
let protein_xlsxData;
let interaction_xlsxData;
var drugStatusNameForDialog = ""
var selectedDrugName1 = "";

// Function to read the Drugs JSON data file
function readDrugJSON() {
    const jsonFilePath = json_drugData;
    fetch(jsonFilePath)
        .then((response) => response.json())
        .then((jsonData) => {
            // Assuming your JSON data is an array of objects, adjust this code accordingly
            drug_xlsxData = jsonData;


            // Now that the JSON data is loaded, you can convert it into a format similar
            // to what you were getting from the XLSX file (if needed)
            // For now, let's log it to the console as an example:
            // console.log(drug_jsonData);
            readProteinJSON();
        })
        .catch((error) => {
            console.error("Error reading the JSON file:", error);
        });
}

function readProteinJSON() {
    const jsonFilePath = json_proteinData;

    fetch(jsonFilePath)
        .then((response) => response.json())
        .then((jsonData) => {
            protein_xlsxData = jsonData;

            readInteractionJSON();
        })
        .catch((error) => {
            console.error("Error reading the file:", error);
        });
}


function readInteractionJSON() {
    const jsonFilePath = json_interactionData;

    fetch(jsonFilePath)
        .then((response) => response.json())
        .then((jsonData) => {
            interaction_xlsxData = jsonData;
            processData();
            //console.log(interaction_xlsxData)
        })
        .catch((error) => {
            console.error("Error reading the file:", error);
        });
}


window.onload = function () {
    readDrugJSON();
};

var exportButton = document.getElementById('exportButton');
exportButton.addEventListener('click', function () {
    showExportOptions();
});

window.addEventListener('click', function (event) {
    var modal = document.getElementById('exportModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
});

function showExportOptions() {
    // Check if the modal already exists
    var modal = document.getElementById('exportModal');
    if (modal) {
        // If it exists, toggle the modal display and return
        modal.style.display = modal.style.display === 'none' ? 'block' : 'none';
        return;
    }

    // Create the modal container
    modal = document.createElement('div');
    modal.id = 'exportModal';
    modal.className = 'modal';

    var content = document.createElement('div');
    content.className = 'modal-content';
    modal.appendChild(content);

    // ... (rest of the function)

    // Add a close button
    var closeBtn = document.createElement('button');
    closeBtn.innerHTML = '&times;';
    closeBtn.className = 'modal-close';
    closeBtn.addEventListener('click', function () {
        modal.style.display = 'none';
    });
    content.appendChild(closeBtn);

    var title = document.createElement('h2');
    title.textContent = "Export Chart As";
    title.className = 'modal-title';
    title.style.marginTop = '20';
    content.appendChild(title);

    // Append the export options to the modal content
    // content.appendChild(createExportOption('View In Full Screen'));
    // content.appendChild(createExportOption('Print Chart'));
    content.appendChild(createExportOption('Download PNG'));
    content.appendChild(createExportOption('Download JPEG'));
    // content.appendChild(createExportOption('Download PDF'));
    // content.appendChild(createExportOption('Download CSV'));
    content.appendChild(createExportOption('Download XLS'));
    // content.appendChild(createExportOption('View Data Table'));

    // Append the modal to the body
    document.body.appendChild(modal);

    // Show the modal
    modal.style.display = 'block';
}

function createExportOption(optionText) {
    var optionButton = document.createElement('button');
    optionButton.textContent = optionText;
    optionButton.className = 'export-option-button'; // add class here
    optionButton.addEventListener('click', function () {
        handleExportOption(optionText);
    });
    return optionButton;
}

function handleExportOption(option) {
    switch (option) {
        case 'View In Full Screen':
            viewFullScreen();
            break;

        case 'Download PNG':
            downloadPNG();
            break;
        case 'Download JPEG':
            downloadJPEG();
            break;

        case 'Download CSV':
            downloadCSV();
            break;
        case 'Download XLS':
            downloadXLS();
            break;
        case 'View Data Table':
            viewDataTable();
            break;
        default:
            break;
    }
}

function getFilteredSvgContent(svgElement) {
    // Clone the original SVG to avoid altering it
    var clonedSvg = svgElement.cloneNode(true);
    var d3ClonedSvg = d3.select(clonedSvg);

    // Remove hidden links first
    d3ClonedSvg.selectAll(".link")
        .filter(function () {
            return this.style.visibility === 'hidden' || this.style.display === 'none';
        })
        .remove();

    // Remove hidden parent nodes
    d3ClonedSvg.selectAll(".node-parent")
        .filter(function () {
            return this.style.visibility === 'hidden' || this.style.display === 'none';
        })
        .remove();

    // Remove hidden child nodes. This checks if both the circle and text children are hidden.
    d3ClonedSvg.selectAll(".node:not(.node-parent)")
        .filter(function () {
            var circleVisibility = d3.select(this).select('circle').style('visibility');
            var textVisibility = d3.select(this).select('text').style('visibility');
            return circleVisibility === 'hidden' && textVisibility === 'hidden';
        })
        .remove();

    return new XMLSerializer().serializeToString(clonedSvg);
}

//Export buttons place
function viewFullScreen() {
    var chartDiv = document.getElementById('chart');
    chartDiv.style.backgroundColor = 'white'; // Set background color to white
    chartDiv.requestFullscreen();
}

// Print Chart
function printChart() {
    window.print();
}

// Download PNG
// Download PNG
// Download PNG
function downloadPNG() {
    var svgElement = document.querySelector("#chart svg");
    var svgData = getFilteredSvgContent(svgElement);
    svgData = addWhiteBackground(svgData);

    // First convert the SVG to canvas
    svgToCanvas(svgData, function (chartCanvas) {
        // Convert the HTML legends to canvas
        html2canvas(document.querySelector("#all-legends")).then(function (legendCanvas) {
            // Calculate the scale factor to match the height of the chart
            var scaleFactor = chartCanvas.height / legendCanvas.height;

            // Adjust the final canvas width to consider the scaled width of the legends
            var finalCanvas = document.createElement("canvas");
            finalCanvas.width = chartCanvas.width + (legendCanvas.width * scaleFactor); // sum of the chart width and the scaled legend width
            finalCanvas.height = chartCanvas.height; // using chart's height

            var context = finalCanvas.getContext("2d");
            context.drawImage(chartCanvas, 0, 0);
            context.drawImage(legendCanvas, chartCanvas.width, 0, legendCanvas.width * scaleFactor, chartCanvas.height);

            // Now you can save the combined canvas as PNG
            var a = document.createElement("a");
            a.href = finalCanvas.toDataURL("image/png");
            a.download = "chart.png";
            a.click();
        });
    });
}

function svgToCanvas(svgData, callback) {
    var canvas = document.createElement("canvas");
    var context = canvas.getContext("2d");
    var image = new Image();

    // Load all images before rendering SVG onto canvas
    var images = document.querySelector("#chart svg").querySelectorAll("image");
    var loadedCount = 0;

    images.forEach(function (img) {
        var xlinkHref = img.getAttribute("href");
        var imgObj = new Image();
        imgObj.onload = function () {
            loadedCount++;
            if (loadedCount === images.length) {
                renderCanvas();
            }
        };

        if (xlinkHref) {
            imgObj.src = "https://entertainmentbuz.com/visual/d3/" + xlinkHref;
        } else {
            loadedCount++;
        }
    });

    function renderCanvas() {
        var scale = 2;
        var width = document.querySelector("#chart svg").clientWidth * scale;
        var height = document.querySelector("#chart svg").clientHeight * scale;

        context.clearRect(0, 0, canvas.width, canvas.height);
        canvas.width = width;
        canvas.height = height;
        context.fillStyle = "white";
        context.fillRect(0, 0, canvas.width, canvas.height);
        context.fillStyle = "black";

        canvg(canvas, svgData, {
            ignoreMouse: true,
            ignoreAnimation: true,
            ignoreDimensions: true,
            scaleWidth: width,
            scaleHeight: height,
            renderCallback: function () {
                callback(canvas);
            }
        });
    }
}

// Download JPEG
function downloadJPEG() {
    var svgElement = document.querySelector("#chart svg");
    var svgData = getFilteredSvgContent(svgElement);
    svgData = addWhiteBackground(svgData);

    // First convert the SVG to canvas
    svgToCanvas(svgData, function (chartCanvas) {
        // Convert the HTML legends to canvas
        html2canvas(document.querySelector("#all-legends")).then(function (legendCanvas) {
            // Calculate the scale factor to match the height of the chart
            var scaleFactor = chartCanvas.height / legendCanvas.height;

            // Adjust the final canvas width to consider the scaled width of the legends
            var finalCanvas = document.createElement("canvas");
            finalCanvas.width = chartCanvas.width + (legendCanvas.width * scaleFactor);
            finalCanvas.height = chartCanvas.height;

            var context = finalCanvas.getContext("2d");
            context.drawImage(chartCanvas, 0, 0);
            context.drawImage(legendCanvas, chartCanvas.width, 0, legendCanvas.width * scaleFactor, chartCanvas.height);

            // Now you can save the combined canvas as JPEG
            var a = document.createElement("a");
            a.href = finalCanvas.toDataURL("image/jpeg", 0.9);  // 0.9 is the quality factor (0 to 1)
            a.download = "chart.jpeg";
            a.click();
        });
    });
}

// Helper function to add a white background rectangle to the SVG
function addWhiteBackground(svgData) {
    var parser = new DOMParser();
    var doc = parser.parseFromString(svgData, "image/svg+xml");
    var svg = doc.documentElement;

    var backgroundRect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    backgroundRect.setAttribute("width", "100%");
    backgroundRect.setAttribute("height", "100%");
    backgroundRect.setAttribute("fill", "white");

    svg.insertBefore(backgroundRect, svg.firstChild);

    return new XMLSerializer().serializeToString(doc);
}

// Download PDF
function downloadPDF() {
    var svgElement = document.querySelector("#chart svg");
    var svgData = new XMLSerializer().serializeToString(svgElement);

    var canvas = document.createElement("canvas");
    var context = canvas.getContext("2d");
    var image = new Image();

    // Load all images before rendering SVG onto canvas
    var images = svgElement.querySelectorAll("image");
    var loadedCount = 0;

    images.forEach(function (img) {
        var xlinkHref = img.getAttribute("href");
        var imgObj = new Image();
        imgObj.onload = function () {
            loadedCount++;
            if (loadedCount === images.length) {
                renderCanvas();
            }
        };

        // Use the href attribute for the image path
        if (xlinkHref) {
            imgObj.src = "https://entertainmentbuz.com/visual/d3/" + xlinkHref;
        } else {
            loadedCount++;
        }
    });

    function renderCanvas() {
        context.clearRect(0, 0, canvas.width, canvas.height);
        canvas.width = svgElement.clientWidth;
        canvas.height = svgElement.clientHeight;
        context.fillStyle = "white"; // Set background color to white
        context.fillRect(0, 0, canvas.width, canvas.height); // Fill with white color

        // Render SVG onto canvas
        canvg(canvas, svgData, {
            ignoreMouse: true,
            ignoreAnimation: true,
            ignoreDimensions: true,
            scaleWidth: canvas.width,
            scaleHeight: canvas.height,
            renderCallback: function () {
                // Convert canvas to image data URL
                var imageData = canvas.toDataURL("image/jpeg");

                // Create a temporary link element to trigger download
                var a = document.createElement("a");
                a.href = imageData;
                a.download = "chart.jpeg";
                a.click();
            }
        });
    }
}

// Download CSV
function downloadCSV() {
    var csvContent = "data:text/csv;charset=utf-8,";
    csvContent += "Source,Target,Type\r\n";

    links.forEach(function (link) {
        var source = link.source.id;
        var target = link.target.id;
        var type = link.type;
        csvContent += source + "," + target + "," + type + "\r\n";
    });

    var encodedURI = encodeURI(csvContent);
    var a = document.createElement("a");
    a.href = encodedURI;
    a.download = "chart.csv";
    a.click();
}

function getFilteredLinksXLSX() {
    var filteredLinks = [];

    // Check the SVG for visible links
    d3.selectAll(".link")
        .filter(function () {
            return this.style.visibility !== 'hidden' && this.style.display !== 'none';
        })
        .each(function (d) {
            filteredLinks.push(d);
        });

    return filteredLinks;
}

// Download XLS
function downloadXLS() {
    var filteredLinks = getFilteredLinksXLSX();
    //console.log(filteredLinks)
    // Load the XLSX
    var req = new XMLHttpRequest();
    req.open("GET", "data_export_file.xlsx", true);
    req.responseType = "arraybuffer";

    req.onload = function (e) {
        var data = new Uint8Array(req.response);
        var workbook = XLSX.read(data, { type: "array" });

        var firstSheetName = workbook.SheetNames[0];
        var worksheet = workbook.Sheets[firstSheetName];
        var rows = XLSX.utils.sheet_to_json(worksheet);
        console.log(rows);
        // Filter the rows based on the filtered links
        var filteredRows = rows.filter(row =>
            filteredLinks.some(link =>
                link.source.id === row.drug_name &&
                link.source.Drug_type === row.drugtype &&
                link.target.id === row.protein &&
                link.target.Protein_Class === row.Protein_Class
            )
        );

        // Create a new worksheet with the filtered rows
        console.log(filteredRows)
        var newWs = XLSX.utils.json_to_sheet(filteredRows);
        var newWb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(newWb, newWs, firstSheetName);

        // Download the new XLSX file
        XLSX.writeFile(newWb, "filtered_data.xlsx");
    };

    req.send();
}

function downloadXLS11() {
    var workbook = XLSX.utils.book_new();
    var worksheet = XLSX.utils.json_to_sheet(links);
    XLSX.utils.book_append_sheet(workbook, worksheet, "Chart Data");

    var wbout = XLSX.write(workbook, { type: "binary", bookType: "xlsx" });
    function s2ab(s) {
        var buf = new ArrayBuffer(s.length);
        var view = new Uint8Array(buf);
        for (var i = 0; i < s.length; i++) view[i] = s.charCodeAt(i) & 0xff;
        return buf;
    }

    var blob = new Blob([s2ab(wbout)], { type: "application/octet-stream" });
    var url = URL.createObjectURL(blob);

    var a = document.createElement("a");
    a.href = url;
    a.download = "chart.xlsx";
    a.click();
}

// View Data Table
function viewDataTable() {
    var tableData = [];
    tableData.push(["Source", "Target", "Type"]);
    links.forEach(function (link) {
        var source = link.source.id;
        var target = link.target.id;
        var type = link.type;
        tableData.push([source, target, type]);
    });

    var table = document.createElement("table");
    var tableHeader = document.createElement("thead");
    var tableBody = document.createElement("tbody");

    tableData.forEach(function (rowData, rowIndex) {
        var row = document.createElement("tr");
        rowData.forEach(function (cellData, cellIndex) {
            var cellElement = rowIndex === 0 ? document.createElement("th") : document.createElement("td");
            cellElement.textContent = cellData;
            row.appendChild(cellElement);
        });
        rowIndex === 0 ? tableHeader.appendChild(row) : tableBody.appendChild(row);
    });

    table.appendChild(tableHeader);
    table.appendChild(tableBody);

    var tableContainer = document.createElement("div");
    tableContainer.appendChild(table);

    var overlay = document.createElement("div");
    overlay.className = "overlay";
    overlay.appendChild(tableContainer);

    document.body.appendChild(overlay);
}

// Drug dialog code place here
function showDialog(title, parentNodeName) {
    var dialog = document.getElementById("dialog");
    var drugName = document.getElementById("drug-name");
    var closeButton = document.getElementById("close-button");
    var oldTabs = document.getElementsByClassName("nav-link");
    var overlay = document.getElementById('overlay');
    selectedDrugName1 = title;


    // Clone tabs and replace old ones to remove previous event listeners
    for (var i = 0; i < oldTabs.length; i++) {
        var newTab = oldTabs[i].cloneNode(true);
        oldTabs[i].parentNode.replaceChild(newTab, oldTabs[i]);
    }

    var tabs = document.getElementsByClassName("nav-link");

    drugName.textContent = parentNodeName;
    dialog.style.display = "block";
    overlay.style.display = "block";

    closeButton.addEventListener("click", function () {
        dialog.style.display = "none";
        overlay.style.display = "none"; // hide the overlay when the dialog is closed
    });

    // Add event listeners to the tabs
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].addEventListener("click", handleTabClick);
    }

    // Set the first tab as active by default
    tabs[0].classList.add("active");

    // Call the corresponding function for the active tab
    var activeTab = tabs[0].getAttribute("data-tab");
    if (activeTab === "drug-image") {
        showDrugImageTab(selectedDrugName1);
    } else if (activeTab === "drug-description") {
        showDrugDescription(selectedDrugName1);
    } else if (activeTab === "drug-structure") {
        showDrugStructureTab(selectedDrugName1)
    }
    /*
    else if (activeTab === "drug-a") {
      showDrugATab();
    } else if (activeTab === "drug-b") {
      showDrugBTab();
    }
    */

    // Function to handle tab click event
    function handleTabClick(event) {
        // Remove the active class from all tabs
        for (var i = 0; i < tabs.length; i++) {
            tabs[i].classList.remove("active");
        }

        // Add the active class to the clicked tab
        event.target.classList.add("active");
        // showDrugDescription
        // Call the corresponding function based on the tab clicked
        var tabName = event.target.getAttribute("data-tab");
        if (tabName === "drug-image") {
            showDrugImageTab(selectedDrugName1);
        } else if (tabName === "drug-description") {
            showDrugDescription(selectedDrugName1);
        } else if (tabName === "drug-structure") {
            showDrugStructureTab(selectedDrugName1)
        }
        /*
        else if (tabName === "drug-a") {
          showDrugATab();
        } else if (tabName === "drug-b") {
          showDrugBTab();
        }
        */
    }

    // Function to showdrug image
    function showDrugImageTab(drugNameValue) {
        var tabContent = document.querySelector(".tab-content");
        tabContent.innerHTML = ""; // Clear previous content

        // Your code to fetch the row where column name "name" = drugNameValue
        // Assuming you have the data in the global variable 'drug_xlsxData'
        var matchingRow = drug_xlsxData.find((row) => row.name === drugNameValue);

        if (matchingRow) {
            var drugbank_id = matchingRow.drugbank_id;

            // Create an img element
            var image = document.createElement("img");

            // Check if the image exists
            image.onerror = function () {
                // If the image does not exist, set the default image path
                image.src = "images/drug_images/imagenotfound.png";
                // Add the CSS classes to center the image and set the maximum height
                image.classList.add("center-image", "first-tab-image");
                // Append the image to the tabContent
                tabContent.appendChild(image);
            };

            // Set the src attribute to the drug image path
            image.src = "images/drug_images/" + drugbank_id + ".png";
            // Add the CSS classes to center the image and set the maximum height
            image.classList.add("center-image", "first-tab-image");
            // Append the image to the tabContent
            tabContent.appendChild(image);
        } else {
            // If the drugNameValue is not found in the data, display a default image
            var defaultImage = document.createElement("img");
            defaultImage.src = "images/drug_images/imagenotfound.png";
            defaultImage.classList.add("center-image", "first-tab-image");
            tabContent.appendChild(defaultImage);
        }
    }

    function showDrugDescription(selectedDrugName1) {
        var tabContent = document.querySelector(".tab-content");
        tabContent.innerHTML = ""; // Clear the existing content

        // Your code to fetch the row where column name "name" matches selectedDrugName1
        // Assuming you have the data in the global variable 'drug_xlsxData'
        var matchingRow = drug_xlsxData.find((row) => row.name === selectedDrugName1);

        if (matchingRow) {
            // Create a table to display the drug information
            var drugInfoTable = document.createElement("div");
            drugInfoTable.classList.add("drug-info-table");
            getDrugStatusName(selectedDrugName1)
            // Create table rows and cells for each field
            var fields = [
                { label: "Drug ID", key: "drugbank_id" },
                { label: "Drug Name", key: "name" },
                { label: "Drug Type", key: "drugtype", isConvert: true },
                { label: "Drug Approval Status", key: "Drug_status", valueForDialog: drugStatusNameForDialog }, // Add Drug_status field with value for dialog
                { label: "Description", key: "description" }, // Move Description to the end
                // Add more fields as needed
            ];

            fields.forEach((field) => {
                var row = document.createElement("div");
                row.classList.add("drug-info-row");

                var labelCell = document.createElement("div");
                labelCell.classList.add("drug-info-cell", "label");
                labelCell.textContent = field.label;
                row.appendChild(labelCell);

                var valueCell = document.createElement("div");
                valueCell.classList.add("drug-info-cell");
                if (field.key === "drugbank_id") {
                    var drugbankIdValue = matchingRow[field.key];
                    var drugbankIdLink = "https://go.drugbank.com/drugs/" + drugbankIdValue;

                    // Create a new anchor element and set its attributes
                    var anchorTag = document.createElement("a");
                    anchorTag.href = drugbankIdLink;
                    anchorTag.target = "_blank";

                    // Set the anchor's innerHTML to include the drug ID and the clickable link
                    anchorTag.innerHTML = drugbankIdValue;

                    // Set the valueCell's innerHTML to the anchor tag
                    valueCell.innerHTML = anchorTag.outerHTML;
                }
                else if (field.valueForDialog !== undefined) {
                    valueCell.textContent = field.valueForDialog;
                } else if (field.isConvert) {
                    valueCell.textContent = convertDrugType(matchingRow[field.key]);
                } else {
                    valueCell.textContent = matchingRow[field.key];
                }

                row.appendChild(valueCell);
                drugInfoTable.appendChild(row);
            });

            // Append the table to the tabContent
            tabContent.appendChild(drugInfoTable);
        } else {
            // If the selectedDrugName1 is not found in the data, display a default message
            var errorMessage = document.createElement("p");
            errorMessage.textContent = "Drug information not found for " + selectedDrugName1;
            tabContent.appendChild(errorMessage);
        }
    }

    function getDrugStatusName(selectedDrugName1) {
        d3.selectAll(".node-parent")
            .filter(function (node) {
                if (node.isParent) {
                    if (node.id === selectedDrugName1) {
                        //console.log(node.Drug_status)
                        drugStatusNameForDialog = node.Drug_status
                        console.log(drugStatusNameForDialog)
                    }
                }
                //console.log(node.Drug_status)

            })
    }
    // Function to convert drugtype reference number into meaningful labels
    function convertDrugType(drugType) {
        console.log("aajaj= " + drugType)
        if (drugType === 0) {
            return "Biologic";
        } else if (drugType === 1) {
            return "Small Molecule";
        } else {
            return "Unknown";
        }
    }

    function showDrugStructureTab(selectedDrugName1) {
        var tabContent = document.querySelector('.tab-content');
        tabContent.innerHTML = ''; // Clear the existing content

        // Your code to fetch the row where column name "name" matches selectedDrugName1
        // Assuming you have the data in the global variable 'drug_xlsxData'
        var matchingRow = drug_xlsxData.find((row) => row.name === selectedDrugName1);

        if (matchingRow) {
            // Create a table to display the drug structure information
            var drugStructureTable = document.createElement('div');
            drugStructureTable.classList.add('drug-info-table');

            // Fields to add to the table
            var fields = [
                { label: 'Indication', key: 'indication' },
                { label: 'Aliases', key: 'aliases', isConvert: true }, // Add isConvert property for "aliases" field
                { label: 'Absorption', key: 'absorption' },
                { label: 'Pharmacodynamics', key: 'pharmacodynamics' },
                { label: 'Mechanism of Action (MOA)', key: 'moa' },
                { label: 'Toxicity', key: 'toxicity' },
                { label: 'Half-life', key: 'half_life' },
                { label: 'Distribution Volume', key: 'distribution_volume' },
                { label: 'Protein Binding', key: 'protein_binding' },
                { label: 'Dosages', key: 'dosages' },
                { label: 'Properties', key: 'properties' },
                // Add more fields as needed
            ];

            fields.forEach((field) => {
                var row = document.createElement('div');
                row.classList.add('drug-info-row');

                var labelCell = document.createElement('div');
                labelCell.classList.add('drug-info-cell', 'label');
                labelCell.textContent = field.label;
                row.appendChild(labelCell);

                var valueCell = document.createElement('div');
                valueCell.classList.add('drug-info-cell');
                if (field.isConvert && matchingRow[field.key]) {
                    valueCell.appendChild(createAliasList(matchingRow[field.key]));
                } else if (field.key === 'dosages') {
                    var dosageRegex = /\('([^']*)', '([^']*)'\)/g;
                    var matches, dosages = [];
                    while (matches = dosageRegex.exec(matchingRow[field.key])) {
                        if (matches[1].trim() && matches[2].trim()) {
                            dosages.push(`<li><b>${matches[2].replace(';', ',')}</b>: ${matches[1]}</li>`); // Replace semicolon with comma
                        }
                    }
                    valueCell.innerHTML = `<ul>${dosages.join('')}</ul>`;
                } else if (field.key === 'properties') {
                    var propertiesRegex = /\('([^']*)', '([^']*)'\)/g;
                    var matches, properties = [];
                    while (matches = propertiesRegex.exec(matchingRow[field.key])) {
                        if (matches[1].trim() && matches[2].trim()) {
                            properties.push(`<li><b>${matches[1]}</b>: ${matches[2]}</li>`); // Add <b> tag and replace comma with colon
                        }
                    }
                    valueCell.innerHTML = `<ul>${properties.join('')}</ul>`;
                }
                else {
                    valueCell.textContent = matchingRow[field.key];
                }
                row.appendChild(valueCell);

                drugStructureTable.appendChild(row);
            });

            // Append the table to the tabContent
            tabContent.appendChild(drugStructureTable);
        } else {
            // If the selectedDrugName1 is not found in the data, display a default message
            var errorMessage = document.createElement('p');
            errorMessage.textContent = 'Drug structure information not found for ' + selectedDrugName1;
            tabContent.appendChild(errorMessage);
        }
    }

    // Function to create a bulleted list from the aliases separated by "|"
    function createAliasList11(aliases) {
        var aliasList = document.createElement('ul');
        aliasList.classList.add('alias-list');
        var aliasItems = aliases.split('|');
        aliasItems.forEach((alias) => {
            var listItem = document.createElement('li');
            listItem.classList.add('alias-list-item');
            listItem.textContent = alias;
            aliasList.appendChild(listItem);
        });
        return aliasList;
    }
    // Function to create a string from the aliases separated by "|"
    function createAliasList(aliases) {
        var aliasItems = aliases.split('|').filter(item => item.trim() !== ''); // Filter out empty strings
        var aliasString = aliasItems.join(', '); // join the items into a string, separated by commas

        var aliasList = document.createElement('p');
        aliasList.textContent = aliasString;

        return aliasList;
    }

    // Function to show drug A
    function showDrugATab() {
        var tabContent = document.querySelector(".tab-content");
        tabContent.textContent = "This is the drug A tab content.";
    }

    // Function to show drug B
    function showDrugBTab() {
        var tabContent = document.querySelector(".tab-content");
        tabContent.textContent = "This is the drug B tab content.";
    }
}

/////Protein Show Dialog

function showDialog_Child(title, childName) {
    var dialog = document.getElementById("dialog1");
    var drugName = document.getElementById("drug-name1");
    var closeButton = document.getElementById("close-button1");
    var oldTabs = document.getElementsByClassName("nav-link1");
    var overlay = document.getElementById('overlay');
    selectedProteinName1 = title;

    // Clone tabs and replace old ones to remove previous event listeners
    for (var i = 0; i < oldTabs.length; i++) {
        var newTab = oldTabs[i].cloneNode(true);
        oldTabs[i].parentNode.replaceChild(newTab, oldTabs[i]);
    }

    var tabs = document.getElementsByClassName("nav-link1");

    drugName.textContent = childName;
    dialog.style.display = "block";
    overlay.style.display = "block";

    closeButton.addEventListener("click", function () {
        dialog.style.display = "none";
        overlay.style.display = "none"; // hide the overlay when the dialog is closed
    });

    // Add event listeners to the tabs
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].addEventListener("click", handleTabClick);
    }

    // Set the first tab as active by default
    tabs[0].classList.add("active");

    // Call the corresponding function for the active tab
    var activeTab = tabs[0].getAttribute("protein-tab");
    if (activeTab === "protein-image") {
        showProteinImageTab();
    } else if (activeTab === "protein-structure") {
        console.log("protein:  " + selectedProteinName1)
        showProteinStructureTab(selectedProteinName1);
    }
    showProteinImageTab();
    // Function to handle tab click event
    function handleTabClick(event) {
        // Remove the active class from all tabs
        for (var i = 0; i < tabs.length; i++) {
            tabs[i].classList.remove("active");
        }

        // Add the active class to the clicked tab
        event.target.classList.add("active");

        // Call the corresponding function based on the tab clicked
        var tabName = event.target.getAttribute("data-tab");
        if (tabName === "protein-image") {
            showProteinImageTab();
        } else if (tabName === "protein-structure") {
            console.log("protein:  " + selectedProteinName1)
            showProteinStructureTab(selectedProteinName1);
        }
    }

    // Function to showdrug image
    // Function to show drug image
    function showProteinImageTab22() {
        var tabContent = document.querySelector(".tab-content1");
        tabContent.innerHTML = ""; // Clear previous content

        // Create an img element
        var image = document.createElement("img");
        image.src = "images/drug_images/" + "Goserelin.png"
        image.classList.add("center-image", "first-tab-image"); // Add CSS classes

        // Append the image to the tabContent
        tabContent.appendChild(image);
    }

    function showProteinImageTab() {
        drugNameValue = selectedProteinName1
        var tabContent = document.querySelector(".tab-content1");
        tabContent.innerHTML = ""; // Clear previous content

        // Your code to fetch the row where column name "name" = drugNameValue
        // Assuming you have the data in the global variable 'drug_xlsxData'
        var matchingRow = protein_xlsxData.find((row) => row.uniprot_ID === drugNameValue);
        console.log(matchingRow)
        if (matchingRow) {
            var drugbank_id = matchingRow.uniprot_ID;

            // Create an img element
            var image = document.createElement("img");

            // Check if the image exists
            image.onerror = function () {
                // If the image does not exist, set the default image path
                image.src = "images/protein_images/imagenotfound.png";
                // Add the CSS classes to center the image and set the maximum height
                image.classList.add("center-image", "first-tab-image");
                // Append the image to the tabContent
                tabContent.appendChild(image);
            };

            // Set the src attribute to the drug image path
            image.src = "images/protein_images/" + drugbank_id + ".png";
            // Add the CSS classes to center the image and set the maximum height
            image.classList.add("center-image", "first-tab-image");
            // Append the image to the tabContent
            tabContent.appendChild(image);
        } else {
            // If the drugNameValue is not found in the data, display a default image
            var defaultImage = document.createElement("img");
            defaultImage.src = "images/protein_images/imagenotfound.png";
            defaultImage.classList.add("center-image", "first-tab-image");
            tabContent.appendChild(defaultImage);
        }
    }

    function showProteinStructureTab(proteinName11111) {
        console.log("dd: " + proteinName11111);
        var tabContent = document.querySelector('.tab-content1');
        tabContent.innerHTML = ''; // Clear the existing content

        // Your code to fetch the row where column name "name" matches selectedDrugName1
        // Assuming you have the data in the global variable 'protein_xlsxData'
        var matchingRow = protein_xlsxData.find((row) => row.uniprot_ID === proteinName11111);
        console.log(matchingRow);
        if (matchingRow) {
            // Create a table to display the protein structure information
            var proteinStructureTable = document.createElement('div');
            proteinStructureTable.classList.add('protein-info-table');

            // Fields to add to the table
            var fields = [
                { label: 'Uniprot ID', key: 'uniprot_ID' },
                { label: 'Gene Name', key: 'genename' },
                { label: 'Gene ID', key: 'geneID' },
                { label: 'Entry Name', key: 'entry_name' },
                { label: 'Protein Name', key: 'protein_name' },
                { label: 'Protein Class', key: 'Protein_class' },
                // Add more fields as needed
            ];

            fields.forEach((field) => {
                var row = document.createElement('div');
                row.classList.add('protein-info-row');

                var labelCell = document.createElement('div');
                labelCell.classList.add('protein-info-cell', 'label');
                labelCell.textContent = field.label;
                row.appendChild(labelCell);

                var valueCell = document.createElement('div');
                valueCell.classList.add('protein-info-cell');

                // Modify the "Uniprot ID" field to include the link
                if (field.key === 'uniprot_ID' || field.key === 'geneID') {
                    var hyperlink = document.createElement('a');
                    var matchingValue = matchingRow[field.key];

                    if (field.key === 'uniprot_ID') {
                        hyperlink.href = 'https://www.uniprot.org/uniprot/' + matchingValue;
                    } else {
                        hyperlink.href = 'https://www.ensembl.org/Homo_sapiens/Gene/Summary?db=core;g=' + matchingValue;
                    }

                    hyperlink.target = '_blank'; // Open link in new tab
                    hyperlink.textContent = '';

                    // Create a new anchor element for the matching value
                    var valueAnchor = document.createElement('a');
                    valueAnchor.href = hyperlink.href;
                    valueAnchor.target = hyperlink.target;
                    valueAnchor.textContent = matchingValue;

                    // Clear the existing content of valueCell and append both anchor tags
                    valueCell.innerHTML = '';
                    valueCell.appendChild(valueAnchor);
                    valueCell.appendChild(document.createTextNode(' '));
                    valueCell.appendChild(hyperlink);
                }
                else {
                    valueCell.textContent = matchingRow[field.key];
                }

                row.appendChild(valueCell);
                proteinStructureTable.appendChild(row);
            });

            // Append the table to the tabContent
            tabContent.appendChild(proteinStructureTable);
        } else {
            // If the selectedDrugName1 is not found in the data, display a default message
            var errorMessage = document.createElement('p');
            errorMessage.textContent = 'Protein structure information not found for ' + proteinName11111;
            tabContent.appendChild(errorMessage);
        }
    }

}

//Interaction Dialog
function showDialog_Links(title, interactionTy) {
    console.log("title: " + title)
    var dialog = document.getElementById("dialog2");
    var drugName = document.getElementById("drug-name2");
    var closeButton = document.getElementById("close-button2");
    var oldTabs = document.getElementsByClassName("nav-link2");
    var overlay = document.getElementById('overlay');
    selectedInteractionName1 = title;

    // Clone tabs and replace old ones to remove previous event listeners
    for (var i = 0; i < oldTabs.length; i++) {
        var newTab = oldTabs[i].cloneNode(true);
        oldTabs[i].parentNode.replaceChild(newTab, oldTabs[i]);
    }

    var tabs = document.getElementsByClassName("nav-link2");

    drugName.textContent = title;
    dialog.style.display = "block";
    overlay.style.display = "block"; // show the overlay when the dialog is shown

    closeButton.addEventListener("click", function () {
        dialog.style.display = "none";
        overlay.style.display = "none"; // hide the overlay when the dialog is closed
    });

    // Add event listeners to the tabs
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].addEventListener("click", handleTabClick);
    }

    // Set the first tab as active by default
    tabs[0].classList.add("active");

    // Call the corresponding function for the active tab
    var activeTab = tabs[0].getAttribute("data-tab");
    if (activeTab === "interaction-strcuture") {
        showInteractionTab(selectedInteractionName1);
    }

    // Function to handle tab click event
    function handleTabClick(event) {
        // Remove the active class from all tabs
        for (var i = 0; i < tabs.length; i++) {
            tabs[i].classList.remove("active");
        }

        // Add the active class to the clicked tab
        event.target.classList.add("active");

        // Call the corresponding function based on the tab clicked
        var tabName = event.target.getAttribute("data-tab");
        if (tabName === "interaction-strcuture") {
            showInteractionTab(selectedInteractionName1);
        }
    }


    // Function to showdrug image
    // Function to show drug image
    function showInteractionTab1(selectedInteractionName1) {
        var tabContent = document.querySelector(".tab-content2");
        tabContent.innerHTML = ""; // Clear previous content


        // Append the image to the tabContent
        //tabContent.appendChild(image);
    }


    function showInteractionTab(selectedInteractionName1) {
        var tabContent = document.querySelector(".tab-content2");
        tabContent.innerHTML = ""; // Clear previous content

        // Your code to fetch the row where columns "drug_bankID", "uniprot_ID", and "interaction_type" matches interaction_source, interaction_target, and selectedInteractionName1 respectively
        // Assuming you have the data in the global variable 'interaction_xlsxData'
        var matchingRow = interaction_xlsxData.find((row) => row.drugbank_id === interaction_source && row.uniprot_ID_id === interaction_target && row.interaction_type.toLowerCase() === selectedInteractionName1.toLowerCase());

        if (matchingRow) {
            // Create a table to display the interaction information
            var interactionInfoTable = document.createElement("div");
            interactionInfoTable.classList.add("interaction-info-table");

            // Create table rows and cells for each field
            var fields = [
                { label: "Interaction Type", key: "interaction_type" },
                { label: "Known Action", key: "known_action" },
                { label: "Actions", key: "actions" },
                { label: "PubMed IDs", key: "pubmed_ids" },
                // Add more fields as needed
            ];

            fields.forEach((field) => {
                var row = document.createElement("div");
                row.classList.add("interaction-info-row");

                var labelCell = document.createElement("div");
                labelCell.classList.add("interaction-info-cell", "label");
                labelCell.textContent = field.label;
                row.appendChild(labelCell);

                var valueCell = document.createElement("div");
                valueCell.classList.add("interaction-info-cell");

                // Check if the current field key is 'pubmed_ids'
                if (field.key === "pubmed_ids") {
                    // Create a new <div> element to hold the list of IDs
                    var divElement = document.createElement("div");

                    // Split the IDs string on "|"
                    var ids = matchingRow[field.key].split("|");

                    // Create a new <span> element for each ID
                    ids.forEach((id, index) => {
                        // Create a hyperlink for each ID
                        var link = document.createElement("a");
                        link.href = "https://pubmed.ncbi.nlm.nih.gov/" + id;
                        link.target = "_blank"; // Open link in a new tab
                        link.textContent = id;

                        // Append the link to the div
                        divElement.appendChild(link);

                        // Add a comma and a space after each ID, except the last one
                        if (index !== ids.length - 1) {
                            divElement.append(" , ");
                        }
                    });

                    // Append the div to the value cell
                    valueCell.appendChild(divElement);
                }
                else {
                    valueCell.textContent = matchingRow[field.key];
                }

                row.appendChild(valueCell);
                interactionInfoTable.appendChild(row);
            });

            // Append the table to the tabContent
            tabContent.appendChild(interactionInfoTable);
        } else {
            // If the selectedInteractionName1 is not found in the data, display a default message
            var errorMessage = document.createElement("p");
            errorMessage.textContent = "Interaction information not found for " + selectedInteractionName1;
            tabContent.appendChild(errorMessage);
        }
    }
}

var width = 400;
var height = 300;
var nodes = []; // Declare nodes array outside of the createChart function
var links = []; // Declare links array outside of the createChart function
var thresholdSlider = document.getElementById('threshold-slider');
var thresholdValueLabel = document.getElementById('threshold-value');
var chartDataJ;
var selectedDrugName1 = "";
var selectedProteinName1 = "";
var selectedInteractionName1 = "";
var hiddenDrugStatuses = {};
var hiddenProteinClasses = {};
var hiddenDrugTypes = {}
var hiddenInteractionTypes = {}
var nodeImages = {};
let drugStatusIndices = {};
let drugTypeIndices = {};
var currentFilters;
var interaction_source = "";
var interaction_target = "";

var imagePaths11 = {
    Nutraceutical: "images/left0.png",
    Experimental: "images/left1.png",
    Investigational: "images/left2.png",
    Approved: "images/left3.png",
    "Vet-approved": "images/left4.png",
    Illicit: "images/left5.png"
};

var colorOptions = ["#e71f73", "#d5a100", "#0a5517", "#061755", "#941a4c", "#3d3d3d"];

var colorCodes = {
    Nutraceutical: "#e71f73",
    Experimental: "#d5a100",
    Investigational: "#0a5517",
    Approved: "#061755",
    "Vet-approved": "#941a4c",
    Illicit: "#3d3d3d"
};

var colorCodesDrugType = {
    Biologic: "#03A9F4",
    "Small Molecule": "#ff5722"
};
var colorCodesDrugType_images = {
    "#03A9F4": "images/right0.png",
    "#ff5722": "images/right1.png"
};
var colorCodesDrugType = {
    Biologic: "#03A9F4",
    "Small Molecule": "#ff5722"
};
var colorPaletteDrugType = {
    "#03A9F4": "#03A9F4",  // Biologic
    "#ff5722": "#ff5722"   // Small molecule
};

var colorPalette = {
    "#e71f73": "images/left0.png",
    "#d5a100": "images/left1.png",
    "#0a5517": "images/left2.png",
    "#061755": "images/left3.png",
    "#941a4c": "images/left4.png",
    "#3d3d3d": "images/left5.png"
};

var colorImageMap = {
    "#e71f73": "images/left0.png",
    "#d5a100": "images/left1.png",
    "#0a5517": "images/left2.png",
    "#061755": "images/left3.png",
    "#941a4c": "images/left4.png",
    "#3d3d3d": "images/left5.png"
};

////Drugs Images Setting Variables
var drugStatuses = ["Nutraceutical", "Experimental", "Investigational", "Approved", "Vet-approved", "Illicit"];
var drugTypes = ["Biologic", "Small Molecule"];

// Generate all combinations of leftXrightY.png for the image paths
var imagePaths = {};
Object.keys(colorCodes).forEach((key, i) => {
    Object.keys(colorCodesDrugType).forEach((key2, j) => {
        var keyCombo = key + "|" + key2;
        imagePaths[keyCombo] = `images/capsules/left${i}right${j}.png`;
    });
});

// Function to convert xlsx to JSON
function xlsxToJson(file, callback) {
    fetch(file)
        .then(response => response.blob())
        .then(blob => {
            var reader = new FileReader();
            reader.onload = function (e) {
                var data = new Uint8Array(e.target.result);
                var workbook = XLSX.read(data, { type: 'array' });
                var jsonData = XLSX.utils.sheet_to_json(workbook.Sheets[workbook.SheetNames[0]]);

                callback(jsonData);
            };
            reader.readAsArrayBuffer(blob);
        })
        .catch(error => {
            console.error('Error reading the file:', error);
        });
}

function processData() {
    const jsonFilePath = json_GeneralFile; // JSON file path

    fetch(jsonFilePath)
        .then((response) => response.json())
        .then((data) => {
            // Extract nodes and links from the JSON data
            // console.log(data);
            chartDataJ = data;
            data.forEach(function (row) {
                console.log(row);
                var drugName = row.drug_name;
                var drugID = row.drugbank_id;
                var protein = row.protein;
                var interaction = row.interaction;
                var drugStatus = row.Drug_status; // Get the "Drug_status" value
                var drugType = row.drugtype; // Get the "Drug_status" value
                var proteinClass = row.Protein_Class;

                if (!nodes.find(function (node) { return node.id === drugName; })) {

                    nodes.push({ id: drugName, isParent: true, radius: 10, Drug_status: drugStatus, Drug_type: drugType, Drug_ID: drugID }); // Include the "Drug_status" value in the node object
                }

                if (!nodes.find(function (node) { return node.id === protein; })) {

                    nodes.push({ id: protein, isParent: false, radius: 5, Protein_Class: proteinClass }); // Include the "Protein_Class" value in the node object
                }

                if (!nodes.find(function (node) { return node.id === drugName; })) {
                    nodes.push({ id: drugName, isParent: true, radius: 10 });
                }

                if (!nodes.find(function (node) { return node.id === protein; })) {
                    nodes.push({ id: protein, isParent: false, radius: 5 });
                }
                links.push({ source: drugName, target: protein, type: interaction });
            });

            var childNodeMap = {};
            links.forEach(function (link) {
                if (!link.target.isParent) {
                    var childNodeId = link.target.id;
                    childNodeMap[childNodeId] = (childNodeMap[childNodeId] || 0) + 1;
                }
            });

            // Assign the parent count to each child node
            nodes.filter(function (d) { return !d.isParent; }).forEach(function (node) {
                node.degree = childNodeMap[node.id] || 0;
            });

            // Set the maximum value of the threshold slider
            thresholdSlider.max = nodes.filter(function (node) { return node.isParent; }).length;

            // Set the default value of the threshold slider to the maximum
            thresholdSlider.value = 50;
            thresholdValueLabel.textContent = thresholdSlider.value;

            // Create the chart using D3.js
            createChart(links);
            // createLegend();
            createLegend_status();
            createLegend_drugType();
            createProteinsLegend();

            // Add an event listener to detect changes in the threshold slider value
            thresholdSlider.addEventListener('input', function () {
                thresholdValueLabel.textContent = thresholdSlider.value;
                updateChartVisibility();
            });
        })
        .catch((error) => {
            console.error("Error reading the JSON file:", error);
        });

    d3.select("#loading").style("display", "none");
}

// Read the data from the Excel file

var link;
var node;
var svg, chart;
var simulation = null




// Create the Forced Directed Network Chart
function createChart(links) {
    d3.select("#chart").selectAll("*").remove();

    var container = d3.select("#chart");
    var containerWidth = [container.node().getBoundingClientRect().width] - 10;
    var containerHeight = [container.node().getBoundingClientRect().height] - 10;
    //console.log("Width : "+containerWidth+"  ----  Height : "+containerHeight);

    var zoom = d3.zoom()
        .scaleExtent([0.1, 10])
        .on("zoom", function (event, d) {
            //console.log("zoom event:", event); 
            //console.log("event.transform:", event.transform);
            svg.attr("transform", event.transform.toString());
        });

    // SVG creation with zoom behavior
    svg = container.append("svg")
        .attr("width", containerWidth)
        .attr("height", containerHeight)
        .call(zoom);

    chart = svg.append("g") // Assign the group element to the 'chart' variable
        .attr("class", "chart");

    var chargeStrength = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--charge-strength'));
    var distanceBetweenNodes = 60;
    var noOfTotalNodes11 = links.length;

    console.log("HHHHHHHH" + noOfTotalNodes11);

    if (noOfTotalNodes11 < 100) {
        chargeStrength = -500
        var distanceBetweenNodes = 100;
    } else if (noOfTotalNodes11 > 99 && noOfTotalNodes11 < 200) {
        chargeStrength = -150
        var distanceBetweenNodes = 100;
    } else if (noOfTotalNodes11 > 199 && noOfTotalNodes11 < 250) {
        chargeStrength = -150
        var distanceBetweenNodes = 100;
    } else if (noOfTotalNodes11 > 249 && noOfTotalNodes11 < 300) {
        chargeStrength = -100
        var distanceBetweenNodes = 80;
    } else if (noOfTotalNodes11 > 299 && noOfTotalNodes11 < 350) {
        chargeStrength = -100
        var distanceBetweenNodes = 80;
    } else if (noOfTotalNodes11 > 349 && noOfTotalNodes11 < 400) {
        chargeStrength = -100
        var distanceBetweenNodes = 60;
    } else if (noOfTotalNodes11 > 399) {
        var distanceBetweenNodes = 60;
    }

    simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(function (d) { return d.id; }).distance(distanceBetweenNodes))
        .force("charge", d3.forceManyBody().strength(chargeStrength))
        // Adding centering forces for X and Y coordinates
        .force("x", d3.forceX(containerWidth / 2).strength(0.1))
        .force("y", d3.forceY(containerHeight / 2).strength(0.1))

        .on("end", function () {
            nodes.forEach(function (node) {
                node.fx = node.x;
                node.fy = node.y;
            });
        });

    //console.log("Creating nodes and links...");
    link = svg.selectAll(".link")
        .data(links)
        .enter().append("line")
        .attr("class", "link")
        .style("stroke", function (d) { return "gray"; })
        .style("stroke-width", 2)
        .on("click", function (event, d) {
            interaction_source = d.source.Drug_ID;
            interaction_target = d.target.id;
            // console.log(interaction_source);
            // console.log(interaction_target);
            console.log(d.type);
            showDialog_Links(d.type, d.type)
            //showDialog_Interaction(d.id, d.id);
        });

    node = svg.selectAll(".node")
        .data(nodes)
        .enter().append("g")
        .attr("class", "node")
        .call(drag(simulation));

    var childNodeMap = {};
    links.forEach(function (link) {
        if (!link.target.isParent) {
            var childNodeId = link.target.id;
            childNodeMap[childNodeId] = (childNodeMap[childNodeId] || 0) + 1;
        }
    });

    // Add the following code to calculate the size of the child nodes based on the number of connected parent nodes
    var childNodeMap = {};
    links.forEach(function (link) {
        if (!link.target.isParent) {
            var childNodeId = link.target.id;
            childNodeMap[childNodeId] = (childNodeMap[childNodeId] || 0) + 1;
        }
    });

    // Add the following code to calculate the size of the child nodes based on the number of connected parent nodes
    node.filter(function (d) { return !d.isParent; })
        .append("circle")
        .attr("r", function (d) {
            var parentCount = childNodeMap[d.id] || 1;
            return 5 + (parentCount - 1) + 1; // Increase the size by 3px for each connected parent node
        })
        .style("fill", function (d) {
            return proteinColorMap[d.Protein_Class] || "steelblue";
        })
        .on("click", function (event, d) {
            console.log(d.id);
            showDialog_Child(d.id, d.id);
        });

    node.filter(function (d) { return d.isParent; })
        .attr("class", "node-parent")
        .append("image")
        .attr("class", "node-image")
        .attr("xlink:href", function (d) {

            var key = d.Drug_status + "|" + d.Drug_type;
            //console.log("key: ", key); // print the key
            //console.log("key: ", imagePaths[key]); // print the key
            //return imagePaths[key];

            return imagePaths[key];
        })
        .attr("x", -12)
        .attr("y", -12)
        .attr("width", 30)
        .attr("height", 30)
        .on("click", function (event, d) {
            console.log(d.id);
            showDialog(d.id, d.id);
        });

    node.filter(function (d) { return d.isParent; })
        .append("text")
        .attr("dx", 14)
        .attr("dy", "2em")
        .text(function (d) { return d.id; })
        .attr("class", "node-label");

    node.append("title")
        .text(function (d) { return d.id; });

    node.filter(function (d) { return !d.isParent; })
        .append("text")
        .attr("dx", 10)
        .attr("dy", ".25em")
        .text(function (d) { return d.id; })
        .attr("class", "node-label")

    simulation.on("tick", function () {
        link.attr("x1", function (d) { return d.source.x; })
            .attr("y1", function (d) { return d.source.y; })
            .attr("x2", function (d) { return d.target.x; })
            .attr("y2", function (d) { return d.target.y; });

        node.attr("transform", function (d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
    });

    // Enable drag behavior for nodes
    function drag(simulation) {
        // console.log("Setting up drag behavior..."); 
        function dragStarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }

        function dragEnded(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            // Removed setting of d.fx and d.fy to null here
        }

        return d3.drag()
            .on("start", dragStarted)
            .on("drag", dragged)
            .on("end", dragEnded);
    }

    // Button click handlers
    d3.select(".zoom-in-btn").on("click", function () {
        console.log("Zoom in called");
        zoom.scaleBy(svg.transition().duration(750), 1.1);  // scale up by 10%
    });

    d3.select(".zoom-out-btn").on("click", function () {
        console.log("Zoom out called");
        zoom.scaleBy(svg.transition().duration(750), 0.9);  // scale down by 10%
    });

    console.log("Chart created.");
    updateChartVisibility();
}

// Update the chart visibility based on the threshold value
function updateChartVisibility() {
    var threshold = parseInt(thresholdSlider.value);

    var visibleParents = nodes.filter(function (node) {
        return node.isParent;
    }).slice(0, threshold);

    nodes.forEach(function (node) {
        if (node.isParent) {
            node.hidden = !visibleParents.includes(node);
        } else {
            var parentLinks = links.filter(function (link) {
                return link.target.id === node.id;
            });
            node.hidden = !parentLinks.some(function (link) {
                return visibleParents.includes(link.source);
            });
        }
    });

    links.forEach(function (link) {
        link.hidden = link.source.hidden || link.target.hidden;
    });

    // Call updateAllFilters to update visibility based on new threshold
    updateAllFilters();
}

function hideNodeAndChildren(node) {
    node.hidden = true;

    var childLinks = links.filter(function (link) {
        return link.source.id === node.id;
    });

    var childNodes = childLinks.map(function (link) {
        return link.target;
    });

    childNodes.forEach(function (child) {
        var parentLinks = links.filter(function (link) {
            return link.target.id === child.id;
        });

        var allParentsHidden = parentLinks.every(function (link) {
            return link.source.hidden;
        });

        if (allParentsHidden) {
            hideNodeAndChildren(child);
        }
    });
}

d3.select("#redrawChart").on("click", function () {
    redrawChart(links);
});

function redrawChart1(originalLinks) {
    if (simulation) {
        console.log("Simulation before restart: ", simulation);

        // Add nodes and links to the simulation and restart
        simulation.nodes(nodes).force("link").links(links);

        simulation.alpha(1).restart();

        console.log("Simulation after restart: ", simulation);
    } else {
        console.log("Simulation is not defined");
    }
}

function redrawChart(originalLinks) {
    if (simulation) {
        console.log("Simulation before restart: ", simulation);

        // Unfix the node positions
        nodes.forEach(function (node) {
            node.fx = null;
            node.fy = null;
        });

        // Add nodes and links to the simulation and restart
        simulation.nodes(nodes).force("link").links(links);

        simulation.alpha(1).restart();

        // Add 'end' event listener to fix node positions when simulation ends
        simulation.on("end", function () {
            nodes.forEach(function (node) {
                node.fx = node.x;
                node.fy = node.y;
            });
        });

        console.log("Simulation after restart: ", simulation);
    } else {
        console.log("Simulation is not defined");
    }
}

// Get color based on interaction type
function getColor(type) {
    if (type.toLowerCase() === "Target".toLowerCase()) {
        return "green";
    } else if (type.toLowerCase() === "Enzyme".toLowerCase()) {
        return "blue";
    } else if (type.toLowerCase() === "Transporter".toLowerCase()) {
        return "red";
    } else if (type.toLowerCase() === "Carrier".toLowerCase()) {
        return "orange";
    } else {
        return "black";
    }
}

var colorMap = {
    "target": "green",
    "enzyme": "blue",
    "transporter": "red",
    "carrier": "orange",
    "unknown": "black"
};
var hiddenInteractions = {
    "target": false,
    "enzyme": false,
    "transporter": false,
    "carrier": false,
    "unknown": false
};

//Legends Dragable code below
// Assuming you've imported D3 as d3
// Draggable functionality for the legend box

//Legends Dragable end code 

// Create the legend for interactions
function createLegend() {
    var interactions = ["Target", "Enzyme", "Transporter", "Carrier", "Unknown"];
    var legendContent = d3.select("#legend-content");

    var uniqueInteractions = new Set();

    links.forEach(function (link) {
        var interaction = link.type; // No need to convert to lowercase
        if (interactions.includes(interaction.charAt(0).toUpperCase() + interaction.slice(1)) && !uniqueInteractions.has(interaction)) {
            createLegendItem(interaction, getColor(interaction));
            uniqueInteractions.add(interaction);
        }
    });
    function createLegendItem(interaction, color) {
        var legendItem = legendContent.append("div")
            .style("display", "flex")
            .style("align-items", "center")
            .style("margin-bottom", "5px")
            .on("click", function () {
                d3.select(this).classed("selected-legend1", true);
            });

        var dropdown = legendItem.append("div")
            .attr("class", "dropdown1")
            .style("position", "relative")
            .style("width", "20px")
            .style("height", "5px") // Adjust the height to control the line thickness
            .style("background-color", color)
            .on("click", function () {
                var clickedText = d3.select(this.parentNode).select("span");
                if (!clickedText.classed("text-through")) {
                    var menu = d3.select(this).select(".dropdown-menu1");
                    if (menu.style("display") === "none") {
                        menu.style("display", "flex");
                    } else {
                        menu.style("display", "none");
                    }
                }
            });

        var dropdownMenu = dropdown.append("div")
            .attr("class", "dropdown-menu1")
            .style("display", "none")
            .style("position", "absolute")
            .style("left", "25px")
            .style("height", "20px")
            .style("flex-direction", "row");

        for (var i = 0; i < interactions.length; i++) {
            var color = getColor(interactions[i]);
            dropdownMenu.append("div")
                .style("width", "20px")
                .style("height", "20px")
                .style("background-color", color)
                .on("click", function (selectedInteraction) {
                    return function () {
                        var selectedColor = getColor(selectedInteraction);
                        var selectedLegendItem = d3.select(".selected-legend1");
                        colorMap[interaction.toLowerCase()] = selectedColor;
                        dropdown.style("background-color", selectedColor);
                        if (selectedLegendItem.node()) {  // Check if the selection is not empty
                            selectedLegendItem.select(".dropdown-menu1").style("display", "none");
                        }
                        d3.selectAll(".selected-legend1").classed("selected-legend1", false);
                        redrawLinks();
                    };
                }(interactions[i]));
        }

        var legendText = legendItem.append("span")
            .style("margin-left", "10px")
            .text(interaction);

        // Event listener for the legend item text
        // Assuming that you have already defined the "nodes" and "links" arrays
        // and the "hiddenInteractions" object to track the visibility of interactions.
        legendText.on("click", function () {
            var clickedText = d3.select(this);
            var interaction = clickedText.text().toLowerCase();

            if (clickedText.classed("text-through")) {
                clickedText.classed("text-through", false);
                hiddenInteractions[interaction] = false;
            } else {
                clickedText.classed("text-through", true);
                hiddenInteractions[interaction] = true;
            }
            updateAllFilters();
        });
    }

    document.addEventListener("click", function (event) {
        var dropdownMenus = d3.selectAll(".dropdown-menu1");
        dropdownMenus.each(function () {
            var menu = d3.select(this);
            if (
                menu.style("display") === "flex" &&
                !menu.empty() &&
                !d3.select(event.target).classed("selected-legend1") &&
                !d3.select(event.target.parentNode).classed("selected-legend1")
            ) {
                menu.style("display", "none");
            }
        });
        d3.selectAll(".selected-legend1").classed("selected-legend1", false);
    });
}










function drawLinks() {
    svg.selectAll(".link")
        .data(links)
        .enter().append("line")
        .attr("class", "link")
        .style("stroke", function (d) { return colorMap[d.type]; }) // Use colorMap to get the color for the link type
    // ... rest of your link drawing code ...
}

// And here's the redrawLinks function
function redrawLinks() {
    // Update the 'stroke' style of the links using the updated colorMap
    //console.log(link)
    link.style("stroke", function (d) {
        console.log("Testinng Interaction :" + colorMap[d.type]);
        return colorMap[d.type];
    });
}



//Protein Class Color Map
var proteinColorMap = {
    "Enzyme": "#1f77b4",
    "Epigenetic regulator": "black",
    "GPCR": "#2ca02c",
    "Ion channel": "#d62728",
    "Kinase": "#9467bd",
    "Nuclear receptor": "#ff7f0e",
    "Transporter": "#7f7f7f",
    "Unknown": "#8c564b"
};
function updateChildNodeColors() {
    d3.selectAll(".node circle")
        .style("fill", function (d) { return proteinColorMap[d.Protein_Class] || "steelblue"; });
}

function createProteinsLegend() {
    var hiddenProteins = {}; // Change this to hiddenProteinClasses
    var proteins = ["Enzyme", "Epigenetic regulator", "GPCR", "Ion channel", "Kinase", "Nuclear receptor", "Transporter", "Unknown"];
    var legendContent = d3.select("#legend_protein_status-content");
    var uniqueProteins = new Set();

    links.forEach(function (link) {
        var proteinClass11 = link.target.Protein_Class; // No need to convert to lowercase
        //console.log(proteinClass11);

        if (proteins.includes(proteinClass11) && !uniqueProteins.has(proteinClass11)) {
            createLegendItem(proteinClass11, proteinColorMap[proteinClass11]);
            uniqueProteins.add(proteinClass11);
        }

    });
    /*
  proteins.forEach(function(protein) {
                    createLegendItem(protein, proteinColorMap[protein]);
  });
                */

    function createLegendItem(protein, color) {
        var legendItem = legendContent.append("div")
            .style("display", "flex")
            .style("align-items", "center")
            .style("margin-bottom", "5px")
            .on("click", function () {
                d3.select(this).classed("selected-legend2", true);
            });

        var dropdown = legendItem.append("div")
            .attr("class", "dropdown2")
            .style("position", "relative")
            .style("width", "10px")
            .style("height", "10px")
            .style("background-color", color)
            .on("click", function () {
                var clickedText = d3.select(this.parentNode).select("span");
                if (!clickedText.classed("text-through")) {
                    var menu = d3.select(this).select(".dropdown-menu2");
                    if (menu.style("display") === "none") {
                        menu.style("display", "flex");
                    } else {
                        menu.style("display", "none");
                    }
                }
            });

        var dropdownMenu = dropdown.append("div")
            .attr("class", "dropdown-menu2")
            .style("display", "none")
            .style("position", "absolute")
            .style("left", "25px")
            .style("height", "20px")
            .style("flex-direction", "row");

        for (let i = 0; i < proteins.length; i++) {
            let color = proteinColorMap[proteins[i]];
            dropdownMenu.append("div")
                .style("width", "20px")
                .style("height", "20px")
                .style("background-color", color)
                .on("click", (function (selectedProtein) {
                    return function () {
                        // d3.event.stopPropagation();  // Stop the click event from bubbling up to parent elements
                        var selectedColor = proteinColorMap[selectedProtein];
                        var selectedLegendItem = d3.select(".selected-legend2");
                        proteinColorMap[protein] = selectedColor;
                        dropdown.style("background-color", selectedColor);
                        if (selectedLegendItem.node()) {
                            selectedLegendItem.select(".dropdown-menu2").style("display", "none");
                        }
                        d3.selectAll(".selected-legend2").classed("selected-legend2", false);
                        updateChildNodeColors();
                    };
                })(proteins[i]));
        }

        var legendText = legendItem.append("span")
            .style("margin-left", "10px")
            .text(protein);

        // Assuming 'legendText' is a selection of the legend text elements
        // Assuming you have already created nodes, links, labels, and images in your chart

        legendText.on("click", function () {
            var clickedText = d3.select(this);
            var proteinClass = clickedText.text();

            if (clickedText.classed("text-through")) {
                clickedText.classed("text-through", false);
                hiddenProteinClasses[proteinClass] = false;
            } else {
                clickedText.classed("text-through", true);
                hiddenProteinClasses[proteinClass] = true;
            }


            updateAllFilters();

        });







    }

    document.addEventListener("click", function (event) {
        var dropdownMenus = d3.selectAll(".dropdown-menu2");
        dropdownMenus.each(function () {
            var menu = d3.select(this);
            if (
                menu.style("display") === "flex" &&
                !menu.empty() &&
                !d3.select(event.target).classed("selected-legend2") &&
                !d3.select(event.target.parentNode).classed("selected-legend2")
            ) {
                menu.style("display", "none");
            }
        });
        d3.selectAll(".selected-legend2").classed("selected-legend2", false);
    });
}


// Call the function to create the legend
function createLegend_status() {
    var legendContent = d3.select("#legend_drug_status-content");
    var drugStatusArray = ["Nutraceutical", "Experimental", "Investigational", "Approved", "Vet-approved", "Illicit"];
    var uniqueDrugStatus = new Set();

    links.forEach(function (link) {
        var drugStatusClass11 = link.source.Drug_status;

        if (drugStatusArray.includes(drugStatusClass11) && !uniqueDrugStatus.has(drugStatusClass11)) {
            createLegendItem(drugStatusClass11, colorCodes[drugStatusClass11]);
            uniqueDrugStatus.add(drugStatusClass11);
        }
    });
    /*
  for (var status in colorCodes) {
                    createLegendItem(status, colorCodes[status]);
  }
                */


    function createLegendItem(status, color) {
        var legendItem = legendContent.append("div")
            .style("display", "flex")
            .style("align-items", "center")
            .style("margin-bottom", "5px")
            .on("click", function () {
                d3.select(this).classed("legend-item-clicked", true); // Add a class to the clicked legend item
            });

        var dropdown = legendItem.append("div")
            .attr("class", "dropdown1")
            .style("position", "relative")
            .style("width", "25px")
            .style("height", "12px")
            .style("border-radius", "12px")
            .style("background-color", color)
            .on("click", function () {
                var clickedText = d3.select(this.parentNode).select("span");
                if (!clickedText.classed("text-through")) {
                    var menu = d3.select(this).select(".dropdown-menu");
                    if (menu.style("display") === "none") {
                        menu.style("display", "flex");
                    } else {
                        menu.style("display", "none");
                    }
                }
            });


        var dropdownMenu = dropdown.append("div")
            .attr("class", "dropdown-menu")
            .style("display", "none")  // make sure the dropdown menu is hidden by default
            .style("position", "absolute")
            .style("left", "25px")
            .style("height", "20px")
            .style("flex-direction", "row");

        for (var color in colorPalette) {
            dropdownMenu.append("div")
                .style("width", "20px")
                .style("height", "20px")
                .style("background-color", color)
                .on("click", function (selectedColor) {
                    return function () {
                        colorCodes[status] = selectedColor;
                        dropdown.style("background-color", selectedColor);
                        //changeNodeImage(status, colorPalette[selectedColor]);
                        //changeNodeImage(status, drugType, colorPalette[selectedColor]);
                        changeNodeImage(status, selectedColor);
                        dropdown.select(".dropdown-menu").style("display", "none"); // <--- This line hides the dropdown after color selection
                        event.stopPropagation();
                    };
                }(color));
        }

        var legendText = legendItem.append("span")
            .style("margin-left", "10px") // reduce left margin from 30px to 10px
            .text(status);

        // Event listener for the legend item text
        legendText.on("click", function () {
            var clickedText = d3.select(this);
            var drugStatus = clickedText.text();

            if (clickedText.classed("text-through")) {
                clickedText.classed("text-through", false);
                hiddenDrugStatuses[drugStatus] = false;
            } else {
                clickedText.classed("text-through", true);
                hiddenDrugStatuses[drugStatus] = true;
            }

            updateAllFilters();

        });

    }

    // Event listener to close the dropdown menus when clicked anywhere on the webpage
    document.addEventListener("click", function (event) {
        var dropdownMenus = d3.selectAll(".dropdown-menu");
        dropdownMenus.each(function () {
            var menu = d3.select(this);
            if (menu.style("display") === "flex" && !menu.empty() && !d3.select(event.target).classed("legend-item-clicked") && !d3.select(event.target.parentNode).classed("legend-item-clicked")) {
                menu.style("display", "none");
            }
        });
        d3.selectAll(".legend-item-clicked").classed("legend-item-clicked", false); // Remove the class from all legend items
    });
}


function updateVisibility_legends() {
    // Update visibility of nodes
    d3.selectAll('.node')
        .style('visibility', function (d) {
            // Hide or show parent nodes based on the drug status, drug type and interaction
            if (d.isParent && (hiddenDrugStatuses[d.Drug_status] || hiddenDrugTypes[d.Drug_type] || links.some(l => l.source.id === d.id && hiddenInteractions[l.type]))) {
                return 'hidden';
            }

            // Hide or show child nodes based on the protein class and interaction
            if (!d.isParent && (hiddenProteinClasses[d.Protein_Class] || links.some(l => l.target.id === d.id && hiddenInteractions[l.type]))) {
                return 'hidden';
            }

            // If the node is neither hidden by drug status, protein class nor interaction
            return 'visible';
        });

    // Update visibility of links
    d3.selectAll('.link')
        .style('visibility', function (d) {
            // Hide or show links based on the interaction type, drug status, drug type, and protein class
            if (hiddenInteractions[d.type] || hiddenDrugStatuses[d.source.Drug_status] || hiddenDrugTypes[d.source.Drug_type] || hiddenProteinClasses[d.target.Protein_Class]) {
                return 'hidden';
            }

            // If the link is neither hidden by interaction type, drug status, nor protein class
            return 'visible';
        });
}






function changeNodeImage(status, selectedColor) {
    const newImagePath = colorPalette[selectedColor];
    const drugStatusIndex = newImagePath.match(/left(\d+)/)[1];

    d3.selectAll(".node-parent")
        .filter(function (node) {
            return node.Drug_status === status;
        })
        .each(function (node) {
            const drugType = node.Drug_type;

            // Fetch the current image path of the node
            let currentImagePath = d3.select(this).select('image').attr('xlink:href');

            // Extract drugTypeIndex from the current image path
            let drugTypeIndex = currentImagePath.match(/right(\d+)/)[1];

            const correctImagePath = `images/capsules/left${drugStatusIndex}right${drugTypeIndex}.png`;
            console.log(correctImagePath);
            nodeImages[node.id] = correctImagePath;
            d3.select(this)
                .select("image")
                .attr("xlink:href", correctImagePath);
        });
}







function createLegend_drugType() {
    var legendContent = d3.select("#legend_drug_type-content");

    var drugTypeArray = ["Biologic", "Small Molecule"];
    var uniqueDrugType = new Set();

    links.forEach(function (link) {
        var drugTypeClass11 = link.source.Drug_type;
        console.log(drugTypeClass11);


        if (drugTypeArray.includes(drugTypeClass11) && !uniqueDrugType.has(drugTypeClass11)) {
            createLegendItem(drugTypeClass11, colorCodesDrugType[drugTypeClass11]);
            uniqueDrugType.add(drugTypeClass11);
        }

    });

    /*
   for (var drugType in colorCodesDrugType) {
                     createLegendItem(drugType, colorCodesDrugType[drugType]);
   }
                 */

    function createLegendItem(drugType, color) {
        var legendItem = legendContent.append("div")
            .style("display", "flex")
            .style("align-items", "center")
            .style("margin-bottom", "5px")
            .on("click", function () {
                d3.select(this).classed("legend-item-clicked", true); // Add a class to the clicked legend item
            });

        var dropdown = legendItem.append("div")
            .attr("class", "dropdown1")
            .style("position", "relative")
            .style("width", "25px")
            .style("height", "12px")
            .style("border-radius", "12px")
            .style("background-color", color)
            .on("click", function () {
                var clickedText = d3.select(this.parentNode).select("span");
                if (!clickedText.classed("text-through")) {
                    var menu = d3.select(this).select(".dropdown-menu");
                    if (menu.style("display") === "none") {
                        menu.style("display", "flex");
                    } else {
                        menu.style("display", "none");
                    }
                }
            });

        var dropdownMenu = dropdown.append("div")
            .attr("class", "dropdown-menu")
            .style("display", "none")  // make sure the dropdown menu is hidden by default
            .style("position", "absolute")
            .style("left", "25px")
            .style("height", "20px")
            .style("flex-direction", "row");

        for (var color in colorPaletteDrugType) {
            dropdownMenu.append("div")
                .style("width", "20px")
                .style("height", "20px")
                .style("background-color", color)
                .on("click", function (selectedColor) {
                    return function () {
                        colorCodesDrugType[drugType] = selectedColor;
                        dropdown.style("background-color", selectedColor);
                        let newImagePath = colorCodesDrugType_images[selectedColor];
                        //console.log(newImagePath)
                        changeNodeImageForDrugType(drugType, selectedColor)
                        dropdown.select(".dropdown-menu").style("display", "none");
                        event.stopPropagation();
                    };
                }(color));
        }

        var legendText = legendItem.append("span")
            .style("margin-left", "10px")
            .text(drugType);


        legendText.on("click", function () {
            var clickedText = d3.select(this);
            var drugType = clickedText.text();

            if (clickedText.classed("text-through")) {
                clickedText.classed("text-through", false);
                hiddenDrugTypes[drugType] = false;
            } else {
                clickedText.classed("text-through", true);
                hiddenDrugTypes[drugType] = true;
            }


            updateAllFilters();

        });


        // TODO: You need to implement the event listener for the legend item text based on the drug type.
        // Refer to the existing legend for how to implement this part.
    }
}


function changeNodeImageForDrugType(drugType, selectedColor) {
    const newImagePath = colorCodesDrugType_images[selectedColor];
    const drugTypeIndex = newImagePath.match(/right(\d+)/)[1];

    d3.selectAll(".node-parent")
        .filter(function (node) {
            return node.Drug_type === drugType;
        })
        .each(function (node) {
            // Fetch the current image path of the node
            let currentImagePath = d3.select(this).select('image').attr('xlink:href');
            console.log(currentImagePath)
            // Extract drugStatusIndex from the current image path
            let drugStatusIndex = currentImagePath.match(/left(\d+)/)[1];

            const correctImagePath = `images/capsules/left${drugStatusIndex}right${drugTypeIndex}.png`;
            console.log(correctImagePath);
            nodeImages[node.id] = correctImagePath;
            d3.select(this)
                .select("image")
                .attr("xlink:href", correctImagePath);
        });
}

function updateAllFilters() {
    // parent nodes
    d3.selectAll(".node-parent")
        .style('visibility', function (d) {
            if (d.hidden) { // if hidden by slider filter
                return 'hidden';
            }

            var relatedLinks = links.filter(l => l.source.id === d.id);
            var anyVisibleChildren = relatedLinks.some(l => !hiddenInteractions[l.type] && !hiddenProteinClasses[nodes.find(n => n.id === l.target.id).Protein_Class]);

            // Check Drug_status and Drug_type directly in the parent node
            var isHiddenBasedOnDrugStatus = hiddenDrugStatuses[d.Drug_status];
            var isHiddenBasedOnDrugType = hiddenDrugTypes[d.Drug_type];

            var isHiddenBasedOnInteraction = relatedLinks.every(l => hiddenInteractions[l.type]);
            var isHiddenBasedOnProteinClass = !anyVisibleChildren;

            if (isHiddenBasedOnInteraction || isHiddenBasedOnProteinClass || isHiddenBasedOnDrugStatus || isHiddenBasedOnDrugType) {
                return 'hidden';
            }
            return 'visible';
        });

    // child nodes
    d3.selectAll(".node:not(.node-parent)")
        .selectAll('circle, text')
        .style('visibility', function (d) {
            if (d.hidden) { // if hidden by slider filter
                return 'hidden';
            }

            var relatedLinks = links.filter(l => l.target.id === d.id);
            var isHiddenBasedOnInteraction = relatedLinks.every(l => hiddenInteractions[l.type]);
            var isHiddenBasedOnProteinClass = hiddenProteinClasses[d.Protein_Class];

            // Hide if not connected to any parent
            if (relatedLinks.length === 0) {
                return 'hidden';
            }

            // Check if all parents connected to this child are hidden
            // Check if all parents connected to this child are hidden
            var allParentsHidden = relatedLinks.every(l => {
                var parentNode = nodes.find(n => n.id === l.source.id && n.isParent);
                return parentNode && (
                    hiddenDrugStatuses[parentNode.Drug_status] ||
                    hiddenDrugTypes[parentNode.Drug_type] ||
                    parentNode.hidden ||
                    hiddenInteractions[l.type] // Here we use the interaction type of the link
                );
            });


            if (isHiddenBasedOnInteraction || isHiddenBasedOnProteinClass || allParentsHidden) {
                return 'hidden';
            }
            return 'visible';
        });

    // links
    link.style('visibility', function (d) {
        if (d.hidden) { // if hidden by slider filter
            return 'hidden';
        }
        var isHiddenBasedOnInteraction = hiddenInteractions[d.type];
        var isHiddenBasedOnProteinClass = hiddenProteinClasses[d.target.Protein_Class];
        var isHiddenBasedOnDrugStatus = hiddenDrugStatuses[d.source.Drug_status];
        var isHiddenBasedOnDrugType = hiddenDrugTypes[d.source.Drug_type];

        // Adding visibility check for source and target nodes for the link.
        var isSourceNodeHidden = nodes.find(n => n.id === d.source.id).hidden;
        var isTargetNodeHidden = nodes.find(n => n.id === d.target.id).hidden;

        if (isHiddenBasedOnInteraction || isHiddenBasedOnProteinClass || isHiddenBasedOnDrugStatus || isHiddenBasedOnDrugType || isSourceNodeHidden || isTargetNodeHidden) {
            return 'hidden';
        }
        return 'visible';
    });
}








// Pull nodes towards the center
// Pull nodes towards the center
// Pull nodes towards the center
function pullToCenterParent11(width, height, strength, gap) {
    var centerX = width / 2;
    var centerY = height / 2;

    return function () {
        var parentNodes = nodes.filter(function (n) { return n.isParent; });
        for (var i = 0, n = parentNodes.length; i < n; ++i) {
            var node = parentNodes[i];
            var targetX = centerX + (i - n / 2) * gap;
            var targetY = centerY + (i - n / 2) * gap;

            node.vx += (targetX - node.x) * strength;
            node.vy += (targetY - node.y) * strength;
        }
    };
}


// Pull nodes towards the center
function pullToCenterParent(width, height, strength) {
    return function () {
        for (var i = 0, n = nodes.length; i < n; ++i) {
            var node = nodes[i];
            if (node.isParent) {
                var childNodes = nodes.filter(function (n) { return n.parent === node.id; });
                if (childNodes.length > 0) {
                    var centerX = d3.mean(childNodes, function (n) { return n.x; });
                    var centerY = d3.mean(childNodes, function (n) { return n.y; });

                    node.vx += (centerX - node.x) * strength;
                    node.vy += (centerY - node.y) * strength;
                }
            }
        }
    };
}


function pullToCenterChild(width, height, strength, gap) {
    return function () {
        for (var i = 0, n = nodes.length; i < n; ++i) {
            var node = nodes[i];
            if (!node.isParent) {
                var parent = nodes.find(function (n) { return n.id === node.parent; });
                if (parent) {
                    var parentX = parent.x;
                    var parentY = parent.y;
                    var dx = parentX - node.x;
                    var dy = parentY - node.y;
                    var distance = Math.sqrt(dx * dx + dy * dy);
                    var targetX = parentX + dx / distance * (parent.radius + gap + node.radius);
                    var targetY = parentY + dy / distance * (parent.radius + gap + node.radius);

                    // Adjust the target coordinates based on node radius and text bounding box
                    var nodeText = node.isParent ? "" : node.id;
                    var textBoundingBox = getTextBoundingBox(nodeText);
                    var textWidth = textBoundingBox.width + 10;
                    var textHeight = textBoundingBox.height + 10;
                    var offsetX = textWidth / 2;
                    var offsetY = textHeight / 2;

                    targetX += node.x > parentX ? offsetX : -offsetX;
                    targetY += node.y > parentY ? offsetY : -offsetY;

                    node.vx += (targetX - node.x) * strength;
                    node.vy += (targetY - node.y) * strength;
                }
            }
        }
    };
}

// Add boundary force to prevent nodes from going outside the chart area
function boundaryForce(width, height, padding) {
    return function () {
        for (var i = 0, n = nodes.length; i < n; ++i) {
            var node = nodes[i];
            var radius = node.isParent ? node.radius : node.radius + 5;
            var x = node.x + node.vx;
            var y = node.y + node.vy;

            if (x - radius < 0) {
                node.vx += (radius - x + padding);
            } else if (x + radius > width) {
                node.vx -= (x + radius - width + padding);
            }

            if (y - radius < 0) {
                node.vy += (radius - y + padding);
            } else if (y + radius > height) {
                node.vy -= (y + radius - height + padding);
            }
        }
    };
}

// Get the bounding box of a text element
function getTextBoundingBox(text) {
    var svg = d3.select("body").append("svg");
    var textElement = svg.append("text").text(text);
    var boundingBox = textElement.node().getBBox();
    svg.remove();
    return boundingBox;
}

// Drag event handlers
function drag(simulation) {
    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }

    function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

    return d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
}