import LinkedinSearchCard from "./LinkedinSearchCard";
import {IndeedSearchCard} from "./IndeedSearchCard";
import linkedin_logo from "../../assets/icons8-linkedin-2.svg"
import indeed_logo from "../../assets/icons8-indeed.svg"
import {Card as MuiCard} from '@mui/material';
import {createContext, useContext} from "react";
import {SearchCardContext} from "../../App";


export function SearchCard() {
    const {platform} = useContext(SearchCardContext)
    const platforms = {
        linkedin: {
            component: LinkedinSearchCard,
            logo: linkedin_logo,
        },
        indeed: {
            component: IndeedSearchCard,
            logo: indeed_logo,
        }
    }
    const Component = platforms[platform].component
    return (
        <div style={{display: "flex", margin: "10px 0"}}>
            <div style={{margin: "auto 0"}}>
                <MuiCard
                    variant="outlined"
                    sx={{
                        height: 38,
                        width: 38,
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center"
                    }}
                >
                    <img
                        src={platforms[platform].logo}
                        alt="Linkedin"
                        style={{height: "25px"}}
                    />

                </MuiCard>
            </div>
            <Component/>
        </div>
    )
}

export const JobBoardContext = createContext({
    radiusOptions: null,
    experienceOptions: null,
    ageOptions: null,
    ExperienceSelect: null,
})