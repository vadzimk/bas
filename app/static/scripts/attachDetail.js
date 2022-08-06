// --------------------- Display Detail -------------------
export default function attachDetail(row) {
    document.querySelector('#detail').innerHTML = row.getData().description_html
    const homeUrl = row.getData().homepage_url
    const listingUrl = row.getData().url


    const homepage = document.querySelector('#homepage-ref')
    if (homeUrl) {
        homepage.href = homeUrl
        homepage.target = "_blank"
        homepage.parentElement.style.display = "block"
    } else {
        homepage.parentElement.style.display = "none"
    }

    const listing = document.querySelector('#job-listing-ref')
    if (listingUrl) {
        listing.href = listingUrl
        listing.target = "_blank"
        listing.parentElement.style.display = "block"
    } else {
        listing.parentElement.style.display = "none"
    }

    const title = document.querySelector('#title-ref')
    title.textContent = row.getData().title
    const companyNameHeader = document.querySelector('#company-name-ref')
    companyNameHeader.textContent = row.getData().name

    const boardLogo = document.querySelector('#board-logo')
    const profile_url = row.getData().profile_url

    if (profile_url.includes('indeed')) {
        boardLogo.src = 'static/assets/icons8-indeed.svg'

    } else if (profile_url.includes('linkedin')) {
        boardLogo.src = 'static/assets/icons8-linkedin-2.svg'
    }

}

