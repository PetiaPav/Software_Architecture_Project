function print(rows = 1) {
    const filename  = 'ThisIsYourPDFFilename.pdf';
    let size = (rows * 9) + 80;

    html2canvas(document.querySelector('#content'), 
                            {scale: 3}
                     ).then(canvas => {
        let pdf = new jsPDF('p', 'mm', 'a4');
        pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 10, 10, 190, size);
        pdf.save(filename);
    });
}