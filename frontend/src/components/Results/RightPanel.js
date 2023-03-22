import {Button, Link} from '@chakra-ui/react'
import PropTypes from 'prop-types'
import {useEffect, useRef} from "react";


RightPanel.propTypes = {
    detail: PropTypes.shape({
        description: PropTypes.string,
        company_homepage_url: PropTypes.string,
        job_url: PropTypes.string,
        title: PropTypes.string,
        company_name: PropTypes.string,
        boardLogo: PropTypes.string,
    })
}

export default function RightPanel({detail}) {

    const descriptionHtml = detail.description
    const element = document.createElement('div')
    element.innerHTML = descriptionHtml
    const descriptionLength = element.innerText.split(/\s+/).length;


    return (
        <div
            id="right_panel"
            className="details-container"
            style={{
                display: "flex",
                right: 0,
                backgroundColor: "#d6e4ea",
                flexDirection: "column",
            }}
        >
            <div id="company-references">
                <div style={{
                    display: "flex",
                    flexDirection: "column",
                    fontWeight: "bold",
                }}>
                    <div id="company-name-ref" dangerouslySetInnerHTML={{__html: detail.company_name}}/>
                    <div id="title-ref" dangerouslySetInnerHTML={{__html: detail.title}}/>
                </div>
                <div style={{
                    display: "flex",
                    flexDirection: "row",
                    justifyContent: "flex-end",
                    flexShrink: 0,
                    height: "40px",
                    gap: "4px"
                }}>
                    {detail.company_homepage_url &&
                        <Button
                            variant="outline"
                            size="sm"
                            className="button"
                        >
                            <Link
                                id="homepage-ref"
                                href={detail.company_homepage_url}
                                target="_blank"
                            >
                                Homepage
                            </Link>
                        </Button>}
                    {detail.job_url &&
                        <Button
                            variant="outline"
                            size="sm"
                            className="button"
                        >
                            <Link
                                id="job-listing-ref"
                                href={detail.job_url}
                                target="_blank"
                            >
                                <img
                                    id="board-logo"
                                    src={detail.boardLogo}
                                    alt={detail.boardLogo.includes('indeed') ? 'Indeed' : 'Linkedin'}
                                    style={{height: "25px"}}
                                />
                            </Link>
                        </Button>}
                </div>
            </div>
            {detail.description &&
                <div style={{fontSize: "12px", textAlign: "right", padding: "0 8px"}}
                >
                    <span>word-count: </span><span>{descriptionLength}</span>
                </div>}
            <div
                id="detail"
                dangerouslySetInnerHTML={{__html: detail.description}}
                style={{overflow: "scroll"}}
            />
        </div>
    )
}