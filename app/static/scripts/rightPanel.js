// ------------------------- Draggable panel ----------------------------

const BORDER_SIZE = 8;
const panel = document.getElementById("right_panel");

let m_pos;

function resize(e) {
    const dx = m_pos - e.x;
    m_pos = e.x;
    panel.style.width = (parseInt(getComputedStyle(panel, '').width) + dx) + "px";
}

panel.addEventListener("mousedown", function (e) {
    if (e.offsetX < BORDER_SIZE) {
        m_pos = e.x;
        document.addEventListener("mousemove", resize, false);
    }
}, false);

document.addEventListener("mouseup", function () {
    document.removeEventListener("mousemove", resize, false);
}, false);
