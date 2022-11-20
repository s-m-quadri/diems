
let textAreas = document.querySelectorAll("textarea");
textAreas.forEach(element => {
    output_div = document.createElement("div");
    output_div.id = `div_output_textArea_${element.id}`;
    output_div.className = "textarea-container";
    element.style.display = "none";
    element.parentElement.appendChild(output_div);
    output_div.outerHTML += `
    <a href="javascript:openEditor('${element.id}')">Edit with StackEdit</a>
    `;
});

function openEditor(textAreaId) {
    element = document.getElementById(textAreaId);
    output = document.getElementById(`div_output_textArea_${textAreaId}`)
    console.log("Done");
    
    const stackEdit = new Stackedit();
    stackEdit.openFile({
        name: element.id, // with an optional filename
        content: {
            text: element.value // and the Markdown content.
        }
    });

    stackEdit.on('fileChange', (file) => {
        element.value = file.content.text;
        output.innerHTML = file.content.html
    });

}

// const el = document.querySelector('textarea');
//     const stackedit = new Stackedit();

//     // Open the iframe
//     stackedit.openFile({
//         name: 'Filename', // with an optional filename
//         content: {
//             text: "el.value" // and the Markdown content.
//         }
//     });

//     // Listen to StackEdit events and apply the changes to the textarea.
//     stackedit.on('fileChange', (file) => {
//         el.value = file.content.text;
// });