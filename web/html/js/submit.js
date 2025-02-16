function test() {
    let $compiler = document.querySelector("select.compiler")
    let $code = document.querySelector("textarea.code")
    let $stdin = document.querySelector("textarea.input")
    new Submission($compiler.value, $code.value, $stdin.value).send()
}

class Submission {
    constructor(compiler, code, stdin) {
        this.compiler = compiler
        this.code = code
        this.stdin = stdin
    }
    send() {
        let $code = document.querySelector("code")
        let body = {
            compiler: this.compiler,
            code: this.code,
            stdin: this.stdin
        }
        $code.innerHTML = JSON.stringify(body)
        navigator.clipboard.writeText(JSON.stringify(body))
    }
}