import LinkedinSearchCard from "./LinkedinSearchCard";
import {IndeedSearchCard} from "./IndeedSearchCard";
import linkedin_logo from "../../../assets/icons8-linkedin-2.svg"
import indeed_logo from "../../../assets/icons8-indeed.svg"
import {createContext, useContext} from "react";
import {SearchCardContext} from "../../../App";
import { Box, Image } from '@chakra-ui/react'

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
        <div style={{display: "flex", margin: "8px 0", gap: "4px"}}>
            <div style={{margin: "auto 0"}}>
                <Box
                    as='button' borderRadius='base' overflow='hidden' borderWidth='2px'
                    style={{
                        height: 32,
                        width: 32,
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center"
                    }}
                >
                    <Image
                        src={platforms[platform].logo}
                        alt="Linkedin"
                        style={{height: "22px"}}
                    />

                </Box>
            </div>
            <Component/>
        </div>
    )
}

export const JobBoardContext = createContext({
    initialValues: null,
    radiusOptions: null,
    experienceOptions: null,
    ageOptions: null,
    ExperienceSelect: null
})