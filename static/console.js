const input = document.getElementById("command-input");
const output = document.getElementById("command_text");
const console_file = "console.txt";

input.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        if (input.value == "") {
            refreshConsole();
            return;
        }
        log("raw", [input.value]);
        let command_name = input.value.split(" ")[0];
        let args = input.value.split(" ").slice(1);
        input.value = "";
        execute_python(command_name, args);
        refreshConsole();
    }
});

async function log(type, messages) {
    try {
        const response = await fetch("/console_log", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                type: type,
                messages: messages,
            }),
        });

        if (response.ok) {
            console.log("Command successfully sent to the server.");
        } else {
            console.error("Failed to send command to the server.");
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

async function execute_python(command_name, args) {
    try {
        const response = await fetch("/console_execute_python", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                command_name: command_name,
                args: args,
            }),
        });

        if (response.ok) {
            console.log("Request successfully sent to the server.");
        } else {
            console.error("Failed to send request to the server.");
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

setInterval(refreshConsole, 1000);
let stored_content = "";
function refreshConsole() {
    const logUrl = `/console/${console_file}`;
    fetch(logUrl)
        .then((response) => response.text())
        .then((data) => {
            const lines = data.split("\n");
            const content = lines
                .map((line) => `<p style="margin: 0;">${line}</p>`)
                .join("");
            if (content != stored_content) {
                stored_content = content;
                document.getElementById("console-content-text").innerHTML =
                    content;
                const container = document.getElementById("console-content");
                container.scrollTop = container.scrollHeight;
            }
        })
        .catch((error) => {
            console.error("Error fetching log file:", error);
        });
}

// const input = document.getElementById("command-input");
// const output = document.getElementById("command_text");
// const console_file = "console.txt";

// class CommandInterpreter {
//     async ICommand_test(args) {
//         execute_python("test", args)
//     }
//     async ICommand_help(args) {
//         log("info", [
// "-------------------- HELP --------------------",
// "? 'help': send this help message",
// "-------------------- HELP --------------------",
//         ]);
//     }

//     async interpreteCommand(command) {
//         let method = this[`ICommand_${command.name}`];

//         if (typeof method === "function") {
//             await method.call(this, command.args);
//         } else {
//             log("info", ["Unknown command. Type 'help' for help."]);
//         }
//     }
// }

// let cmdInt = new CommandInterpreter();

// input.addEventListener("keydown", function (event) {
//     if (event.key === "Enter") {
//         if (input.value == "") {
//             refreshConsole();
//             return;
//         }
//         log("raw", [input.value]);
//         let command = {
//             name: input.value.split(" ")[0],
//             args: input.value.split(" ").slice(1),
//         };

//         input.value = "";
//         cmdInt.interpreteCommand(command);
//         refreshConsole();
//     }
// });

// async function log(type, messages) {
//     try {
//         const response = await fetch("/console_log", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//             body: JSON.stringify({
//                 type: type,
//                 messages: messages,
//             }),
//         });

//         if (response.ok) {
//             console.log("Command successfully sent to the server.");
//         } else {
//             console.error("Failed to send command to the server.");
//         }
//     } catch (error) {
//         console.error("Error:", error);
//     }
// }

// async function execute_python(command_name, args) {
//     try {
//         const response = await fetch("/console_execute_python", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//             body: JSON.stringify({
//                 command_name: command_name,
//                 args: args,
//             }),
//         });

//         if (response.ok) {
//             console.log("Request successfully sent to the server.");
//         } else {
//             console.error("Failed to send request to the server.");
//         }
//     } catch (error) {
//         console.error("Error:", error);
//     }
// }

// setInterval(refreshConsole, 1000);
// let stored_content = "";
// function refreshConsole() {
//     const logUrl = `/console/${console_file}`;
//     fetch(logUrl)
//         .then((response) => response.text())
//         .then((data) => {
//             const lines = data.split("\n");
//             const content = lines
//                 .map((line) => `<p style="margin: 0;">${line}</p>`)
//                 .join("");
//             if (content != stored_content) {
//                 stored_content = content;
//                 document.getElementById("console-content-text").innerHTML =
//                     content;
//                 const container = document.getElementById("console-content");
//                 container.scrollTop = container.scrollHeight;
//             }
//         })
//         .catch((error) => {
//             console.error("Error fetching log file:", error);
//         });
// }
