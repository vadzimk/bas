// --------------------- Display Detail -------------------
export default function attachDetail(row) {
    document.querySelector('#detail').innerHTML = row.getData().description_html
    const homeUrl = row.getData().company_homepage_url
    const listingUrl = row.getData().url
    console.log('url', listingUrl)

    const homepageButton = document.querySelector('#homepage-ref')
    homepageButton.addEventListener('click', (e) => {
        window.open(homeUrl, "_blank")
    })
    const listingButton = document.querySelector('#job-listing-ref')
    listingButton.addEventListener('click', (e) => {
        window.open(listingUrl, "_blank")
    })

    const title = document.querySelector('#title-ref')
    title.textContent = row.getData().title
    const companyNameHeader = document.querySelector('#company-name-ref')
    companyNameHeader.textContent = row.getData().company_name


}

