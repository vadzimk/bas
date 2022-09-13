import {Button, Link} from '@mui/material'

export default function RightPanel() {
    return (
        <div id="right_panel" className="details-container">
            <div id="company-references">
                <div style={{
                    display: "flex",
                    flexDirection: "column",
                    fontWeight: "bold",
                }}>
                    <div id="company-name-ref"/>
                    <div id="title-ref"/>
                </div>
                <div style={{
                    display: "flex",
                    flexDirection: "row",
                    justifyContent: "flex-end",
                    flexShrink: 0,
                    height: "40px"
                }}>
                    <Button
                        type="button"
                        className="button"
                        variant="outlined"
                        size="small"
                    >
                        <Link
                            id="homepage-ref"
                        >
                            Homepage
                        </Link>
                    </Button>
                    <Button
                        type="button"
                        className="button"
                        variant="outlined"
                        size="small"
                    >
                        <Link id="job-listing-ref">
                            <img
                                id="board-logo"
                                src="#"
                                alt=""
                                style={{height: "25px"}}
                            />
                        </Link>
                    </Button>
                </div>
            </div>
            <div id="detail"/>
        </div>
    )
}