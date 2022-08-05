// --------------------- Display Detail -------------------
export default function attachDetail(row) {
    document.querySelector('#detail').innerHTML = row.getData().description_html
    const homeUrl = row.getData().company_homepage_url
    const listingUrl = row.getData().url


    const homepage = document.querySelector('#homepage-ref')
    homepage.href = homeUrl
    homepage.target = "_blank"


    const listing = document.querySelector('#job-listing-ref')
    listing.href = listingUrl
    listing.target = "_blank"

    const title = document.querySelector('#title-ref')
    title.textContent = row.getData().title
    const companyNameHeader = document.querySelector('#company-name-ref')
    companyNameHeader.textContent = row.getData().name


}

