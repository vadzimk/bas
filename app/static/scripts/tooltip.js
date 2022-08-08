
// ----------------------- ToolTip ----------------

export default function makeToolTipFunction({
                                 innerTextGetterFunction = (cell) => cell.getValue(),
                                 innerHtmlGetterFunction
                             } = {}) {
    return function tooltipFunction(e, cell, onRendered) {
        //e - mouseover event
        //cell - cell component
        //onRendered - onRendered callback registration function

        var el = document.createElement("div");
        el.style.maxWidth = "500px";
        el.style.borderRadius = "4px";
        el.style.opacity = "0";
        el.style.transition = 'opacity .15s ease'
        const mouse_position_y = e.clientY
        const mouse_position_x = e.clientX
        const scroll_position_y = window.scrollY


        if (typeof innerHtmlGetterFunction === 'function') {
            el.innerHTML = innerHtmlGetterFunction(cell)
        } else
            el.innerText = innerTextGetterFunction(cell);

        onRendered(() => {
            const {y: oldY, height: height} = el.getBoundingClientRect()
            if (mouse_position_y - height < 0) {
                // element above the window
                let newY = height + mouse_position_y + scroll_position_y + 16;
                el.style.top = `${newY}px`;
                el.style.left = `${mouse_position_x + 16}px`
            }
            el.style.position = 'absolute';
            el.style.opacity = "1";
        })


        return el;
    }
}
