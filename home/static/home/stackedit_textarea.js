
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
        document.querySelectorAll("#renderMarkdown-loading").forEach((loading) => {
            loading.style.display = "none";
        })
    });

}

function activateEditStackTextarea(element) {
    // Create output division
    output_div = document.createElement("div");
    output_div.id = `div_output_textArea_${element.id}`;
    output_div.className = "textarea-container";
    insertAfter(output_div, element);

    // Provide option to editing
    output_para = document.createElement("p");
    output_option = document.createElement("a");
    output_option.href = `javascript:openEditor('${element.id}')`;
    output_option.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16">
    <path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"/>
    </svg>
    Edit This
    `;
    output_para.appendChild(output_option);
    insertAfter(output_para, output_div);
}

function insertAfter(newNode, existingNode) {
    existingNode.parentNode.insertBefore(newNode, existingNode.nextSibling);
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