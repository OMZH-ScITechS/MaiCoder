const editor = ace.edit("editor", {
    fontSize: "15px"
})

async function getData(data) {
    const url = "https://api.maicoder.f5.si/judge/test";
    try {
        const response = await fetch(url, {
            method: "POST",
            body: JSON.stringify(data),
        });
        if (!response.ok) {
            throw new Error(`レスポンスステータス: ${response.status}`);
        }
        const json = await response.json();
        return json
    } catch (error) {
        return error
    }
}

async function go() {
    let data = {
        compiler: document.querySelector("select.compiler").value.split(",")[1],
        code: editor.getValue(),
        stdin: document.querySelector("textarea.input").value
    }

    console.log(data)

    let $button = document.querySelector("button.go")
    $button.classList.add("loading")

    const response = await getData(data)

    let $output = document.querySelector(".output code")
    let $speed = document.querySelector("span.speed")

    $button.classList.remove("loading")
    $output.innerText = response.message.program_message
    $speed.innerText = Math.round(response.speed * 1000) + ' ms'
}

function compiler_change() {
    let compiler = document.querySelector("select.compiler").value.split(",")[0]
    editor.session.setMode(`ace/mode/${compiler}`);
}

function badge(state){
    return `<div class="badge ${state}"></div>`
}

compiler_change()