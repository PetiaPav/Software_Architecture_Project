// Function for generating pdf
function print(rows = 1) {
    const filename  = 'uber-sante-receipt.pdf';
    let size = (rows * 8) + 80;

    html2canvas(document.querySelector('#content'), 
                            {scale: 3}
                     ).then(canvas => {
        let pdf = new jsPDF('p', 'mm', 'a4');
        pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 10, 10, 190, size);
        pdf.save(filename);
    });
}

// Small script for generating chosen fields
$(document).ready(function () {
    var chosenField = $('.chosen-select');
    if(chosenField !== null) {
        chosenField.chosen({
            width: "100%",
            placeholder_text_multiple: "Select Options"
        });
    }
});