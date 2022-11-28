
processTextAreas();

function processTextAreas() {
    let toRenderMarkdown = document.querySelectorAll("textarea.render-markdown");
    toRenderMarkdown.forEach(element => {
        element.style.display = "none";
        renderMarkdown(element);
    });
    let textAreas = document.querySelectorAll("textarea");
    textAreas.forEach(element => {
        if (element.className != "render-markdown") {
            element.style.display = "none";
            activateEditStackTextarea(element);
        }
    });
}

function renderMarkdown(element) {
    const text = element.value;
    loading_element = document.createElement("div");
    loading_element.id = `renderMarkdown-loading`;
    loading_element.innerHTML = "Loading, Please Wait...";
    element.parentElement.appendChild(loading_element);
    const stackEdit = new Stackedit();
    stackEdit.openFile({
        name: "sample",
        content: {
            text: text
        }
    }, true);
    stackEdit.on('fileChange', (file) => {
        element.outerHTML = file.content.html;
        document.querySelectorAll("#renderMarkdown-loading").forEach((loading)=>{
            loading.style.display = "none";
        })
    });

}

function activateEditStackTextarea(element) {
    // Create output division
    output_div = document.createElement("div");
    output_div.id = `div_output_textArea_${element.id}`;
    output_div.className = "textarea-container";
    element.parentElement.appendChild(output_div);

    // Provide option to editing
    output_div.outerHTML += `
    <a href="javascript:openEditor('${element.id}')">Edit with StackEdit</a>
    `;
}


function openEditor(textAreaId) {
    element = document.getElementById(textAreaId);
    output = document.getElementById(`div_output_textArea_${textAreaId}`)
    console.log("Done");

    const stackEdit = new Stackedit();
    stackEdit.openFile({
        name: element.id,
        content: {
            text: element.value
        }
    });

    stackEdit.on('fileChange', (file) => {
        element.value = file.content.text;
        output.innerHTML = file.content.html
    });

}