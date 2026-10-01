const buttonGroup = document.querySelector(".button-group");

const inspectButton = document.createElement("a");

inspectButton.href = "#";
inspectButton.className = "link-button";
inspectButton.innerHTML = "<b>#</b> Inspect";

buttonGroup.appendChild(inspectButton);

let inspecting = false;

const style = document.createElement("style");

style.textContent = `
    .inspect-hover {
        outline: 2px solid #4285f4 !important;
    }

    #inspect-popup {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 700px;
        max-width: 90%;
        max-height: 80vh;
        overflow: auto;
        padding: 20px;
        box-sizing: border-box;
        background: white;
        color: #202124;
        border: 1px solid #dadce0;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        z-index: 10000;
        text-align: left;
        font-family: Arial, sans-serif;
    }

    #inspect-popup h2 {
        margin-top: 0;
        font-weight: normal;
    }

    #inspect-popup h3 {
        margin-top: 20px;
    }

    #inspect-popup pre {
        background: #f8f9fa;
        padding: 12px;
        border-radius: 4px;
        overflow-x: auto;
        white-space: pre-wrap;
        word-break: break-word;
    }

   #inspect-close {
        display: block;
        margin-left: auto;
        border: 1px solid #dadce0;
        background: #f8f9fa;
        padding: 8px 15px;
        cursor: pointer;
        margin-bottom: 15px;
    }

    #inspect-overlay {
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.25);
        z-index: 9999;
    }
`;

document.head.appendChild(style);

function formatCSS(rule) {
    let css = rule.cssText;

    const start = css.indexOf("{");
    const end = css.lastIndexOf("}");

    if (start === -1 || end === -1) {
        return css;
    }

    const selector = css.substring(0, start).trim();
    const properties = css.substring(start + 1, end).trim();

    let result = selector + " {\n";

    properties.split(";").forEach(property => {
        property = property.trim();

        if (property) {
            result += "    " + property + ";\n";
        }
    });

    result += "}";

    return result;
}

function showInspector(element) {
    const overlay = document.createElement("div");
    overlay.id = "inspect-overlay";

    const popup = document.createElement("div");
    popup.id = "inspect-popup";

    const close = document.createElement("button");
    close.id = "inspect-close";
    close.textContent = "Close";

    const title = document.createElement("h2");
    title.textContent = element.tagName.toLowerCase();

    const htmlTitle = document.createElement("h3");
    htmlTitle.textContent = "HTML";

    const html = document.createElement("pre");
    html.textContent = element.outerHTML;

    const cssTitle = document.createElement("h3");
    cssTitle.textContent = "CSS";

    const css = document.createElement("pre");

    let cssText = "";

    for (const sheet of document.styleSheets) {
        for (const rule of sheet.cssRules) {
            if (rule.selectorText && element.matches(rule.selectorText)) {
                cssText += formatCSS(rule) + "\n";
            }
        }
    }

    if (!cssText) {
        cssText = "No explicit CSS found.";
    }

    css.textContent = cssText;

    const computedTitle = document.createElement("h3");
    computedTitle.textContent = "Implied CSS";

    const computedCss = document.createElement("pre");

    const computed = getComputedStyle(element);
    let computedText = "";

    for (let i = 0; i < computed.length; i++) {
        const property = computed[i];

        computedText +=
            property +
            ": " +
            computed.getPropertyValue(property) +
            ";\n";
    }

    computedCss.textContent = computedText;

    popup.append(
        close,
        title,
        htmlTitle,
        html,
        cssTitle,
        css,
        computedTitle,
        computedCss
    );

    document.body.append(overlay, popup);

    close.onclick = () => {
        overlay.remove();
        popup.remove();
    };

    overlay.onclick = () => {
        overlay.remove();
        popup.remove();
    };
}

function startInspecting() {
    inspecting = true;

    inspectButton.innerHTML = "<b>#</b> Exit Inspect";

    document.addEventListener("mouseover", highlight);
    document.addEventListener("mouseout", removeHighlight);
    document.addEventListener("click", inspectClick, true);
}

function stopInspecting() {
    inspecting = false;

    inspectButton.innerHTML = "<b>#</b> Inspect";

    document.removeEventListener("mouseover", highlight);
    document.removeEventListener("mouseout", removeHighlight);
    document.removeEventListener("click", inspectClick, true);

    document
        .querySelectorAll(".inspect-hover")
        .forEach(element => {
            element.classList.remove("inspect-hover");
        });
}

function highlight(event) {
    if (!inspecting) return;

    event.target.classList.add("inspect-hover");
}

function removeHighlight(event) {
    event.target.classList.remove("inspect-hover");
}

function inspectClick(event) {
    if (!inspecting) return;

    if (event.target === inspectButton) {
        return;
    }

    event.preventDefault();
    event.stopPropagation();

    stopInspecting();
    showInspector(event.target);
}

inspectButton.onclick = event => {
    event.preventDefault();

    if (inspecting) {
        stopInspecting();
    } else {
        startInspecting();
    }
};