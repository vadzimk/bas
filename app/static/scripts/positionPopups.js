// columnDefaults: {
// ...
//         cellContext: positionPopups



export default function positionPopups(e) {

    const popups = document.getElementsByClassName('tabulator-menu tabulator-popup-container')
    console.log(popups)
    Array.prototype.forEach.call(popups, pop => {
        const mouse_position_y = e.clientY
        const mouse_position_x = e.clientX
        const scroll_position_y = window.scrollY

        const {y: oldY, height: height} = pop.getBoundingClientRect()
        if (mouse_position_y - height < 0) {
            // element above the window
            let newY = height + mouse_position_y + scroll_position_y + 16;
            pop.style.top = `${newY}px`;
            pop.style.left = `${mouse_position_x + 16}px`
        }
    })
}