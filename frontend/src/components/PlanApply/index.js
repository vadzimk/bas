import Results from "../Results";
import {getPlanApply, updatePlanAppyRow} from "../../services/planApplyService";

export function PlanApply() {
    return (
        <Results
            getData={getPlanApply}
            updateRow={updatePlanAppyRow}
        />
    )
}