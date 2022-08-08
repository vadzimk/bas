// {% with distance_options=['distance-one', 'distance-two'], experience_options=['experience-one', 'experience-two'], date_options=['date-one', 'date-two'] %}
//     {% include "_search.html" %}
// {% endwith %}`;

const app = Vue.createApp({
    // delimiters: ['${', '}'],
    data() {
        return {
            message: "hello"
        }
    },
    template: `<div>${message}</div>`
})
app.config.compilerOptions.delimiters = ['${', '}']
app.mount('#app')