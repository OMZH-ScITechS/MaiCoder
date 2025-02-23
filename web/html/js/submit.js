if (document.querySelector("#editor")!=undefined) {
    const editor = ace.edit("editor", {
        fontSize: "15px"
    })
}

async function get_judge(data) {
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

async function get_problem(id) {
    const response = await fetch("https://api.maicoder.f5.si/problems/" +id)
    const json = await response.json()
    return await json
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

    const response = await get_judge(data)

    let $output = document.querySelector(".output code")
    let $speed = document.querySelector("span.speed")

    $button.classList.remove("loading")
    $output.innerText = response.message.program_message
    $speed.innerText = Math.round(response.speed * 1000) + ' ms'
}

function compiler_change() {
    if (document.querySelector("select.compiler")) {
        let compiler = document.querySelector("select.compiler").value.split(",")[0]
        editor.session.setMode(`ace/mode/${compiler}`);
    }
}

function badge(state) {
    return `<div class="badge ${state}"></div>`
}

compiler_change()